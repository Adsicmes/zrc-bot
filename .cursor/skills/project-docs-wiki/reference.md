# docs/ 目录结构与模板

## 推荐目录结构

```
docs/
├── README.md           # Wiki 索引与导航
├── design.md           # 设计考虑与架构决策
├── runtime.md          # 运行思路、生命周期、事件流
├── permissions.md      # 权限体系与角色
├── glossary.md         # 独特名词与术语表
└── plugins/            # 各插件用法
    ├── README.md       # 插件列表与索引
    ├── hello_plugin.md
    └── ...
```

## 插件文档模板（plugins/xxx.md）

```markdown
# 插件名（如 HelloPlugin）

## 简介
一句话说明插件用途。

## 命令
| 命令 | 参数 | 说明 | 权限 |
|------|------|------|------|
| /hello | 无 | 示例 | 所有用户 |

## 权限与过滤
- 需要的权限组或 filter。
- 群聊/私聊是否可用。

## 配置项（如有）
- 配置路径、键、含义、默认值。

## 示例
- 典型使用示例。
```

## 权限文档要点（permissions.md）

- root / admin / 普通用户 等角色定义。
- 与 NcatBot 权限组、command_registry 的对应关系。
- 如何设置 root、如何添加 admin。

## 名词表要点（glossary.md）

- 项目内专有缩写（如 ZRC、UR 等）。
- 与 NcatBot/NapCat 相关术语在本项目中的指代。
- 业务或领域专有概念。

## 设计文档要点（design.md）

- 为什么选用 NcatBot、NapCat。
- 插件划分与职责边界。
- 扩展点与不支持的场景。
- 安全与配置上的取舍。

## 运行与架构要点（runtime.md）

- 启动顺序：main → BotClient → PluginLoader → 内置插件 → 用户插件。
- 事件流：Adapter → EventBus → 插件 handler。
- 依赖关系图（可文字或 Mermaid）。
