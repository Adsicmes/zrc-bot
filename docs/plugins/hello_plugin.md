# HelloPlugin

## 简介

示例插件：提供 `/hello` 命令与私聊消息的自动回复，用于演示 NcatBot 的 command_registry 与 filter_registry 用法。

## 命令

| 命令 | 参数 | 说明 | 权限 |
|------|------|------|------|
| /hello | 无 | 回复「你好！我是插件 HelloPlugin。」 | 默认随框架（通常 root 组） |

## 权限与过滤

- 命令通过 `command_registry.command("hello")` 注册，权限组依赖全局配置。
- 私聊消息通过 `filter_registry.private_filter` 注册，收到任意私聊即回复「你发送了一条私聊消息！」。

## 配置项

无独立配置项。

## 示例

- 群聊或私聊发送：`/hello` → Bot 回复问候语。
- 私聊发送任意内容 → Bot 回复私聊提示句。
