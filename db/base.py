"""声明式基类，供所有模型继承。单独模块避免与 models 的依赖方向混淆。"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
