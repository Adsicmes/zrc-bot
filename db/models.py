"""
可选：在此定义项目级共享模型，或由各插件在自己的包内定义并继承 db.Base。

SQLAlchemy 2.0 推荐写法：DeclarativeBase + Mapped + mapped_column。
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


def _utc_now() -> datetime:
    return datetime.now(UTC)


class ExampleEntity(Base):
    """示例表：演示 2.0 风格映射。可按需删除或改为实际业务模型。"""

    __tablename__ = "example_entity"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=_utc_now)

    def __repr__(self) -> str:
        return f"ExampleEntity(id={self.id!r}, name={self.name!r})"
