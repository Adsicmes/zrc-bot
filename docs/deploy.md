# 部署文档

本文说明如何部署 ZRC Bot 与 Napcat，支持本地运行与 Docker Compose 两种方式。

## 一、本地运行

### 1. 环境准备

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)（推荐）或 pip
- 已启动的 [Napcat](https://github.com/NapNeko/NapCatQQ)（WebSocket 与 Web 管理界面可用）

### 2. 安装与启动

```bash
# 克隆仓库后进入项目目录
cd zrc-bot

# 安装依赖（uv）
uv sync

# 编辑 config.yaml，确认 napcat.ws_uri、napcat.webui_uri、token 与 Napcat 一致
# 默认：ws_uri: ws://localhost:3001，webui_uri: http://localhost:6099

# 启动机器人
uv run python main.py
```

Napcat 需单独安装并启动，并在其 Web 管理界面（默认 6099 端口）登录 QQ。

---

## 二、Docker Compose 部署

使用仓库根目录的 `docker-compose.yml` 可一键启动 **Napcat** 与 **ZRC Bot**，二者在同一网络中通过服务名通信。

### 1. 前置要求

- 已安装 [Docker](https://docs.docker.com/get-docker/) 与 [Docker Compose](https://docs.docker.com/compose/install/)
- 可选：为 Napcat 配置 `NAPCAT_UID`、`NAPCAT_GID` 环境变量（见 Napcat 官方文档）

### 2. 配置文件

Compose 中 **zrc-bot** 通过挂载使用宿主机上的 `config.yaml`、`data`、`logs`。与 Napcat 联用时，必须让机器人连接容器内的 Napcat 服务名，而非 `localhost`。

在项目根目录的 `config.yaml` 中修改（或复制一份专用于 Docker 的配置并挂载）：

```yaml
napcat:
  ws_uri: ws://napcat:3001      # 容器内 Napcat 服务名
  webui_uri: http://napcat:6099
  ws_token: NcatBot             # 与 Napcat 内配置一致
  # ... 其他项保持不变
```

若使用独立配置文件（如 `config.docker.yaml`），可在 `docker-compose.yml` 中把挂载改为：

```yaml
volumes:
  - ./config.docker.yaml:/app/config.yaml
  - ./data:/app/data
  - ./logs:/app/logs
```

### 3. 启动与停止

```bash
cd zrc-bot

# 构建并启动（首次会构建 zrc-bot 镜像）
docker compose up -d

# 查看日志
docker compose logs -f zrc-bot
docker compose logs -f napcat

# 停止
docker compose down
```

### 4. 端口与访问

| 服务    | 宿主机端口 | 说明 |
|---------|------------|------|
| Napcat  | 36099      | Web 管理界面（对应容器内 6099），用于登录 QQ、配置 Napcat |

容器内端口说明：

- **3000**：Napcat HTTP API（未映射到宿主机，仅供同网络内服务使用）
- **3001**：Napcat 正向 WebSocket，zrc-bot 连接 `ws://napcat:3001`
- **6099**：Napcat Web 管理界面，已映射为宿主机 **36099**

在浏览器访问：`http://<宿主机IP>:36099`，按 Napcat 提示完成 QQ 登录与配置。

### 5. 数据持久化

以下目录通过卷挂载，数据保存在宿主机，重启容器不会丢失：

- `./config.yaml` → 机器人配置
- `./data` → 插件数据（如牛牛大作战等）
- `./logs` → 日志目录

请勿删除上述目录；首次部署前可先创建空目录：`mkdir -p data logs`。

### 6. 仅构建 zrc-bot 镜像（不包含 Napcat）

若已有 Napcat 或使用其他方式部署 Napcat，可仅构建并运行 zrc-bot：

```bash
docker build -t zrc-bot:latest .
docker run -d --name zrc-bot \
  -v $(pwd)/config.yaml:/app/config.yaml \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  --network host \
  zrc-bot:latest
```

使用 `--network host` 时，`config.yaml` 中 `napcat.ws_uri`、`napcat.webui_uri` 可继续使用 `localhost`。若接入已有 Docker 网络，可改为 `--network container:<napcat容器名>` 或自定义网络并指定 Napcat 的容器名/IP。

---

## 三、GitHub Actions 镜像构建

对仓库打 tag `v*.*.*`（如 `v0.1.0`）时，GitHub Actions 会自动构建镜像并推送到 GitHub Container Registry (GHCR)。

- 镜像地址：`ghcr.io/<你的用户名或组织>/zrc-bot:latest` 或 `ghcr.io/.../zrc-bot:v0.1.0`
- 使用方式：将 `docker-compose.yml` 中 zrc-bot 的 `build: .` 改为 `image: ghcr.io/<org>/zrc-bot:latest` 即可拉取预构建镜像，无需本地构建。

---

*部署相关问题可参考 [运行与架构](runtime.md)、[权限说明](permissions.md) 及 [项目 Wiki](README.md)。*
