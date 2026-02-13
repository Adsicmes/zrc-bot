# 运行与架构

## 启动流程

1. `main.py` 创建 `BotClient` 并调用 `run_frontend()` 或 `run_backend()`。
2. BotClient 启动 NapCat 连接、建立 WebSocket，并初始化 PluginLoader。
3. PluginLoader 先加载内置插件（SystemManager、UnifiedRegistry），再加载 `plugins/` 下用户插件。
4. 事件经 Adapter → EventBus 分发给各插件的 command/filter 处理函数。

## 事件流

- 消息事件：NapCat → Adapter → EventBus → UnifiedRegistry（命令/过滤器匹配）→ 对应插件 handler。
- 权限由 NcatBot 的 RBAC 与 command_registry 的权限组控制。

## 依赖关系

- 用户插件可声明 `dependencies` 依赖其他插件；加载顺序由 PluginLoader 按依赖拓扑排序。

---

*可补充 Mermaid 图或更细的时序说明。*
