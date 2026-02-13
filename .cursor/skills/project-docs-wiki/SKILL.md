---
name: project-docs-wiki
description: Centralizes all project documentation in docs/. Use when adding or updating project docs, plugin usage, permissions, terminology, design notes, or runtime flow. Ensures docs/ serves as the project wiki for zrc-bot.
---

# 项目文档与 Wiki 规范

## 核心约定

- **中心文档目录**：`docs/`。所有与本项目相关的文档一律放在此目录。
- **docs 即项目 Wiki**：`docs/` 内应形成可被 AI 与人类查阅的完整项目知识库。

## 必须包含的内容

在 `docs/` 中维护以下内容，并在新增/变更时同步更新：

| 类别 | 说明 | 建议路径/文件 |
|------|------|----------------|
| **插件用法** | 每个插件的命令、参数、示例、适用场景 | `docs/plugins/`，每插件一文档 |
| **权限** | 权限体系、角色、谁可用哪些命令/功能 | `docs/permissions.md` 或 `docs/权限.md` |
| **独特名词** | 项目内专有术语、缩写、概念定义 | `docs/glossary.md` 或 `docs/名词表.md` |
| **设计考虑** | 架构决策、取舍、扩展点、约束 | `docs/design.md` 或 `docs/设计.md` |
| **运行思路** | 启动流程、事件流、生命周期、依赖关系 | `docs/runtime.md` 或 `docs/运行与架构.md` |
| **Wiki 索引** | 总览与导航，便于发现所有文档 | `docs/README.md` 或 `docs/index.md` |

## 何时应用本规范

- 新增或修改插件时：在 `docs/plugins/` 下新增或更新对应插件文档（用法、权限、命令）。
- 变更权限/角色时：更新 `docs/` 中的权限说明。
- 引入新概念或专有名词时：更新 `docs/` 中的名词表/术语表。
- 做架构或设计决策时：在 `docs/design.md`（或等价文件）中记录原因与考虑。
- 回答“项目怎么跑”“有哪些命令”“权限怎么设”时：优先引用或编写 `docs/` 内内容。

## 文档编写原则

- **一处权威**：同一类信息只在一处详细写，其他文件用链接或简短引用。
- **可被检索**：标题和段落清晰，便于搜索和 AI 理解。
- **与代码同步**：功能、命令、权限变更后，及时更新对应 doc。

## 详细结构参考

完整目录与模板见 [reference.md](reference.md)。
