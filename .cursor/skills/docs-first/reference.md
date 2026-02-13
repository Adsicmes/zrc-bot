# 查阅路径速查

## 设计草稿

- **目录**：`docs/design/drafts/`
- **说明**：`docs/design/drafts/README.md`
- **用途**：插件/功能拟设计、提案、RFC；按插件名或主题命名的 .md 文件。

## 相关 Wiki（docs 导航）

- **总索引**：`docs/README.md`
- **设计原则与约束**：`docs/design.md`（含单向依赖等）
- **运行与架构**：`docs/runtime.md`
- **权限**：`docs/permissions.md`
- **术语**：`docs/glossary.md`
- **数据库**：`docs/database.md`
- **插件**：`docs/plugins/README.md` 及各 `docs/plugins/xxx.md`

## 项目原则（写码与审阅时须遵守）

当前文档化原则见 `docs/design.md`，例如：

- 单向依赖（模块依赖 DAG，无循环）
- 插件与扩展的约束（如 `docs/design.md` 扩展与约束一节）
