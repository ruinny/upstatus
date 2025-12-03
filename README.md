# 每日记事本 - 跨设备共享工具

一个功能强大的在线记事本应用，支持按日期组织笔记、跨设备访问和数据持久化。

## 功能特点

✨ **核心功能**
- 📅 按日期组织笔记内容
- 📝 实时自动保存（3秒防抖）
- 🔄 跨设备同步访问
- 📚 历史记录浏览
- ✏️ 记录重命名（支持自定义标题）
- 🗑️ 删除记录功能
- ⌨️ 支持 Ctrl+S 快捷键保存
- 📊 实时字符和行数统计
- 📱 完美适配移动端
- 💾 数据持久化存储（JSON文件）

## 本地运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动

## Docker 部署

### 使用 Docker Compose（推荐）

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 使用 Docker 命令

```bash
# 构建镜像
docker build -t upstatus .

# 运行容器（数据持久化）
docker run -d \
  --name upstatus \
  -p 5000:5000 \
  -v $(pwd)/notes_data.json:/app/notes_data.json \
  --restart unless-stopped \
  upstatus

# 查看日志
docker logs -f upstatus

# 停止容器
docker stop upstatus

# 删除容器
docker rm upstatus
```

访问 `http://localhost:5000` 即可使用应用。

## 部署到 Zeabur

### 方法一：通过 Git 部署

1. 将代码推送到 GitHub 仓库
2. 登录 [Zeabur](https://zeabur.com)
3. 创建新项目并连接你的 GitHub 仓库
4. Zeabur 会自动检测 Python 项目并部署

### 方法二：通过 Zeabur CLI

```bash
# 安装 Zeabur CLI
npm install -g @zeabur/cli

# 登录
zeabur auth login

# 部署
zeabur deploy
```

### 环境变量

无需额外配置环境变量，应用开箱即用。

## 技术栈

- **后端**: Flask (Python)
- **前端**: HTML, CSS, JavaScript
- **部署**: Zeabur / Gunicorn

## 文件结构

```
.
├── app.py              # Flask 后端应用
├── index.html          # 前端界面
├── requirements.txt    # Python 依赖
├── Dockerfile          # Docker 镜像配置
├── docker-compose.yml  # Docker Compose 配置
├── .dockerignore       # Docker 忽略文件
├── Procfile           # Zeabur 部署配置
├── notes_data.json    # 数据存储文件（自动生成）
└── README.md          # 项目说明
```

## API 接口

### GET /api/note
获取指定日期的笔记内容
- 参数: `date` (可选，默认当天)
- 返回: JSON 格式的笔记内容

### POST /api/note
保存笔记内容
```json
{
  "content": "笔记内容",
  "date": "2024-12-03"
}
```

### DELETE /api/note
删除指定日期的记录
- 参数: `date` (必需)

### POST /api/note/rename
重命名记录（修改日期或添加自定义标题）
```json
{
  "old_date": "2024-12-03",
  "new_date": "2024-12-04",
  "custom_title": "重要笔记"
}
```

### GET /api/dates
获取所有有记录的日期列表
- 返回: 按日期倒序排列的记录列表

## 注意事项

💡 **使用提示**：
- 数据存储在 `notes_data.json` 文件中，支持持久化
- Docker 部署时建议挂载数据文件以确保数据不丢失
- 支持移动端访问，响应式设计适配各种屏幕
- 删除操作不可撤销，请谨慎操作
- 自定义标题可帮助快速识别重要记录

## 使用场景

- 💻 在不同电脑间快速共享代码片段
- 📱 手机和电脑间传输文本
- 🔗 团队内临时共享配置信息
- 📄 按日期记录每日工作笔记
- 📝 保存重要的临时信息
- 🎯 项目进度追踪和备忘

## 移动端优化

本应用已针对移动端进行优化：
- 📱 自适应布局，完美适配手机屏幕
- 👆 触摸友好的操作按钮
- 📏 合理的字体和间距设计
- 🎨 清晰易读的界面元素

## License

MIT