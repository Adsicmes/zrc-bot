"""牛牛大作战：设了曲线、DB 读写、排行榜。"""

from __future__ import annotations

import random
from datetime import date
from typing import List, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import NiuniuDailyCount, NiuniuUser

INITIAL_LENGTH = 8.0
DELTA_MAX = 2.0
BASE = 0.85
DECAY = 0.6
FLOAT_RANGE = 0.06
LENGTH_MIN = -999.99
LENGTH_MAX = 999.99


def _today_str() -> str:
    return date.today().isoformat()


def _round_length(v: float) -> float:
    return round(float(v), 2)


def get_or_create_user(session: Session, group_id: str, user_id: str) -> NiuniuUser:
    row = session.execute(
        select(NiuniuUser).where(
            NiuniuUser.group_id == group_id,
            NiuniuUser.user_id == user_id,
        )
    ).scalars().first()
    if row:
        return row
    row = NiuniuUser(group_id=group_id, user_id=user_id, length=INITIAL_LENGTH)
    session.add(row)
    return row


def get_or_create_daily_count(
    session: Session, group_id: str, user_id: str
) -> NiuniuDailyCount:
    today = _today_str()
    row = session.execute(
        select(NiuniuDailyCount).where(
            NiuniuDailyCount.group_id == group_id,
            NiuniuDailyCount.user_id == user_id,
            NiuniuDailyCount.date == today,
        )
    ).scalars().first()
    if row:
        return row
    row = NiuniuDailyCount(group_id=group_id, user_id=user_id, date=today, count=0)
    session.add(row)
    return row


def p_increase(n: int) -> float:
    """n=发起者当日已设了次数（本次操作前）。返回本次「增加」的概率。"""
    if n <= 0:
        return 1.0
    p_base = BASE * (DECAY ** n)
    p = max(0.0, min(1.0, p_base + random.uniform(-FLOAT_RANGE, FLOAT_RANGE)))
    return p


def apply_delta(current_length: float, n: int) -> float:
    """根据设了次数 n 判定增加/减少，再在 [0, DELTA_MAX] 均匀取幅度，返回新长度。"""
    p = p_increase(n)
    increase = random.random() < p
    delta = random.uniform(0, DELTA_MAX)
    if not increase:
        delta = -delta
    return _round_length(current_length + delta)


def inc_daily_count(session: Session, group_id: str, user_id: str) -> int:
    """发起者当日设了次数 +1，返回加一后的值。"""
    row = get_or_create_daily_count(session, group_id, user_id)
    row.count += 1
    return row.count


def get_ranking(
    session: Session, group_id: str
) -> Tuple[List[Tuple[str, float]], List[Tuple[str, float]]]:
    """(前十最长, 后十最短)，每项 (user_id, length)。"""
    rows = (
        session.execute(
            select(NiuniuUser.user_id, NiuniuUser.length)
            .where(NiuniuUser.group_id == group_id)
            .order_by(NiuniuUser.length.desc())
        )
    ).all()
    if not rows:
        return [], []
    top10 = [tuple(r) for r in rows[:10]]
    bottom10 = [tuple(r) for r in (rows[-10:] if len(rows) >= 10 else rows)]
    return top10, bottom10


def get_daily_count_for_today(session: Session, group_id: str, user_id: str) -> int:
    today = _today_str()
    row = session.execute(
        select(NiuniuDailyCount).where(
            NiuniuDailyCount.group_id == group_id,
            NiuniuDailyCount.user_id == user_id,
            NiuniuDailyCount.date == today,
        )
    ).scalars().first()
    return int(row.count) if row else 0


def set_length(session: Session, group_id: str, user_id: str, value: float) -> None:
    """设置某人在某群的长度（会 get_or_create_user 再更新）。"""
    u = get_or_create_user(session, group_id, user_id)
    u.length = _round_length(value)


def set_daily_count(
    session: Session, group_id: str, user_id: str, value: int
) -> None:
    """设置某人当日设了次数（无则插入）。"""
    today = _today_str()
    row = session.execute(
        select(NiuniuDailyCount).where(
            NiuniuDailyCount.group_id == group_id,
            NiuniuDailyCount.user_id == user_id,
            NiuniuDailyCount.date == today,
        )
    ).scalars().first()
    if row:
        row.count = value
    else:
        session.add(
            NiuniuDailyCount(group_id=group_id, user_id=user_id, date=today, count=value)
        )
