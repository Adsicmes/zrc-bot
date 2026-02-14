"""牛牛大作战：触发词常量与严格匹配逻辑（见 docs/design/drafts/2026-02-14）。"""

from __future__ import annotations

from ncatbot.core.event import GroupMessageEvent
from ncatbot.core.event.message_segment import At

# 触发词（可后续从配置读取）
TRIGGER_DAO = ("导",)
TRIGGER_RI = ("日群友", "草群友", "操群友")
TRIGGER_MY = ("我的牛牛", "我的牛子")
TRIGGER_RANK = ("牛牛排行榜",)
TRIGGER_VIEW = ("查看牛牛",)
TRIGGER_SET = ("设置牛牛",)
TRIGGER_ON = ("开启牛牛大作战",)
TRIGGER_OFF = ("关闭牛牛大作战",)


def first_at_qq(event: GroupMessageEvent) -> str | None:
    """消息中第一个 @ 的用户 QQ（非 all）。"""
    try:
        ats = event.message.filter(At)
    except Exception:
        ats = []
    for seg in ats:
        qq = getattr(seg, "qq", None)
        if qq and str(qq) != "all":
            return str(qq)
    return None


def trigger_exact(text: str, triggers: tuple[str, ...]) -> bool:
    """严格匹配：strip 后整句等于某触发词（空格变体已由 strip 覆盖）。"""
    return text in triggers


def trigger_ri_match(text: str, event: GroupMessageEvent) -> bool:
    """日群友类：整句等于触发词，或 触发词+空白+@某人 且 @ 后无其它内容。"""
    if text in TRIGGER_RI:
        return True
    for t in TRIGGER_RI:
        if not text.startswith(t):
            continue
        rest = text[len(t) :].strip()
        if rest == "":
            return True
        if " " not in rest and first_at_qq(event) is not None:
            return True
    return False


def trigger_view_match(text: str, event: GroupMessageEvent) -> bool:
    """查看牛牛：以触发词开头，且后缀仅为空白+@某人（无其它文字）。"""
    for t in TRIGGER_VIEW:
        if not text.startswith(t):
            continue
        rest = text[len(t) :].strip()
        if rest == "":
            return False
        if " " not in rest and first_at_qq(event) is not None:
            return True
    return False
