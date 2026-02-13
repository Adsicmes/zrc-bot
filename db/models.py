"""
可选：在此定义项目级共享模型，或由各插件在自己的包内定义并继承 db.Base。

SQLAlchemy 2.0 推荐写法：DeclarativeBase + Mapped + mapped_column。
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Float, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


def _utc_now() -> datetime:
    return datetime.now(UTC)


# --------------- 牛牛大作战 (NiuNiuBattle) ---------------
# 按「群 + 用户」维度；同一用户在不同群数据独立。

class NiuniuUser(Base):
    """用户在某群内的牛牛长度。"""

    __tablename__ = "niuniu_user"
    __table_args__ = (UniqueConstraint("group_id", "user_id", name="uq_niuniu_user_group_user"),)

    group_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    length: Mapped[float] = mapped_column(Float, nullable=False, default=8.0)
    updated_at: Mapped[datetime] = mapped_column(default=_utc_now)

    def __repr__(self) -> str:
        return f"NiuniuUser(group_id={self.group_id!r}, user_id={self.user_id!r}, length={self.length})"


class NiuniuDailyCount(Base):
    """用户在某群、某自然日的设了次数（按发起者计数）。"""

    __tablename__ = "niuniu_daily_count"
    __table_args__ = (
        UniqueConstraint("group_id", "user_id", "date", name="uq_niuniu_daily_group_user_date"),
    )

    group_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    date: Mapped[str] = mapped_column(String(10), primary_key=True)  # YYYY-MM-DD
    count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def __repr__(self) -> str:
        return f"NiuniuDailyCount(group_id={self.group_id!r}, user_id={self.user_id!r}, date={self.date!r}, count={self.count})"


# --------------- 示例（可按需删除） ---------------

class ExampleEntity(Base):
    """示例表：演示 2.0 风格映射。可按需删除或改为实际业务模型。"""

    __tablename__ = "example_entity"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=_utc_now)

    def __repr__(self) -> str:
        return f"ExampleEntity(id={self.id!r}, name={self.name!r})"
