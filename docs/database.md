# 数据库（SQLAlchemy 2.0 + SQLite）

项目使用 **SQLAlchemy 2.0** 风格 + **SQLite**，数据库层在 `db` 包中。

## 配置

- **默认路径**：`data/zrc_bot.db`（相对运行目录，目录不存在会自动创建）。
- **覆盖 URL**：环境变量 `ZRC_BOT_DATABASE_URL`，例如：
  - `export ZRC_BOT_DATABASE_URL="sqlite:///data/my.db"`
  - Windows: `set ZRC_BOT_DATABASE_URL=sqlite:///data/my.db`
- **打印 SQL**：`ZRC_BOT_SQL_ECHO=1` 时会在控制台输出 SQL（调试用）。

## 2.0 写法要点

- **Base**：继承 `DeclarativeBase`，用 `Mapped[...]` 和 `mapped_column()` 声明列。
- **会话**：用 `get_session()` 上下文管理器，自动 commit/rollback/close。
- **建表**：入口处已调用 `init_db()`，新模型需在 `init_db()` 执行前被导入（例如在 `db.models` 或插件内定义并 import）。

## 在插件中使用

```python
from db import Base, get_session
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

# 1. 定义模型（继承 Base）
class MyPluginData(Base):
    __tablename__ = "my_plugin_data"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(64), unique=True)
    value: Mapped[str] = mapped_column(String(512))

# 2. 在插件加载时确保表存在：在 on_load 里 import 本模型后调用 init_db() 一次，
#    或把模型放在 db.models 中由 main 统一 import 后 init_db()。

# 3. 使用会话
with get_session() as session:
    session.add(MyPluginData(key="k", value="v"))
    # 退出 with 时自动 commit
```

## 项目内模块

| 模块 | 说明 |
|------|------|
| `db` | 导出 `engine`, `Base`, `SessionLocal`, `get_session`, `init_db` |
| `db.models` | 可选共享模型（含示例 `ExampleEntity`） |

## 依赖

- `sqlalchemy>=2.0`（见 `pyproject.toml`）。安装后运行 `uv sync` 或 `pip install -e .`。
