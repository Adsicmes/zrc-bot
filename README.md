# ZRC Bot

基于 [NcatBot](https://github.com/NcatBot/NcatBot) 插件模式的 QQ 机器人，连接 [Napcat](https://github.com/NapNeko/NapCatQQ) 作为 OneBot 前端。

## 环境要求

- Python 3.12+
- [Napcat](https://github.com/NapNeko/NapCatQQ)（用于登录 QQ 并暴露 OneBot 协议）
- 依赖管理：[uv](https://docs.astral.sh/uv/)（推荐）或 pip

## 快速开始

### 本地运行

1. 安装依赖：`uv sync`（或 `pip install -e .`）
2. 启动 Napcat，并确保 WebSocket 与 Web 管理界面可访问（默认如 `localhost:3001`、`localhost:6099`）
3. 按需修改项目根目录 `config.yaml`（`napcat.ws_uri`、`napcat.webui_uri`、token 等）
4. 运行：`uv run python main.py`（或 `python main.py`）

### Docker 部署

使用本仓库提供的 `docker-compose.yml` 可同时启动 Napcat 与 ZRC Bot，详见 **[部署文档](docs/deploy.md)**。

## 文档

- **[项目 Wiki](docs/README.md)**：设计、规约、数据库、权限、插件列表等
- **[部署文档](docs/deploy.md)**：Docker / Docker Compose 部署步骤与配置说明

## 许可证

见仓库说明。
