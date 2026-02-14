"""牛牛大作战：指令具体逻辑（导、日、查询、排行榜、设置）。"""

from __future__ import annotations

import random

from ncatbot.core.event import GroupMessageEvent
from ncatbot.utils import status

from db import get_session
from utils import MsgTemplates
from plugins.niuniu_battle import messages as msg_tpl
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
from plugins.niuniu_battle.triggers import first_at_qq


async def do_dao(event: GroupMessageEvent, group_id: str, user_id: str) -> None:
    """执行「导」：自身长度变化，当日设了次数 +1。"""
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


async def do_ri(
    event: GroupMessageEvent, group_id: str, user_id: str
) -> None:
    """执行「日群友」：指定或随机目标长度变化，发起者当日设了次数 +1。"""
    target_id = first_at_qq(event)
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


async def do_my(
    event: GroupMessageEvent, group_id: str, user_id: str
) -> None:
    """查询自己的牛牛长度。"""
    with get_session() as session:
        u = get_or_create_user(session, group_id, user_id)
    await event.reply(
        MsgTemplates.pick(msg_tpl.MY_LENGTH, length=f"{u.length:.2f}"),
        at=True,
    )


async def do_view(
    event: GroupMessageEvent, group_id: str, target_qq: str
) -> None:
    """查看某人的牛牛长度。"""
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


async def do_rank(event: GroupMessageEvent, group_id: str) -> None:
    """本群牛牛排行榜（前十与后十）。"""
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


async def do_set(
    event: GroupMessageEvent,
    group_id: str,
    target_qq: str,
    key: str,
    value_str: str,
) -> None:
    """设置某人长度或设了次数（管理员）。"""
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
