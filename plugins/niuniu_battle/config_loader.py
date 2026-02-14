"""牛牛大作战：按 NcatBot 插件配置规范持久化配置。

配置存储在 data/<插件名>/<插件名>.yaml，与 NcatBot 官方一致。
插件通过 register_config 注册默认值，运行时通过本模块的 save_plugin_config 写回文件。
参考：https://docs.ncatbot.xyz/guide/plugin-config/
"""

from __future__ import annotations

from pathlib import Path

import yaml


def _config_path(plugin_name: str) -> Path:
    return Path("data") / plugin_name / f"{plugin_name}.yaml"


def save_plugin_config(plugin_name: str, config: dict) -> None:
    """将插件配置字典写入 data/<插件名>/<插件名>.yaml，供 NcatBot 下次加载时读取。"""
    path = _config_path(plugin_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
