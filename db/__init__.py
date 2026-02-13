"""
SQLAlchemy 2.0 + SQLite 集成。

用法（最新写法）:
    from db import Base, get_session
    from db import engine, Session

    # 定义模型（继承 Base，使用 Mapped / mapped_column）
    class MyModel(Base):
        __tablename__ = "my_table"
        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        name: Mapped[str] = mapped_column(String(255))

    # 建表（应用启动时调用一次）
    init_db()

    # 在插件或业务代码中使用会话
    with get_session() as session:
        session.add(MyModel(name="example"))
    # 自动 commit（成功时）并关闭 session
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from db.base import Base

# 默认数据库路径（工作目录下的 data/zrc_bot.db）
_DEFAULT_DB_DIR = "data"
_DEFAULT_DB_FILE = "zrc_bot.db"


def _make_engine(url: str | None = None, *, echo: bool = False):
    if url is None:
        os.makedirs(_DEFAULT_DB_DIR, exist_ok=True)
        path = os.path.join(_DEFAULT_DB_DIR, _DEFAULT_DB_FILE)
        url = f"sqlite:///{path}"
    return create_engine(
        url,
        echo=echo,
        connect_args={"check_same_thread": False},  # SQLite 多线程需显式允许
    )


# 可从环境变量或后续配置覆盖；默认不 echo
_db_url = os.environ.get("ZRC_BOT_DATABASE_URL")
_echo = os.environ.get("ZRC_BOT_SQL_ECHO", "").lower() in ("1", "true", "yes")
engine = _make_engine(_db_url, echo=_echo)

# 会话工厂：Session(engine) 等价于 sessionmaker(bind=engine)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)


def init_db() -> None:
    """创建所有已注册的 ORM 表（若不存在）。应在应用启动时调用一次。"""
    # 导入所有定义在 db 包内的模型，使其注册到 Base.metadata
    from db import models  # noqa: F401
    Base.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """获取会话的上下文管理器，退出时自动 commit（无异常）或 rollback（有异常）。"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "get_session",
    "init_db",
]
