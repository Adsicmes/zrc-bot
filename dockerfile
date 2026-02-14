# 基于 Astral uv 的 Alpine 镜像构建 zrc-bot
# 国内构建可选用镜像加速，参考：https://gitee.com/wangnov/uv-custom/releases
FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /app

# 可选：国内 PyPI 镜像（构建时生效，可按需取消注释或替换）
ENV UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple
ENV UV_PYTHON_INSTALL_MIRROR=https://ghfast.top/https://github.com/astral-sh/python-build-standalone/releases/download

# 先复制依赖声明，利用层缓存
COPY pyproject.toml uv.lock ./
# 仅安装生产依赖，不装 dev（如 ruff）
RUN uv sync --frozen --no-dev

# 复制项目代码与默认配置
COPY main.py config.yaml ./
COPY db ./db
COPY plugins ./plugins
COPY utils ./utils

# 运行时目录：data/、logs/ 建议挂载卷持久化
ENV UV_PROJECT_ENVIRONMENT=/app/.venv
CMD ["uv", "run", "python", "main.py"]
