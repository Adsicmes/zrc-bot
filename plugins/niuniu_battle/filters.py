"""牛牛大作战：群启用过滤与管理员判断。"""

from __future__ import annotations

from ncatbot.plugin_system import NcatBotPlugin
from ncatbot.plugin_system import filter_registry
from ncatbot.plugin_system.builtin_plugin.unified_registry.filter_system.base import (
    BaseFilter,
)
from ncatbot.utils import status
from ncatbot.utils.assets.literals import PermissionGroup

from ncatbot.core.event import GroupMessageEvent

# 供过滤器读取当前插件 config（由 niuniu_battle 在 on_load 中 set_plugin_ref）
_plugin_ref: NcatBotPlugin | None = None


def set_plugin_ref(plugin: NcatBotPlugin | None) -> None:
    """由主插件在 on_load 时调用，供过滤器读取 config。"""
    global _plugin_ref
    _plugin_ref = plugin


def is_group_enabled(group_id: str) -> bool:
    """当前群是否在可用群聊列表中（读自插件 config）。"""
    if _plugin_ref is None:
        return False
    ids = _plugin_ref.config.get("enabled_group_ids")
    if ids is None:
        return False
    return group_id in [str(x) for x in ids]


def is_admin(event: GroupMessageEvent) -> bool:
    """发送者是否为管理员（admin/root）。"""
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
        return is_group_enabled(str(gid))


def niuniu_enabled_filter(func):
    """仅当当前群在可用群聊列表内时调用 handler。"""
    filter_registry.add_filter_to_function(func, NiuNiuBattleEnabledFilter())
    return func
