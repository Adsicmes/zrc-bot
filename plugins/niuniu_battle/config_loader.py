"""牛牛大作战：可用群聊配置读写。列表为空时默认全部不开放。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

CONFIG_DIR = Path("data") / "NiuNiuBattle"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_CONFIG = {"enabled_group_ids": []}


def _ensure_config_dir() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        return dict(DEFAULT_CONFIG)
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_CONFIG)
    if not data:
        return dict(DEFAULT_CONFIG)
    return data


def save_config(config: dict) -> None:
    _ensure_config_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def get_enabled_group_ids() -> List[str]:
    cfg = load_config()
    ids = cfg.get("enabled_group_ids")
    if ids is None:
        return []
    return [str(x) for x in ids]


def is_group_enabled(group_id: str) -> bool:
    return group_id in get_enabled_group_ids()


def add_group(group_id: str) -> None:
    cfg = load_config()
    ids = cfg.get("enabled_group_ids") or []
    ids = [str(x) for x in ids]
    if group_id not in ids:
        ids.append(group_id)
        cfg["enabled_group_ids"] = ids
        save_config(cfg)


def remove_group(group_id: str) -> None:
    cfg = load_config()
    ids = cfg.get("enabled_group_ids") or []
    ids = [str(x) for x in ids if str(x) != group_id]
    cfg["enabled_group_ids"] = ids
    save_config(cfg)
