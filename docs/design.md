# 设计考虑

（在此记录架构决策、技术选型理由、扩展点与约束。）

## 技术选型

- **NcatBot**：基于 NapCat 的 Python SDK，用于 QQ 机器人逻辑与插件系统。
- **NapCat**：协议端，连接 NTQQ 与 OneBot 接口。

## 扩展与约束

- 插件统一放在 `plugins/`，通过 NcatBot 的 PluginLoader 加载。
- 内置插件（SystemManager、UnifiedRegistry）由框架加载，当前无配置关闭方式。

---

*随项目演进补充设计理由与取舍。*
