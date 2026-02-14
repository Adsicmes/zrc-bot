"""牛牛大作战 (NiuNiuBattle) 插件：仅群聊，可用群聊由插件配置项控制。"""

from __future__ import annotations

import json
import random
from pathlib import Path

from ncatbot.core.event import GroupMessageEvent
from ncatbot.core.event.message_segment import At
from ncatbot.plugin_system import NcatBotPlugin
from ncatbot.plugin_system import filter_registry, group_filter, on_message
from ncatbot.plugin_system.builtin_plugin.unified_registry.filter_system.base import (
    BaseFilter,
)
from ncatbot.utils import status
from ncatbot.utils.assets.literals import PermissionGroup

from db import get_session
from utils import MsgTemplates
from plugins.niuniu_battle import messages as msg_tpl
from plugins.niuniu_battle.config_loader import save_plugin_config
from plugins.niuniu_battle.service import (
    INITIAL_LENGTH,
    LENGTH_MAX,
    LENGTH_MIN,
    apply_delta,
    get_daily_count_for_today,
    get_or_create_user,
    get_ranking,
    inc_daily_count,
    set_daily_count,
    set_length,
)


# 供过滤器读取当前插件 config（在 on_load 中赋值）
_plugin_ref: NcatBotPlugin | None = None


def _is_group_enabled(group_id: str) -> bool:
    """当前群是否在可用群聊列表中（读自插件 config）。"""
    if _plugin_ref is None:
        return False
    ids = _plugin_ref.config.get("enabled_group_ids")
    if ids is None:
        return False
    return group_id in [str(x) for x in ids]


def _is_admin(event: GroupMessageEvent) -> bool:
    if not status.global_access_manager:
        return False
    uid = event.user_id
    return (
        status.global_access_manager.user_has_role(uid, PermissionGroup.ADMIN.value)
        or status.global_access_manager.user_has_role(uid, PermissionGroup.ROOT.value)
    )


class NiuNiuBattleEnabledFilter(BaseFilter):
    """仅当当前群在可用群聊列表内时通过。"""

    def check(self, event) -> bool:
        if not getattr(event, "is_group_event", lambda: False)():
            return False
        gid = getattr(event, "group_id", None)
        if not gid:
            return False
        return _is_group_enabled(str(gid))


# 触发词（可后续从配置读取）
TRIGGER_DAO = ("导",)
TRIGGER_RI = ("日群友", "草群友", "操群友")
TRIGGER_MY = ("我的牛牛", "我的牛子")
TRIGGER_RANK = ("牛牛排行榜",)
TRIGGER_VIEW = ("查看牛牛",)
TRIGGER_SET = ("设置牛牛",)
TRIGGER_ON = ("开启牛牛大作战",)
TRIGGER_OFF = ("关闭牛牛大作战",)


def _strip_text(event: GroupMessageEvent) -> str:
    try:
        return (event.message.concatenate_text() or "").strip()
    except Exception:
        return (event.raw_message or "").strip()


def _niuniu_enabled_filter(func):
    """仅当当前群在可用群聊列表内时调用 handler。"""
    filter_registry.add_filter_to_function(func, NiuNiuBattleEnabledFilter())
    return func


def _first_at_qq(event: GroupMessageEvent) -> str | None:
    try:
        ats = event.message.filter(At)
    except Exception:
        ats = []
    for seg in ats:
        qq = getattr(seg, "qq", None)
        if qq and str(qq) != "all":
            return str(qq)
    return None


class NiuNiuBattlePlugin(NcatBotPlugin):
    name = "NiuNiuBattle"
    version = "1.0.0"
    dependencies = {}

    async def on_load(self):
        global _plugin_ref
        self.register_config("enabled_group_ids", [])
        # 从旧版 config.json 迁移到 NcatBot 插件配置 yaml
        _legacy_path = Path("data") / "NiuNiuBattle" / "config.json"
        if _legacy_path.exists():
            try:
                with open(_legacy_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                legacy_ids = data.get("enabled_group_ids")
                if legacy_ids is not None:
                    self.config["enabled_group_ids"] = [str(x) for x in legacy_ids]
                    save_plugin_config(self.name, self.config)
                _legacy_path.unlink()
            except (json.JSONDecodeError, OSError):
                pass
        _plugin_ref = self

    @on_message
    @group_filter
    @_niuniu_enabled_filter
    async def on_group_niuniu(self, event: GroupMessageEvent):
        if not isinstance(event, GroupMessageEvent):
            return
        text = _strip_text(event)
        if not text:
            return

        # 私聊不处理（group_filter 已保证是群消息）
        group_id = str(event.group_id)
        user_id = str(event.user_id)

        # 开启/关闭牛牛大作战（仅管理员，当前群）
        if any(text == t for t in TRIGGER_ON):
            if not _is_admin(event):
                await event.reply(MsgTemplates.pick(msg_tpl.NEED_ADMIN), at=True)
                return
            ids = self.config.get("enabled_group_ids") or []
            ids = [str(x) for x in ids]
            if group_id not in ids:
                ids.append(group_id)
                self.config["enabled_group_ids"] = ids
                save_plugin_config(self.name, self.config)
            await event.reply(MsgTemplates.pick(msg_tpl.GROUP_ENABLED), at=True)
            return
        if any(text == t for t in TRIGGER_OFF):
            if not _is_admin(event):
                await event.reply(MsgTemplates.pick(msg_tpl.NEED_ADMIN), at=True)
                return
            ids = [x for x in (self.config.get("enabled_group_ids") or []) if str(x) != group_id]
            self.config["enabled_group_ids"] = ids
            save_plugin_config(self.name, self.config)
            await event.reply(MsgTemplates.pick(msg_tpl.GROUP_DISABLED), at=True)
            return

        # 导
        if any(text == t or text.startswith(t) for t in TRIGGER_DAO):
            await self._do_dao(event, group_id, user_id)
            return

        # 日（随机或 @）
        if any(text == t or text.startswith(t) for t in TRIGGER_RI):
            await self._do_ri(event, group_id, user_id)
            return

        # 我的牛牛
        if any(text == t or text.startswith(t) for t in TRIGGER_MY):
            await self._do_my(event, group_id, user_id)
            return

        # 牛牛排行榜
        if any(text == t or text.startswith(t) for t in TRIGGER_RANK):
            await self._do_rank(event, group_id)
            return

        # 查看牛牛@某人
        if any(text.startswith(t) for t in TRIGGER_VIEW):
            target_qq = _first_at_qq(event)
            if not target_qq:
                await event.reply(MsgTemplates.pick(msg_tpl.VIEW_NEED_AT), at=True)
                return
            await self._do_view(event, group_id, target_qq)
            return

        # 设置牛牛@某人 键 数值（管理员）
        if any(text.startswith(t) for t in TRIGGER_SET):
            if not _is_admin(event):
                await event.reply("需要管理员权限。", at=True)
                return
            target_qq = _first_at_qq(event)
            if not target_qq:
                await event.reply(MsgTemplates.pick(msg_tpl.SET_FORMAT_EXAMPLE), at=True)
                return
            rest = text
            for t in TRIGGER_SET:
                if rest.startswith(t):
                    rest = rest[len(t) :].strip()
                    break
            parts = rest.split()
            if len(parts) < 2:
                await event.reply(MsgTemplates.pick(msg_tpl.SET_FORMAT_EXAMPLE), at=True)
                return
            key, value_str = parts[0], parts[1]
            await self._do_set(event, group_id, target_qq, key, value_str)
            return

    async def _do_dao(self, event: GroupMessageEvent, group_id: str, user_id: str):
        with get_session() as session:
            u = get_or_create_user(session, group_id, user_id)
            old_len = u.length
            n = get_daily_count_for_today(session, group_id, user_id)
            new_len = apply_delta(old_len, n)
            u.length = new_len
            inc_daily_count(session, group_id, user_id)
        await event.reply(
            MsgTemplates.pick(
                msg_tpl.DAO_RESULT,
                old_len=f"{old_len:.2f}",
                new_len=f"{new_len:.2f}",
            ),
            at=True,
        )

    async def _do_ri(
        self, event: GroupMessageEvent, group_id: str, user_id: str
    ):
        target_id = _first_at_qq(event)
        if target_id:
            if target_id == user_id:
                await event.reply(MsgTemplates.pick(msg_tpl.RI_SELF_FORBIDDEN), at=True)
                return
        else:
            api = status.global_api
            if not api:
                await event.reply(MsgTemplates.pick(msg_tpl.RI_RANDOM_FAIL), at=True)
                return
            try:
                member_list = await api.get_group_member_list(group_id)
            except Exception:
                await event.reply(MsgTemplates.pick(msg_tpl.RI_NO_TARGET), at=True)
                return
            members = getattr(member_list, "members", []) or []
            candidates = [str(m.user_id) for m in members if str(m.user_id) != user_id]
            if not candidates:
                await event.reply(MsgTemplates.pick(msg_tpl.RI_NO_TARGET), at=True)
                return
            target_id = random.choice(candidates)

        with get_session() as session:
            target_user = get_or_create_user(session, group_id, target_id)
            n = get_daily_count_for_today(session, group_id, user_id)
            new_len = apply_delta(target_user.length, n)
            target_user.length = new_len
            inc_daily_count(session, group_id, user_id)
        await event.reply(
            MsgTemplates.pick(msg_tpl.RI_RESULT, new_len=f"{new_len:.2f}"),
            at=True,
        )

    async def _do_my(
        self, event: GroupMessageEvent, group_id: str, user_id: str
    ):
        with get_session() as session:
            u = get_or_create_user(session, group_id, user_id)
        await event.reply(
            MsgTemplates.pick(msg_tpl.MY_LENGTH, length=f"{u.length:.2f}"),
            at=True,
        )

    async def _do_view(
        self, event: GroupMessageEvent, group_id: str, target_qq: str
    ):
        with get_session() as session:
            u = get_or_create_user(session, group_id, target_qq)
        await event.reply(
            MsgTemplates.pick(
                msg_tpl.VIEW_OTHER,
                length=f"{u.length:.2f}",
                initial=f"{INITIAL_LENGTH:.2f}",
            ),
            at=True,
        )

    async def _do_rank(self, event: GroupMessageEvent, group_id: str):
        with get_session() as session:
            top10, bottom10 = get_ranking(session, group_id)
        if not top10 and not bottom10:
            await event.reply(MsgTemplates.pick(msg_tpl.RANK_EMPTY), at=True)
            return
        lines = []
        if top10:
            lines.append(MsgTemplates.pick(msg_tpl.RANK_TOP_HEADER))
            for i, (uid, length) in enumerate(top10, 1):
                lines.append(
                    MsgTemplates.pick(
                        msg_tpl.RANK_LINE,
                        rank=i,
                        user_id=uid,
                        length=f"{length:.2f}",
                    )
                )
        if bottom10:
            lines.append(MsgTemplates.pick(msg_tpl.RANK_BOTTOM_HEADER))
            for i, (uid, length) in enumerate(bottom10, 1):
                lines.append(
                    MsgTemplates.pick(
                        msg_tpl.RANK_LINE,
                        rank=i,
                        user_id=uid,
                        length=f"{length:.2f}",
                    )
                )
        await event.reply("\n".join(lines), at=True)

    async def _do_set(
        self,
        event: GroupMessageEvent,
        group_id: str,
        target_qq: str,
        key: str,
        value_str: str,
    ):
        key = key.strip()
        if key == "长度":
            try:
                value = float(value_str.strip())
            except ValueError:
                await event.reply(MsgTemplates.pick(msg_tpl.SET_LENGTH_NOT_NUMBER), at=True)
                return
            if not (LENGTH_MIN <= value <= LENGTH_MAX):
                await event.reply(
                    MsgTemplates.pick(
                    msg_tpl.SET_LENGTH_OUT_OF_RANGE,
                    min=LENGTH_MIN,
                    max=LENGTH_MAX,
                ),
                    at=True,
                )
                return
            with get_session() as session:
                set_length(session, group_id, target_qq, value)
            await event.reply(
                MsgTemplates.pick(msg_tpl.SET_LENGTH_OK, value=f"{value:.2f}"),
                at=True,
            )
            return
        if key == "设了次数":
            try:
                value = int(value_str.strip())
            except ValueError:
                await event.reply(MsgTemplates.pick(msg_tpl.SET_COUNT_NOT_INT), at=True)
                return
            if value < 0:
                await event.reply(MsgTemplates.pick(msg_tpl.SET_COUNT_NEGATIVE), at=True)
                return
            with get_session() as session:
                set_daily_count(session, group_id, target_qq, value)
            await event.reply(
                MsgTemplates.pick(msg_tpl.SET_COUNT_OK, value=value),
                at=True,
            )
            return
        await event.reply(
            MsgTemplates.pick(msg_tpl.SET_UNKNOWN_KEY, key=key),
            at=True,
        )
