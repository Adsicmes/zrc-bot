# 项目规约

本文档记录项目内**统一约定**，所有插件与模块应遵循。

---

## 插件与代码结构：单文件保持较小、按功能拆分、标准化插件目录

**规约**：单文件保持较小体量；按职责拆分为独立文件与独立文件夹；插件采用统一的目录与命名结构，便于维护与复用。

### 原则

- **单文件较小**：单个 Python 文件不宜过大（建议常规业务文件控制在数百行内），逻辑复杂时拆成多文件，每个文件聚焦单一职责。
- **按功能拆分**：一个「功能单元」对应一个文件或一个子包；可独立测试、可独立复用的部分放在独立模块中。
- **插件结构统一**：所有插件遵循同一套目录与文件约定，新人上手与跨插件复用更简单。

### 插件标准结构

每个插件对应 **一个独立文件夹**，位于 `plugins/<插件目录名>/`，目录名建议与插件 ID 一致（小写、下划线，如 `niuniu_battle`）。

| 文件 / 目录 | 是否必须 | 说明 |
|-------------|----------|------|
| `__init__.py` | 必须 | 导出插件主类（如 `from .niuniu_battle import NiuNiuBattlePlugin`），供 NcatBot 加载。 |
| `<插件主文件>.py` | 必须 | 插件类、事件注册、指令入口等「入口逻辑」；文件名可与目录名一致（如 `niuniu_battle/niuniu_battle.py`）。 |
| `messages.py` | 推荐 | 面向用户的文案模板（含 `MsgTemplates` 常量），见规约「发送给用户的文案：MsgTemplates」。 |
| `service.py` | 按需 | 业务逻辑、数据读写、算法等，与「事件/指令」解耦，便于单测与复用。 |
| `config_loader.py` 等 | 按需 | 配置读写、持久化等，若仅用 NcatBot 配置项且写回逻辑简单，可与主文件合并。 |

- **禁止**：在 `plugins/` 下放置与插件无关的散落脚本；新插件应为**文件夹**，不在 `plugins/` 根目录单文件实现完整插件（除极简示例外）。
- **命名**：插件目录名、主文件名、插件类名在文档与代码中保持一致（如目录 `niuniu_battle`、主文件 `niuniu_battle.py`、类名 `NiuNiuBattlePlugin`）。

### 单文件与拆分建议

- **主文件**：只保留「注册 handler、解析指令、调用 service/消息」等入口与分支，不堆积长段业务算法或大块数据定义。
- **文案**：统一放在插件内 `messages.py`（或规约允许的等价模块），不散落在主文件。
- **业务与数据**：可读写 DB、调用外部 API、复杂计算等放入 `service.py` 或同名子包（如 `service/` 多文件时）。
- **配置**：配置项注册、默认值、写回逻辑可集中在 `config_loader.py` 或主文件内一小节，避免散落多处。
- **行数参考**：单文件超过约 400～500 行时，优先考虑按「入口 / 文案 / 服务 / 配置」拆成多文件，而不是继续在一个文件中追加。

### 适用范围

- 所有位于 `plugins/` 下的插件；新建或大改插件时须符合上述结构。
- 项目内其他模块（如 `utils/`、`db/`）也可按「单文件较小、按功能拆到独立文件/文件夹」执行，具体命名可与插件规约区分。

### 参考

- 标准结构示例：`plugins/niuniu_battle`（`__init__.py`、`niuniu_battle.py`、`messages.py`、`service.py`、`config_loader.py`）
- 极简示例：`plugins/hello_plugin`（单入口文件 + `__init__.py`）

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

## 插件配置项：NcatBot 官方配置管理

**规约**：插件的可持久化配置项统一使用 [NcatBot 插件配置项](https://docs.ncatbot.xyz/guide/plugin-config/) 机制，不自行维护独立配置文件（如单独 json/yaml）。

### 要点

- 在 `on_load` 中用 `self.register_config("配置项名", 默认值)` 注册。
- 通过 `self.config["配置项名"]` 读取；运行时修改后需自行写回（见下）。
- 配置存储在 `data/<插件名>/<插件名>.yaml`，与 NcatBot 一致，Bot 退出后可手动编辑，下次加载会覆盖默认值。
- 用户可通过系统命令 `/set_config <插件名> <配置项名> <新值>` 或 `/cfg` 别名修改配置。

### 程序内修改配置并持久化

若插件在运行中修改了 `self.config`，需将整份 `self.config` 写回 `data/<插件名>/<插件名>.yaml`，否则重启后会被默认值或旧文件覆盖。可复用项目内已有的写回方式（例如牛牛大作战的 `config_loader.save_plugin_config(self.name, self.config)`），或按同一路径与 YAML 格式自行实现。

### 参考

- 官方文档：[插件配置项 | NcatBot 文档](https://docs.ncatbot.xyz/guide/plugin-config/)
- 本项示例：`plugins/niuniu_battle`（`register_config("enabled_group_ids", [])`、`save_plugin_config` 写回）

---

## 指令触发：严格匹配（开发规范）

**规约**：凡通过**纯文本消息**触发的指令（无斜杠前缀），一律采用**严格匹配**，避免讨论、吐槽等自然语句误触发。所有相关插件实现须遵循下列规则。

### 原则

- **仅当用户明显在发指令时才触发**；句中「出现关键词」或「以关键词开头」但整句为自然语言的，不触发。
- **空格**视为合法变体：指令前后仅带空白（strip 后等价于触发词）可触发。
- **标点**不视为变体：带标点（如「导。」「日群友。」）不触发。
- **带后缀不触发**：若指令允许「触发词 + 空白 + @某人」形式，则 @ 之后不得再有任何其它文字；如「日群友 @张三 谢谢」不触发。

### 实现要求

| 场景 | 要求 |
|------|------|
| 单触发词（如「导」「我的牛牛」） | 使用 **整句相等** 判定：`text.strip() == 触发词`，禁止 `startswith(触发词)` 或前缀匹配。 |
| 触发词 + @某人 | 仅允许「触发词」或「触发词 + 空白 + @某人」且 **@ 后无其它内容**；带任意后缀一律不触发。 |
| 空格 | 比较前对消息做 `strip()`，即允许前后空白；不再对内容做「去掉标点」等放宽。 |
| 标点 | 不将「去掉句末标点再比较」视为合法变体；带标点即不触发。 |

### 适用范围

- 所有通过群聊/私聊**文本消息**触发的插件指令（含同义触发词如 日群友/草群友/操群友）。
- 斜杠命令（如 `/hello`）若由框架做精确路由，可不受本条约束；若自行解析文本，建议同此严格匹配。

### 参考

- 细则与示例：[设计草稿 2026-02-14 牛牛指令避免误触发](design/drafts/2026-02-14_牛牛指令避免误触发.md)
- 实现示例（待按规约调整）：`plugins/niuniu_battle/niuniu_battle.py`

---

*新增规约时请在此文档追加并注明适用范围。*
