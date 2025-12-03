# 📝 每日记事本

一个简洁、优雅的在线记事本应用，支持按日期记录、自动保存。基于 Flask + SQLite 构建，开箱即用。

## ✨ 特性

- 📅 **按日期记录** - 每天的笔记独立存储，方便回顾
- 💾 **自动保存** - 3秒无操作后自动保存，不用担心丢失内容
- 🗄️ **本地存储** - 基于 SQLite 数据库，无需配置，开箱即用
- 📚 **历史记录** - 右侧侧边栏显示所有历史笔记，快速切换
- ✏️ **自定义标题** - 为笔记添加易记的标题
- 🗑️ **管理功能** - 重命名、删除笔记
- 📊 **实时统计** - 显示字符数和行数
- 🎨 **现代界面** - 简洁美观的用户界面
- 📱 **响应式设计** - 完美支持手机、平板、电脑
- 🚀 **零配置启动** - 不需要配置数据库，直接运行即可

## 🚀 快速开始

### 方法 1：本地运行（推荐）

1. **克隆项目**
```bash
git clone <your-repo-url>
cd upstatus
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **运行应用**
```bash
python app.py
```

就是这么简单！访问 `http://localhost:5000` 即可使用。

数据库会在首次运行时自动创建在 `notes.db` 文件中。

### 方法 2：自定义配置（可选）

如果需要自定义数据库路径或端口：

```bash
# 1. 复制配置模板
cp .env.example .env

# 2. 编辑 .env 文件
# DB_PATH=data/notes.db  # 自定义数据库路径
# PORT=8080              # 自定义端口

# 3. 运行应用
python app.py
```

### 方法 3：Docker 部署

```bash
# 使用 Docker Compose 启动
docker-compose up -d

# 数据会持久化在本地挂载的卷中
```

## 📖 环境变量说明

项目支持以下环境变量（均为可选）：

| 变量名 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `DB_PATH` | SQLite 数据库文件路径 | `notes.db` | `data/notes.db` |
| `PORT` | Web 服务监听端口 | `5000` | `8080` |

**配置示例：**

```bash
# 创建 .env 文件
DB_PATH=data/notes.db
PORT=5000
```

## 🔧 技术栈

- **后端**: Flask (Python 3.11+)
- **数据库**: SQLite 3
- **前端**: 原生 HTML/CSS/JavaScript
- **WSGI**: Gunicorn
- **部署**: Docker, 任何支持 Python 的平台

## 📋 项目结构

```
upstatus/
├── app.py                  # Flask 应用主文件（包含所有 API 和数据库逻辑）
├── index.html              # 前端界面
├── requirements.txt        # Python 依赖
├── .env.example            # 环境变量模板
├── .gitignore              # Git 忽略文件
├── .dockerignore           # Docker 忽略文件
├── Dockerfile              # Docker 镜像配置
├── docker-compose.yml      # Docker Compose 配置
├── Procfile                # Heroku/PaaS 部署配置
├── README.md               # 项目说明（本文件）
├── notes.db                # SQLite 数据库（首次运行自动创建）
└── data/                   # 数据目录（可选，用于存放数据库文件）
```

## 🔄 数据库设计

应用使用 SQLite 数据库存储笔记，数据表结构如下：

```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,           -- 日期（YYYY-MM-DD）
    content TEXT NOT NULL,                -- 笔记内容
    custom_title TEXT,                    -- 自定义标题
    last_updated TEXT NOT NULL,           -- 最后更新时间
    created_at TEXT NOT NULL              -- 创建时间
);

CREATE INDEX idx_date ON notes(date);    -- 日期索引
```

**特点：**
- 自动初始化：首次运行时自动创建表结构
- 日期唯一：每个日期只能有一条记录
- 索引优化：按日期查询性能优秀
- 自动管理：空内容自动删除

## 🌐 部署选项

### Docker 部署（推荐）

```bash
# 1. 使用 docker-compose
docker-compose up -d

# 2. 查看日志
docker-compose logs -f

# 3. 停止服务
docker-compose down
```

数据会通过 Docker 卷持久化，容器重启后数据不会丢失。

### Heroku 部署

```bash
# 1. 创建应用
heroku create your-app-name

# 2. 推送代码
git push heroku main

# 3. 访问应用
heroku open
```

> **注意**: 免费 Heroku dyno 会休眠，且文件系统是临时的。建议使用付费版本或其他平台。

### Railway / Render 部署

1. 连接 GitHub 仓库
2. 自动检测 Python 应用
3. 点击部署

> **注意**: 确保平台支持持久化存储，否则数据会在容器重启后丢失。

### VPS 部署

```bash
# 1. 克隆代码
git clone <your-repo-url>
cd upstatus

# 2. 安装依赖
pip install -r requirements.txt

# 3. 使用 systemd 或 supervisor 管理进程
# 或使用 gunicorn 直接运行
gunicorn --bind 0.0.0.0:5000 --workers 2 --threads 4 app:app
```

## 🔒 数据持久化说明

### 本地运行

数据存储在 SQLite 数据库文件中（默认 `notes.db`），只要文件不丢失，数据就会保留。

**建议：**
- 定期备份数据库文件
- 使用版本控制系统（Git）时，将 `*.db` 添加到 `.gitignore`

### Docker 部署

需要正确配置卷挂载以确保数据持久化。建议的 `docker-compose.yml` 配置：

```yaml
version: '3.8'
services:
  upstatus:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data        # 挂载数据目录
    environment:
      - DB_PATH=/app/data/notes.db
      - PORT=5000
    restart: unless-stopped
```

### 云平台部署

大多数云平台的容器文件系统是临时的，需要：
1. 使用平台提供的持久化卷
2. 或配置外部存储（如 AWS EFS、Azure Files）
3. 或定期备份数据库文件到对象存储

## 🐛 故障排查

### 应用无法启动

**检查项：**
- Python 版本是否 >= 3.11
- 依赖是否正确安装：`pip install -r requirements.txt`
- 端口 5000 是否被占用

**解决方案：**
```bash
# 查看详细错误信息
python app.py

# 或更换端口
export PORT=8080
python app.py
```

### 数据库错误

**检查项：**
- 数据库文件所在目录是否有写权限
- 数据库文件是否损坏

**解决方案：**
```bash
# 检查权限
ls -la notes.db

# 如果数据库损坏，删除后重新创建
rm notes.db
python app.py
```

### 历史记录不显示

**原因：**
- 数据库中没有记录
- 前端 JavaScript 错误

**解决方案：**
- 先保存至少一条笔记
- 打开浏览器开发者工具（F12）查看控制台错误
- 检查网络请求是否正常

### Docker 容器数据丢失

**原因：**
- 未正确配置卷挂载
- 容器被删除而非停止

**解决方案：**
```bash
# 确保使用卷挂载
docker-compose down  # 停止但不删除卷
docker-compose up -d # 重新启动

# 避免使用
docker-compose down -v  # 这会删除卷和数据
```

## 📝 API 接口文档

### 获取笔记
```http
GET /api/note?date=2024-01-01
```

### 保存笔记
```http
POST /api/note
Content-Type: application/json

{
  "date": "2024-01-01",
  "content": "今天的笔记内容"
}
```

### 删除笔记
```http
DELETE /api/note?date=2024-01-01
```

### 重命名笔记
```http
POST /api/note/rename
Content-Type: application/json

{
  "old_date": "2024-01-01",
  "new_date": "2024-01-02",
  "custom_title": "自定义标题"
}
```

### 获取所有日期
```http
GET /api/dates
```

## 📊 使用提示

- **快捷键**: `Ctrl+S` / `Cmd+S` 手动保存
- **自动保存**: 停止输入 3 秒后自动保存
- **空内容处理**: 空内容的笔记会自动删除
- **日期切换**: 点击历史记录中的日期快速切换
- **数据备份**: 定期备份 `notes.db` 文件
- **内容预览**: 历史列表显示前 50 个字符的内容预览

## 🔐 安全建议

1. ✅ 如果部署到公网，建议添加身份验证
2. ✅ 不要将包含敏感数据的 `.env` 文件提交到 Git
3. ✅ 定期备份数据库文件
4. ✅ 使用 HTTPS 保护数据传输
5. ✅ 限制 API 请求速率防止滥用

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**开发流程：**
1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add amazing feature'`
4. 推送到分支：`git push origin feature/amazing-feature`
5. 提交 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Flask](https://flask.palletsprojects.com/) - 轻量级 Python Web 框架
- [SQLite](https://www.sqlite.org/) - 轻量级嵌入式数据库
- [Gunicorn](https://gunicorn.org/) - Python WSGI HTTP 服务器
- [Flask-CORS](https://flask-cors.readthedocs.io/) - 处理跨域请求

## 📮 联系方式

如有问题或建议，请：
- 提交 [GitHub Issue](https://github.com/your-username/upstatus/issues)
- 发送邮件至：your-email@example.com

---

**享受使用每日记事本！** 📝✨