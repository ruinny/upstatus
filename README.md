# 📝 每日记事本 (UpStatus)

一个简洁、优雅、**安全**的在线记事本应用，支持按日期记录、自动保存、多人共享。基于 Flask + SQLite 构建，无需数据库配置，开箱即用。

> 💡 **适用场景**：个人笔记、临时记录、团队协作、跨设备同步、代码片段分享

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 特性

### 🎯 核心功能
- 📅 **按日期记录** - 每天的笔记独立存储，按日期索引，快速查找
- 💾 **即时自动保存** - 输入后立即自动保存（延迟0秒），防止数据丢失
- 🗄️ **零配置存储** - 基于 SQLite 数据库，无需安装 MySQL/PostgreSQL
- 📚 **历史记录侧边栏** - 显示所有历史笔记，支持快速切换和内容预览
- ✏️ **自定义标题** - 为笔记添加易记的标题，支持中文/英文/Emoji
- 🗑️ **完整管理功能** - 支持重命名日期、修改标题、删除笔记
- 📊 **实时统计** - 实时显示字符数和行数统计
- 🎨 **现代化界面** - 渐变色背景、流畅动画、Material Design 风格
- 📱 **完美响应式** - 自适应手机、平板、电脑，任何设备都能流畅使用
- ⌨️ **快捷键支持** - `Ctrl+S` / `Cmd+S` 手动保存

### 🔐 安全特性
- 🔑 **API Token 认证** - 所有 API 接口都需要 Token 验证，防止未授权访问
- 🚦 **多级速率限制** - 每分钟/每小时/每天三级速率限制，防止暴力破解和 DDoS
- 🌐 **CORS 白名单** - 可配置允许访问的域名，生产环境必须指定
- 📝 **访问日志记录** - 记录所有 API 访问（IP、路径、状态、耗时），便于审计
- 📏 **内容大小限制** - 限制单个笔记（50000字符）和请求体（1MB）大小
- 🛡️ **IP 白名单（可选）** - 支持配置仅允许特定 IP 访问
- 📊 **分层日志系统** - 应用日志（`app.log`）和访问日志（`access.log`）分离
- 🔒 **上下文管理器** - 数据库连接自动管理，事务自动提交/回滚
- ✅ **装饰器验证链** - 认证 → IP检查 → 内容验证 → 速率限制 → 访问日志

### 🌟 技术亮点
- 🎯 **装饰器模式** - 多个安全装饰器组合，代码清晰易维护
- 🔄 **上下文管理器** - 自动管理数据库连接和事务
- 📦 **零依赖前端** - 纯原生 JavaScript，无需 React/Vue，加载极快
- 🚀 **高性能** - SQLite 索引优化，查询速度快
- 🐳 **容器化支持** - 完整的 Docker 和 Docker Compose 配置
- ♻️ **自动清理** - 空内容自动删除，保持数据库整洁

## 🚀 快速开始

### 方法 1：本地运行（5分钟）

1. **克隆项目**
```bash
git clone <your-repo-url>
cd upstatus
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置 API Token（重要）**
```bash
# 生成安全的 Token
python -c "import secrets; print(secrets.token_urlsafe(32))"

# 创建 .env 文件并配置 Token
cp .env.example .env
# 编辑 .env 文件，将 API_TOKEN 修改为上面生成的值
```

4. **运行应用**
```bash
python app.py
```

5. **首次访问配置**
- 访问 `http://localhost:5000`
- 系统会提示输入 API Token（即 .env 中配置的 API_TOKEN）
- Token 会保存在浏览器 localStorage 中，下次访问无需重新输入
- 如需更新 Token，点击页面右上角的 🔑 按钮

就是这么简单！数据库会在首次运行时自动创建。

### 方法 2：Docker 部署

```bash
# 1. 编辑 .env 文件配置 Token
cp .env.example .env
nano .env  # 修改 API_TOKEN

# 2. 使用 Docker Compose 启动
docker-compose up -d

# 3. 查看日志
docker-compose logs -f
```

## 🔧 环境变量配置

项目支持以下环境变量配置（在 `.env` 文件中设置）：

### 基础配置
| 变量名 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `DB_PATH` | SQLite 数据库文件路径 | `data/notes.db` | `data/notes.db` |
| `PORT` | Web 服务监听端口 | `5000` | `8080` |

### 🔐 安全配置（重要）
| 变量名 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `API_TOKEN` | **API 访问令牌（必须修改）** | `please-change-this...` | 使用 `secrets.token_urlsafe(32)` 生成 |
| `ALLOWED_ORIGINS` | CORS 允许的域名（逗号分隔） | `*` | `https://yourdomain.com,https://app.yourdomain.com` |
| `ALLOWED_IPS` | IP 白名单（逗号分隔，可选） | 空（不限制） | `192.168.1.100,10.0.0.1` |
| `RATE_LIMIT_PER_MINUTE` | 每分钟请求限制 | `60` | `100` |
| `RATE_LIMIT_PER_HOUR` | 每小时请求限制 | `200` | `500` |
| `RATE_LIMIT_PER_DAY` | 每日请求限制 | `1000` | `5000` |
| `MAX_CONTENT_LENGTH` | 请求体最大字节数 | `1048576` (1MB) | `2097152` (2MB) |
| `MAX_NOTE_LENGTH` | 单个笔记最大字符数 | `50000` | `100000` |
| `LOG_LEVEL` | 日志级别 | `INFO` | `DEBUG`, `WARNING`, `ERROR` |
| `LOG_DIR` | 日志目录 | `logs` | `logs` |

### 完整配置示例

```bash
# .env 文件示例

# === 数据库配置 ===
DB_PATH=data/notes.db
PORT=5000

# === 安全配置 ===

# API Token（必须修改！使用强随机字符串）
# 生成方法：python -c "import secrets; print(secrets.token_urlsafe(32))"
API_TOKEN=pxK8vQzP3mN9wE2rT5yH7jL6nB4cF1dG8sA0uI9oP3qR11

# CORS 允许的域名（多个用逗号分隔）
# 开发环境：使用 * 允许所有域名
# 生产环境：必须指定具体域名
ALLOWED_ORIGINS=*
# ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# 请求速率限制（每个 IP 地址）
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=200
RATE_LIMIT_PER_DAY=1000

# 内容大小限制（字节，默认 1MB）
MAX_CONTENT_LENGTH=1048576

# 单个笔记内容最大字符数
MAX_NOTE_LENGTH=50000

# IP 白名单（可选，留空则不限制）
# 多个 IP 用逗号分隔，例如：192.168.1.100,10.0.0.1
ALLOWED_IPS=

# 日志配置
LOG_LEVEL=INFO
LOG_DIR=logs
```

## 🔐 安全最佳实践

### 首次部署必做
1. ✅ **生成强随机 Token**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   将生成的 Token 配置到 `.env` 文件的 `API_TOKEN` 中

2. ✅ **配置 CORS 白名单**（生产环境）
   ```bash
   ALLOWED_ORIGINS=https://yourdomain.com
   ```
   不要在生产环境使用 `*`

3. ✅ **定期备份数据库文件**
   ```bash
   # 手动备份
   cp data/notes.db data/notes.db.backup.$(date +%Y%m%d)
   
   # 或使用 cron 定时备份
   0 2 * * * cp /path/to/data/notes.db /path/to/backup/notes.db.$(date +\%Y\%m\%d)
   ```

4. ✅ **不要将 `.env` 提交到 Git**
   ```bash
   # 已在 .gitignore 中配置
   echo ".env" >> .gitignore
   ```

### 可选安全加固
5. 🔒 **配置 IP 白名单**（适用于固定 IP 访问场景）
   ```bash
   ALLOWED_IPS=192.168.1.100,10.0.0.1
   ```

6. 🔒 **使用 HTTPS**（生产环境必须）
   - 使用 Nginx 反向代理并配置 SSL 证书
   - 或使用云平台的 HTTPS 终止功能

7. 🔒 **调整速率限制**（根据实际使用情况）
   ```bash
   # 更严格的限制
   RATE_LIMIT_PER_MINUTE=30
   RATE_LIMIT_PER_HOUR=100
   RATE_LIMIT_PER_DAY=500
   ```

### 安全日志审计
应用会生成两个日志文件：
- `logs/app.log` - 应用运行日志
- `logs/access.log` - API 访问日志（包含 IP、请求路径、响应状态等）

定期检查日志以发现异常访问：
```bash
# 查看最近的访问
tail -f logs/access.log

# 查看失败的认证尝试
grep "401" logs/access.log

# 查看速率限制触发
grep "429" logs/access.log
```

## 📋 技术栈与架构

### 后端技术
- **Web 框架**: Flask 3.0.0 

(轻量级 Python Web 框架)
- **数据库**: SQLite 3 (嵌入式数据库，无需额外服务)
- **WSGI 服务器**: Gunicorn 21.2.0 (生产环境推荐)
- **环境管理**: python-dotenv 1.0.0 (环境变量管理)

### 安全组件
- **速率限制**: Flask-Limiter 3.5.0 (防止 API 滥用)
- **跨域处理**: Flask-CORS 4.0.0 (CORS 策略管理)
- **认证机制**: 自定义 Token 认证装饰器
- **日志系统**: Python logging 模块 (分层日志记录)

### 前端技术
- **纯原生实现**: HTML5 + CSS3 + Vanilla JavaScript
- **无框架依赖**: 不依赖任何前端框架，加载速度快
- **响应式设计**: CSS Flexbox 布局，适配各种屏幕尺寸
- **本地存储**: localStorage 存储 Token，自动持久化

### 部署支持
- **容器化**: Docker + Docker Compose
- **云平台**: Heroku, Railway, Render, Zeabur
- **传统部署**: VPS + Nginx + Systemd
- **数据持久化**: 卷挂载确保数据安全

## 📂 项目结构

```
upstatus/
├── app.py                      # Flask 应用主文件（464行）
│   ├── 安全装饰器              # @require_auth, @check_ip_whitelist, @validate_content
│   ├── 数据库管理              # get_db() 上下文管理器, init_db()
│   ├── API 路由                # 5个 RESTful API 端点
│   └── 日志系统                # 应用日志 + 访问日志
├── index.html                  # 前端界面（1167行）
│   ├── Token 管理              # localStorage 自动保存/读取
│   ├── 自动保存逻辑            # 输入后立即保存
│   ├── 历史记录侧边栏          # 动态加载所有笔记
│   └── 模态框                  # 重命名、删除确认
├── requirements.txt            # Python 依赖（5个包）
├── .env                        # 环境变量配置（不提交到 Git）
├── .env.example                # 环境变量模板
├── .gitignore                  # Git 忽略文件
├── .dockerignore               # Docker 忽略文件
├── Dockerfile                  # Docker 镜像配置
├── docker-compose.yml          # Docker Compose 配置
├── Procfile                    # Heroku/PaaS 部署配置
├── README.md                   # 项目说明（本文件）
├── data/
│   └── notes.db                # SQLite 数据库（首次运行自动创建）
└── logs/                       # 日志目录
    ├── app.log                 # 应用日志（启动、错误等）
    └── access.log              # 访问日志（IP、路径、耗时等）
```

## 🔄 数据库设计

应用使用 SQLite 数据库存储笔记，数据表结构如下：

```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 主键 ID
    date TEXT NOT NULL UNIQUE,            -- 日期（YYYY-MM-DD 格式）
    content TEXT NOT NULL,                 -- 笔记内容（支持大文本）
    custom_title TEXT,                     -- 自定义标题（可选）
    last_updated TEXT NOT NULL,            -- 最后更新时间（ISO 8601 格式）
    created_at TEXT NOT NULL               -- 创建时间（ISO 8601 格式）
);

CREATE INDEX idx_date ON notes(date);     -- 日期索引，优化查询性能
```

### 数据库特点

**设计优势**：
- ✅ **自动初始化** - 首次运行时自动创建表结构，无需手动建表
- ✅ **日期唯一约束** - 每个日期只能有一条记录，避免重复
- ✅ **索引优化** - 日期字段建立索引，查询速度快
- ✅ **空内容自动删除** - 保存时若内容为空则自动删除记录
- ✅ **事务管理** - 使用上下文管理器，自动提交/回滚
- ✅ **字典访问** - `row_factory = sqlite3.Row`，结果可像字典一样访问

### 数据库上下文管理器实现

```python
@contextmanager
def get_db():
    """获取数据库连接的上下文管理器"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 使结果可以像字典一样访问
    try:
        yield conn
        conn.commit()  # 自动提交
    except Exception:
        conn.rollback()  # 出错自动回滚
        raise
    finally:
        conn.close()  # 自动关闭连接
```

### 数据示例

```json
{
  "id": 1,
  "date": "2024-01-01",
  "content": "今天学习了 Flask 框架...",
  "custom_title": "Flask 学习笔记",
  "last_updated": "2024-01-01T15:30:00",
  "created_at": "2024-01-01T10:00:00"
}
```

## 📝 API 接口文档

### ⚠️ 认证要求
所有 API 端点都需要在请求头中包含 Token：
```http
X-API-Token: your-api-token-here
```

前端会自动处理 Token，无需手动添加。

### 1. 获取笔记
```http
GET /api/note?date=2024-01-01
X-API-Token: your-api-token-here
```
**速率限制**: 60次/分钟

**响应示例**:
```json
{
  "content": "今天的笔记内容",
  "last_updated": "2024-01-01T12:00:00",
  "date": "2024-01-01",
  "custom_title": "自定义标题"
}
```

### 2. 保存笔记
```http
POST /api/note
Content-Type: application/json
X-API-Token: your-api-token-here

{
  "date": "2024-01-01",
  "content": "今天的笔记内容"
}
```

**速率限制**: 30次/分钟

**响应示例**:
```json
{
  "success": true,
  "message": "保存成功",
  "last_updated": "2024-01-01T12:00:00",
  "date": "2024-01-01"
}
```

### 3. 删除笔记
```http
DELETE /api/note?date=2024-01-01
X-API-Token: your-api-token-here
```

**速率限制**: 10次/分钟

**响应示例**:
```json
{
  "success": true,
  "message": "记录已删除",
  "date": "2024-01-01"
}
```

### 4. 重命名笔记
```http
POST /api/note/rename
Content-Type: application/json
X-API-Token: your-api-token-here

{
  "old_date": "2024-01-01",
  "new_date": "2024-01-02",
  "custom_title": "自定义标题"
}
```

**速率限制**: 20次/分钟

**响应示例**:
```json
{
  "success": true,
  "message": "重命名成功",
  "old_date": "2024-01-01",
  "new_date": "2024-01-02"
}
```

### 5. 获取所有日期
```http
GET /api/dates
X-API-Token: your-api-token-here
```

**速率限制**: 60次/分钟

**响应示例**:
```json
{
  "dates": [
    {
      "date": "2024-01-01",
      "custom_title": "自定义标题",
      "last_updated": "2024-01-01T12:00:00",
      "preview": "笔记内容预览前50个字符..."
    }
  ],
  "count": 1
}
```

### 错误响应

**401 未授权** - Token 缺失或无效:
```json
{
  "error": "缺少认证 Token"
}
```

**403 禁止访问** - IP 不在白名单:
```json
{
  "error": "访问被拒绝：IP 不在白名单中"
}
```

**413 内容过大**:
```json
{
  "error": "内容过长，最大允许 50000 字符"
}
```

**429 请求过于频繁**:
```json
{
  "error": "Too Many Requests"
}
```

## 🛡️ 安全机制详解

### 装饰器执行顺序
```python
@app.route('/api/note', methods=['POST'])
@require_auth           # 1️⃣ 验证 Token
@check_ip_whitelist     # 2️⃣ 检查 IP 白名单
@validate_content       # 3️⃣ 验证内容长度
@limiter.limit("30 per minute")  # 4️⃣ 速率限制
@log_access             # 5️⃣ 记录访问日志
def save_note():
    # 业务逻辑
```

### Token 认证流程
1. 前端从 localStorage 读取 Token
2. 每个 API 请求自动添加 `X-API-Token` 头部
3. 后端 `@require_auth` 装饰器验证 Token
4. Token 无效返回 401，前端自动清除并要求重新输入

### 速率限制策略
- **读取操作** (GET): 60次/分钟
- **写入操作** (POST): 30次/分钟
- **删除操作** (DELETE): 10次/分钟
- **全局限制**: 200次/小时，1000次/天

## 🌐 部署指南

### Docker 部署（推荐）

**优点**: 环境隔离、易于迁移、自动重启

```bash
# 1. 配置环境变量
cp .env.example .env
nano .env  # 修改 API_TOKEN

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 停止服务
docker-compose down
```

**数据持久化**: 数据通过卷挂载到 `./data` 目录，容器重启后数据不会丢失。

### VPS 部署（生产环境）

```bash
# 1. 克隆代码
git clone <your-repo-url>
cd upstatus

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
nano .env  # 修改配置

# 4. 使用 Gunicorn 运行
gunicorn --bind 0.0.0.0:5000 --workers 2 --threads 4 app:app

# 5. 配置 Nginx 反向代理（推荐）
# /etc/nginx/sites-available/upstatus
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

# 6. 配置 systemd 服务（开机自启）
# /etc/systemd/system/upstatus.service
[Unit]
Description=Upstatus Note App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/upstatus
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 2 app:app
Restart=always

[Install]
WantedBy=multi-user.target

# 启动服务
sudo systemctl enable upstatus
sudo systemctl start upstatus
```

### Heroku / Railway / Render 部署

1. 连接 GitHub 仓库
2. 配置环境变量（在平台控制台设置）
   - `API_TOKEN`: 你的安全 Token
   - `ALLOWED_ORIGINS`: 你的域名
3. 点击部署

> **注意**: 确保平台支持持久化存储，否则数据会在容器重启后丢失。

## 🐛 故障排查

### 应用无法启动

**症状**: `python app.py` 报错

**检查项**:
1. Python 版本是否 >= 3.11
2. 依赖是否正确安装
3. 端口是否被占用

**解决方案**:
```bash
# 检查 Python 版本
python --version

# 重新安装依赖
pip install -r requirements.txt

# 更换端口
export PORT=8080
python app.py
```

### Token 认证失败

**症状**: 前端提示 "Token 无效或已过期"

**检查项**:
1. `.env` 

文件中的 `API_TOKEN` 是否正确配置
2. 浏览器中存储的 Token 是否与服务器配置一致

**解决方案**:
```bash
# 1. 检查服务器配置
cat .env | grep API_TOKEN

# 2. 清除浏览器 Token
# 点击页面右上角 🔑 按钮，输入新 Token

# 3. 或清除浏览器 localStorage
# 打开开发者工具 > Application > Local Storage > 删除 upstatus_api_token
```

### 速率限制触发

**症状**: 提示 "请求过于频繁"

**检查项**:
- 是否在短时间内发送了大量请求
- 速率限制配置是否过于严格

**解决方案**:
```bash
# 调整速率限制（.env 文件）
RATE_LIMIT_PER_MINUTE=120  # 增加到 120 次/分钟
RATE_LIMIT_PER_HOUR=500    # 增加到 500 次/小时

# 重启应用
```

### 数据库错误

**症状**: "数据库文件损坏" 或写入失败

**检查项**:
1. 数据库文件所在目录是否有写权限
2. 磁盘空间是否充足
3. 数据库文件是否损坏

**解决方案**:
```bash
# 检查权限
ls -la data/notes.db

# 修复权限
chmod 666 data/notes.db
chmod 777 data/

# 如果数据库损坏，备份后重建
cp data/notes.db data/notes.db.broken
rm data/notes.db
python app.py  # 会自动创建新数据库
```

### Docker 容器数据丢失

**症状**: 容器重启后数据消失

**原因**: 未正确配置卷挂载

**解决方案**:
```bash
# 确保 docker-compose.yml 中有卷挂载
volumes:
  - ./data:/app/data

# 停止但不删除卷
docker-compose down

# 重新启动
docker-compose up -d

# 避免使用（会删除数据）
docker-compose down -v
```

### 日志中出现 emoji 编码错误

**症状**: Windows 环境下日志显示 `UnicodeEncodeError`

**原因**: Windows 终端默认使用 GBK 编码

**解决方案**:
```bash
# 方法 1: 切换终端编码
chcp 65001  # 切换到 UTF-8

# 方法 2: 修改日志级别（.env 文件）
LOG_LEVEL=WARNING  # 减少日志输出

# 不影响功能，可忽略
```

## 📊 使用技巧与最佳实践

### ⌨️ 快捷键
- `Ctrl+S` / `Cmd+S` - 手动保存当前笔记
- 浏览器快捷键可能冲突，建议使用鼠标操作历史记录

### 💡 使用技巧

**编辑器功能**：
- ✅ **自动保存** - 输入后立即自动保存，无需手动操作
- ✅ **空内容处理** - 空内容的笔记会自动删除，保持数据库整洁
- ✅ **快速切换** - 点击历史记录中的日期快速切换笔记
- ✅ **内容预览** - 历史列表显示前 50 个字符的内容预览
- ✅ **实时统计** - 实时显示字符数和行数

**Token 管理**：
- ✅ Token 会自动保存在浏览器 localStorage 中
- ✅ 换设备或清除浏览器数据需要重新输入
- ✅ 点击页面右上角 🔑 按钮可更新 Token
- ✅ Token 验证失败会自动清除并提示重新输入

**历史记录操作**：
- ✏️ **重命名** - 修改日期或添加自定义标题
- 🗑️ **删除** - 删除不需要的笔记（不可恢复）
- 📅 **日期选择** - 使用日期选择器快速跳转
- 📌 **自定义标题** - 为笔记添加易记的标题

### 🔄 数据备份策略

**手动备份**：
```bash
# 备份数据库文件
cp data/notes.db backups/notes.db.$(date +%Y%m%d)

# 压缩备份（节省空间）
tar -czf backups/notes-backup-$(date +%Y%m%d).tar.gz data/notes.db

# 远程备份（推荐）
scp data/notes.db user@backup-server:/backup/path/
```

**自动定时备份**：
```bash
# 添加到 crontab（每天凌晨2点备份）
0 2 * * * cp /path/to/data/notes.db /path/to/backup/notes.db.$(date +\%Y\%m\%d)

# 自动清理旧备份（保留30天）
0 3 * * * find /path/to/backup/ -name "notes.db.*" -mtime +30 -delete
```

**Docker 备份**：
```bash
# 备份 Docker 卷中的数据
docker cp upstatus:/app/data/notes.db ./backup/notes.db.$(date +%Y%m%d)

# 或直接备份挂载目录
tar -czf backup-$(date +%Y%m%d).tar.gz data/
```

### 📈 性能优化建议

1. **定期清理旧笔记** - 删除不需要的历史记录
2. **控制笔记大小** - 单个笔记建议不超过 10000 字符
3. **使用 Gunicorn** - 生产环境使用 Gunicorn 代替 Flask 开发服务器
4. **启用 Nginx 缓存** - 静态文件（index.html）可以缓存
5. **监控日志大小** - 定期清理或轮转日志文件

## 🔍 代码结构说明

### 后端核心代码（app.py）

**安全装饰器链**：
```python
# 认证装饰器
@require_auth           # 验证 API Token
@check_ip_whitelist     # 检查 IP 白名单（可选）
@validate_content       # 验证内容长度
@limiter.limit()        # 速率限制
@log_access             # 记录访问日志
```

**数据库操作**：
```python
# 上下文管理器自动处理连接
with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes WHERE date = ?', (date,))
    # 自动提交/回滚/关闭
```

**API 端点**：
- `GET /` - 返回前端页面
- `GET /api/note?date=xxx` - 获取笔记
- `POST /api/note` - 保存笔记
- `DELETE /api/note?date=xxx` - 删除笔记
- `POST /api/note/rename` - 重命名笔记
- `GET /api/dates` - 获取所有日期列表

### 前端核心代码（index.html）

**Token 管理**：
```javascript
// 从 localStorage 获取 Token
const API_TOKEN = getApiToken();

// API 请求自动添加 Token
options.headers['X-API-Token'] = API_TOKEN;
```

**自动保存机制**：
```javascript
// 输入时触发
textarea.addEventListener('input', function() {
    hasUnsavedChanges = true;
    scheduleAutoSave();  // 延迟0秒立即保存
});
```

**历史记录加载**：
```javascript
// 页面加载时自动获取
async function loadHistory() {
    const response = await apiRequest('/api/dates');
    // 动态生成历史列表
}
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程
1. Fork 本仓库
2. 创建特性分支: `git checkout -b feature/amazing-feature`
3. 提交更改: `git commit -m 'Add amazing feature'`
4. 推送到分支: `git push origin feature/amazing-feature`
5. 提交 Pull Request

### 代码规范
- **Python**: 遵循 PEP 8 规范
- **JavaScript**: 使用 ES6+ 语法
- **注释**: 关键逻辑添加中文注释
- **测试**: 确保代码通过基本测试

### 提交信息格式
```
<type>: <subject>

<body>

<footer>
```

类型（type）：
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具链更新

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Flask](https://flask.palletsprojects.com/) - 轻量级 Python Web 框架
- [SQLite](https://www.sqlite.org/) - 轻量级嵌入式数据库
- [Gunicorn](https://gunicorn.org/) - Python WSGI HTTP 服务器
- [Flask-CORS](https://flask-cors.readthedocs.io/) - 处理跨域请求
- [Flask-Limiter](https://flask-limiter.readthedocs.io/) - API 速率限制

## 📮 反馈与支持

如有问题或建议，请：
- 提交 [GitHub Issue](https://github.com/your-username/upstatus/issues)
- 查看日志文件排查问题: `logs/app.log` 和 `logs/access.log`
- 阅读本文档的故障排查章节

## 🎯 未来计划

- [ ] 支持 Markdown 渲染
- [ ] 添加全文搜索功能
- [ ] 支持笔记分类/标签
- [ ] 导出笔记（PDF/Markdown）
- [ ] 多用户支持
- [ ] 移动端 App
- [ ] 数据加密存储
- [ ] WebSocket 实时同步

---

**享受使用每日记事本！** 📝✨🔐

> 💡 **提示**: 如果觉得这个项目有用，请给个 ⭐ Star 支持一下！
