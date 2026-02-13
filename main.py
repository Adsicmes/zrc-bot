"""NcatBot 插件模式最小示例 - 入口。工作目录为 main.py 所在目录，插件从 plugins/ 加载。"""

from ncatbot.core import BotClient

from db import init_db

# 启动前初始化 SQLite 表结构
init_db()

bot = BotClient()
bot.run_frontend()
