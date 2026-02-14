# 权限说明

## 角色与权限组

- **root**：在 `config.yaml` 中通过 `root` 配置，拥有最高权限（如系统命令 `/set_admin`、`/ncatbot_status` 等）。
- **admin**：由 root 通过 `/set_admin` 添加的管理员。
- **普通用户**：未在 root/admin 中的用户，仅能使用已对普通用户开放的插件命令。

## 与 NcatBot 的对应

- 系统命令（如 `/ncs`、`/sa`）通常仅对 root 组开放。
- 插件内通过 `command_registry.command(...)` 注册时可指定权限组；未指定时以框架默认为准（如 root）。

## 配置

- `config.yaml` 中 `root` 为 root 用户 QQ 号。
- 管理员列表由 NcatBot 持久化在权限数据中，通过 `/set_admin` 管理。

---

## NcatBot RBAC 用法

NcatBot 的权限由内置 **RBAC（角色访问控制）** 管理，数据持久化在 `data/rbac.json`（路径由插件系统配置 `rbac_path` 决定，默认 `./data/rbac.json`）。

### 角色与继承

- 内置三种**权限组**（角色）：`user`、`admin`、`root`。
- **继承关系**：`root` → 继承 `admin` → 继承 `user`。拥有 root 即拥有 admin 与 user 的权限。
- 启动时会把 `config.yaml` 里的 `root`（QQ 号）自动赋予 `root` 角色；其余用户首次被检查时以 `user` 身份加入。

### 管理管理员：/set_admin（仅 root 可用）

- **命令**：`/set_admin <user_id> add` 或 `/sa <user_id> add` — 将某 QQ 设为 admin。
- **移除**：`/set_admin <user_id> remove` 或 `/sa <user_id> remove` — 取消其 admin。
- `user_id` 可为 QQ 号；若消息中带 @，框架会解析出被 @ 者的 QQ 号。
- 仅 **root** 可执行；执行后会写回 `data/rbac.json`。

### 插件内如何检查权限

通过全局的 **`status.global_access_manager`**（类型为 `RBACManager`）判断当前用户是否具备某角色或某权限路径。

**1. 按角色判断（常用）**

- 使用 **`user_has_role(user_id, role_name)`**：判断用户是否拥有某角色（如 admin、root）。
- 角色名为字符串，与 `PermissionGroup` 枚举一致：`PermissionGroup.ROOT.value` 为 `"root"`，`PermissionGroup.ADMIN.value` 为 `"admin"`，`PermissionGroup.USER.value` 为 `"user"`。

示例（仅 admin 或 root 可执行某逻辑）：

```python
from ncatbot.utils import status
from ncatbot.utils.assets.literals import PermissionGroup

def _is_admin(event) -> bool:
    if not status.global_access_manager:
        return False
    uid = event.user_id  # 或 event.sender.xxx，视事件类型而定
    return (
        status.global_access_manager.user_has_role(uid, PermissionGroup.ADMIN.value)
        or status.global_access_manager.user_has_role(uid, PermissionGroup.ROOT.value)
    )

# 在 handler 中
if not _is_admin(event):
    await event.reply("需要管理员权限。")
    return
```

**2. 使用过滤器装饰器（仅群聊/私聊 + 角色）**

- 注册 handler 时加上 **`@admin_filter`**：仅 admin 或 root 可触发。
- **`@root_filter`**：仅 root 可触发。
- **`@group_admin_filter`**：仅群管理员（QQ 群内身份）可触发。
- 这些装饰器内部同样依赖 `status.global_access_manager.user_has_role`。

**3. 按权限路径判断（高级）**

- **`check_permission(user_name, path)`**：判断用户是否拥有某条「权限路径」。
- 需要先在 RBAC 中注册该路径并为角色/用户分配白名单或黑名单；适合细粒度、可配置的权限（如某插件下某命令）。本项目中牛牛大作战等插件目前仅用「角色」判断即可。

### 小结

| 需求           | 做法 |
|----------------|------|
| 只允许 admin 或 root | `status.global_access_manager.user_has_role(uid, "admin") or user_has_role(uid, "root")` 或 `@admin_filter` |
| 只允许 root    | `user_has_role(uid, "root")` 或 `@root_filter` |
| 添加/移除管理员 | root 在聊天中发 `/set_admin <QQ> add` 或 `remove` |
| 数据存储       | `data/rbac.json`，启动时加载，变更时写回 |

---

*随插件与权限策略变更更新。*
