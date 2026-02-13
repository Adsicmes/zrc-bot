"""
文案模板工具：基于 string.Template，支持多条同义文案、回复时随机抽取。

用法:
    from utils import MsgTemplates

    # 定义文案数组（占位符 $name）
    HELLO = MsgTemplates.create("你好 $user！", "欢迎 $user～")
    # 回复时随机选一条并替换占位符
    text = MsgTemplates.pick(HELLO, user="张三")
"""

from __future__ import annotations

import random
from string import Template
from typing import Any


class MsgTemplates:
    """文案模板工具类：创建模板数组，回复时随机抽取一条并替换占位符。"""

    @staticmethod
    def create(*strings: str) -> tuple[Template, ...]:
        """用多条同义文案创建模板数组。占位符使用 $name 或 ${name}。"""
        return tuple(Template(s) for s in strings)

    @staticmethod
    def pick(templates: tuple[Template, ...], **kwargs: Any) -> str:
        """从模板数组中随机选一条，做 substitute(**kwargs)，返回最终字符串。"""
        return random.choice(templates).substitute(**kwargs)
