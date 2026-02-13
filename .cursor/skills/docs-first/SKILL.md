---
name: docs-first
description: Before designing, writing, or reviewing project code, consult docs/ including design principles, design drafts, and wiki. Use when designing features, implementing code, or performing code review for zrc-bot.
---

# 先查阅文档再动手

在为项目**设计**、**编写代码**或**审阅代码**之前，必须先查阅 `docs/` 中的相关内容，再开始执行。

## 何时应用

- 接到设计类需求（新功能、新插件、架构调整）时。
- 动手写或改项目代码之前。
- 做代码审阅（review）之前。

## 必读与选读

**第一步：入口与原则**

- 打开 [docs/README.md](docs/README.md) 了解 Wiki 导航。
- 阅读 [docs/design.md](docs/design.md)：**设计考虑**与**项目原则**（如单向依赖）。

**第二步：与当前任务相关的文档**

| 任务类型 | 建议查阅 |
|----------|----------|
| 设计 / 新功能 / 新插件 | [docs/design/drafts/](docs/design/drafts/) 中是否有相关草稿；[docs/design.md](docs/design.md) 扩展与约束 |
| 写插件或改插件 | [docs/plugins/README.md](docs/plugins/README.md) 及对应插件文档；[docs/permissions.md](docs/permissions.md) |
| 用数据库 | [docs/database.md](docs/database.md) |
| 审阅 / 理解运行方式 | [docs/runtime.md](docs/runtime.md)；[docs/glossary.md](docs/glossary.md) 名词表 |

**第三步：再动手**

- 设计：遵循已记录的原则与约束，有草稿则对齐草稿。
- 编码：符合文档中的架构、权限与用法约定。
- 审阅：以文档中的原则与约定为基准提出意见。

## 原则摘要（来自 docs）

- **单向依赖**：模块依赖为 DAG，禁止循环引用；基础放底层，上层只引用底层。
- **docs 即 Wiki**：项目说明、插件用法、权限、术语、设计、运行思路均在 `docs/` 维护，一处权威。

## 参考

- 文档结构与更多约定见 [project-docs-wiki](.cursor/skills/project-docs-wiki/SKILL.md) 与 [reference.md](.cursor/skills/project-docs-wiki/reference.md)。
