# 项目规约

本文档记录项目内**统一约定**，所有插件与模块应遵循。

---

## 发送给用户的文案：MsgTemplates

**规约**：面向用户的回复文案使用 `utils.MsgTemplates`，采用「模板数组 + 回复时随机抽取」的方式。

### 目的

- 文案集中管理，便于修改与多语言扩展。
- 同义多句随机轮换，减少重复感。
- 占位符统一用 `string.Template` 语法（`$name` / `${name}`），避免手写 f-string 分散在逻辑里。

### 实现位置

- 工具类：`utils/msg_templates.py`（`MsgTemplates`）
- 使用：`from utils import MsgTemplates`

### API

| 方法 | 说明 |
|------|------|
| `MsgTemplates.create(*strings)` | 用多条同义文案创建模板数组，返回 `tuple[Template, ...]`。占位符使用 `$name` 或 `${name}`。 |
| `MsgTemplates.pick(templates, **kwargs)` | 从模板数组中随机选一条，执行 `substitute(**kwargs)`，返回最终字符串。 |

### 用法示例

```python
from utils import MsgTemplates

# 1. 定义文案数组（通常在插件内的 messages 模块或同文件顶部）
HELLO = MsgTemplates.create("你好 $user！", "欢迎 $user～")
ERR_PERMISSION = MsgTemplates.create("需要管理员权限。")

# 2. 回复时随机选一条并替换占位符
await event.reply(MsgTemplates.pick(HELLO, user="张三"), at=True)
await event.reply(MsgTemplates.pick(ERR_PERMISSION), at=True)  # 无占位符则不传 kwargs
```

### 约定

- **文案存放**：每条业务（插件）的文案模板建议放在该插件下的单独模块中（如 `plugins/xxx/messages.py`），常量命名清晰、按功能分组。
- **每条文案多句**：同一场景可提供多条同义句，用 `MsgTemplates.create("A。", "B。", "C。")`；仅一句时也写为数组，便于后续扩展。
- **占位符命名**：使用有意义的名字（如 `$user`、`$length`、`$min`），在调用 `pick` 时传入对应关键字参数；数值、长度等需格式化的在调用处先格式成字符串再传入（如 `length=f"{x:.2f}"`）。

### 参考

- 实现：`utils/msg_templates.py`
- 使用示例：`plugins/niuniu_battle/messages.py`（定义）、`plugins/niuniu_battle/niuniu_battle.py`（调用）

---

*新增规约时请在此文档追加并注明适用范围。*
