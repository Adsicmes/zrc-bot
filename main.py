"""NcatBot 插件模式最小示例 - 入口。工作目录为 main.py 所在目录，插件从 plugins/ 加载。"""

from ncatbot.core import BotClient

bot = BotClient()
bot.run_frontend()
