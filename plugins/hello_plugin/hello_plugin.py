"""NcatBot 插件模式最小示例 - 插件实现。"""

from ncatbot.plugin_system import NcatBotPlugin
from ncatbot.plugin_system import command_registry
from ncatbot.plugin_system import filter_registry
from ncatbot.core.event import BaseMessageEvent, PrivateMessageEvent


class HelloPlugin(NcatBotPlugin):
    """示例插件：命令 hello + 私聊回复。"""

    name = "HelloPlugin"
    version = "1.0.0"
    dependencies = {}

    async def on_load(self):
        """插件加载时调用，可留空保持轻量。"""
        pass

    @command_registry.command("hello")
    async def hello_cmd(self, event: BaseMessageEvent):
        """收到 hello 命令时回复。"""
        await event.reply("你好！我是插件 HelloPlugin。")

    @filter_registry.private_filter
    async def on_private_msg(self, event: PrivateMessageEvent):
        """收到任意私聊消息时回复。"""
        await event.reply("你发送了一条私聊消息！")
