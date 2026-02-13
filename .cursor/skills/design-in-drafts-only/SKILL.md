---
name: design-in-drafts-only
description: When designing plugins or features, draft and iterate only in docs/design/drafts/. Do not modify project code until the user explicitly instructs to implement or write code. Use when the user asks to design a plugin, plan a feature, or propose functionality.
---

# 设计阶段仅起草文档、不改代码

在设计插件或功能时，**只可在 `docs/design/drafts/` 中起草与修改规划文档**。在用户**明确要求开始执行或编写代码之前**，**不得修改项目中的任何代码**。

## 何时应用

- 用户提出「设计一个插件」「规划某功能」「先设计再实现」等需求时。
- 讨论新插件/新功能的命令、权限、配置、流程时。
- 任何「先做方案、尚未要写代码」的设计讨论。

## 必须遵守的规则

### 设计阶段允许做的

- 在 **`docs/design/drafts/`** 下新建或修改草稿文档（如 `插件名.md`、`功能简述.md`）。
- 在草稿中写：目标、背景、命令/接口设想、权限、配置、与现有插件关系、TBD。
- 根据讨论多次修改同一份草稿，或拆分/合并草稿文件。
- 引用或链接 `docs/` 内其他文档（如 design.md、plugins/、glossary.md）。

### 设计阶段禁止做的

- **不得**修改 `plugins/` 下任何代码或新增插件目录。
- **不得**修改 `main.py`、`db/`、`config.yaml` 等项目代码或配置。
- **不得**新增或修改除 `docs/design/drafts/` 以外的实现性代码（若仅更新 `docs/` 中非草案的说明文档，需与「只改草案」的意图一致；设计阶段优先只动草案）。

## 何时可以开始改代码

仅当用户**明确**表示要落地实现时，方可修改项目代码。明确表述包括但不限于：

- 「开始执行」「开始实现」「可以写代码了」「去实现吧」
- 「修改代码」「编写代码」「写代码」「实现这个设计」
- 「按草稿实现」「按设计稿开发」

若用户未使用上述或类似表述，一律视为仍在设计阶段，**仅允许在 `docs/design/drafts/` 中起草与修改**。

## 草稿命名与结构

- 命名：按 [docs/design/drafts/README.md](docs/design/drafts/README.md) 的约定（插件名.md、主题-日期.md 等）。
- 内容建议：目标与背景、命令/接口、权限与配置、与现有插件关系、TBD；详见草案目录内 README。

## 小结

| 阶段     | 可做                         | 不可做           |
|----------|------------------------------|------------------|
| 设计阶段 | 仅在 `docs/design/drafts/` 起草与修改 | 改 plugins/、main、db、config 等代码 |
| 执行阶段 | 按用户指示修改代码、实现功能 | —                |

执行阶段仅在使用户**明确要求开始执行或编写代码**之后开始。
