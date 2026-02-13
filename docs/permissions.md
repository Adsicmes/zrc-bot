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

*随插件与权限策略变更更新。*
