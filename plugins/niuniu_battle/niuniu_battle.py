"""牛牛大作战 (NiuNiuBattle) 插件入口：仅群聊，可用群聊由插件配置项控制。"""

from __future__ import annotations

import json
from pathlib import Path

from ncatbot.core.event import GroupMessageEvent
from ncatbot.plugin_system import NcatBotPlugin
from ncatbot.plugin_system import group_filter, on_message

from utils import MsgTemplates
from plugins.niuniu_battle import messages as msg_tpl
from plugins.niuniu_battle.config_loader import save_plugin_config
from plugins.niuniu_battle.filters import (
    is_admin,
    niuniu_enabled_filter,
    set_plugin_ref,
)
from plugins.niuniu_battle.triggers import (
    TRIGGER_DAO,
    TRIGGER_MY,
    TRIGGER_OFF,
    TRIGGER_ON,
    TRIGGER_RANK,
    TRIGGER_SET,
    TRIGGER_VIEW,
    first_at_qq,
    trigger_exact,
    trigger_ri_match,
    trigger_view_match,
)
from plugins.niuniu_battle import handlers as h


def _strip_text(event: GroupMessageEvent) -> str:
    """从事件消息中取出纯文本并 strip。"""
    try:
        return (event.message.concatenate_text() or "").strip()
    except Exception:
        return (event.raw_message or "").strip()


class NiuNiuBattlePlugin(NcatBotPlugin):
    name = "NiuNiuBattle"
    version = "1.0.0"
    dependencies = {}

    async def on_load(self):
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
        set_plugin_ref(self)

    @on_message
    @group_filter
    async def on_group_niuniu_enable_disable(self, event: GroupMessageEvent):
        """开启/关闭牛牛大作战：不要求本群已在可用列表，否则管理员无法在未开启的群里首次开启。"""
        if not isinstance(event, GroupMessageEvent):
            return
        text = _strip_text(event)
        if not text:
            return
        group_id = str(event.group_id)

        if any(text == t for t in TRIGGER_ON):
            if not is_admin(event):
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
            if not is_admin(event):
                await event.reply(MsgTemplates.pick(msg_tpl.NEED_ADMIN), at=True)
                return
            ids = [x for x in (self.config.get("enabled_group_ids") or []) if str(x) != group_id]
            self.config["enabled_group_ids"] = ids
            save_plugin_config(self.name, self.config)
            await event.reply(MsgTemplates.pick(msg_tpl.GROUP_DISABLED), at=True)
            return

    @on_message
    @group_filter
    @niuniu_enabled_filter
    async def on_group_niuniu(self, event: GroupMessageEvent):
        """牛牛指令分发：导、日群友、我的牛牛、排行榜、查看牛牛、设置牛牛。"""
        if not isinstance(event, GroupMessageEvent):
            return
        text = _strip_text(event)
        if not text:
            return
        group_id = str(event.group_id)
        user_id = str(event.user_id)

        if trigger_exact(text, TRIGGER_DAO):
            await h.do_dao(event, group_id, user_id)
            return
        if trigger_ri_match(text, event):
            await h.do_ri(event, group_id, user_id)
            return
        if trigger_exact(text, TRIGGER_MY):
            await h.do_my(event, group_id, user_id)
            return
        if trigger_exact(text, TRIGGER_RANK):
            await h.do_rank(event, group_id)
            return
        if text in TRIGGER_VIEW and first_at_qq(event) is None:
            await event.reply(MsgTemplates.pick(msg_tpl.VIEW_NEED_AT), at=True)
            return
        if trigger_view_match(text, event):
            target_qq = first_at_qq(event)
            if not target_qq:
                await event.reply(MsgTemplates.pick(msg_tpl.VIEW_NEED_AT), at=True)
                return
            await h.do_view(event, group_id, target_qq)
            return
        if any(text.startswith(t) for t in TRIGGER_SET):
            if not is_admin(event):
                await event.reply("需要管理员权限。", at=True)
                return
            target_qq = first_at_qq(event)
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
            await h.do_set(event, group_id, target_qq, key, value_str)
            return
