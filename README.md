# 临时记事本 - 跨设备共享工具

一个简单实用的在线记事本应用，支持跨设备访问和数据共享。

## 功能特点

✨ **核心功能**
- 📝 实时保存和加载笔记内容
- 🔄 跨设备同步访问
- 📋 一键复制到剪贴板
- 🗑️ 快速清空内容
- ⌨️ 支持 Ctrl+S 快捷键保存
- ⏰ 每30秒自动保存
- 📊 实时字符计数

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
├── Procfile           # Zeabur 部署配置
└── README.md          # 项目说明
```

## API 接口

### GET /api/note
获取当前保存的笔记内容

### POST /api/note
保存笔记内容
```json
{
  "content": "笔记内容"
}
```

### DELETE /api/note
清空笔记内容

## 注意事项

⚠️ **重要提示**：
- 当前版本使用内存存储，服务器重启后数据会丢失
- 建议用于临时数据共享，不要存储重要信息
- 如需持久化存储，可以集成数据库（如 PostgreSQL、Redis 等）

## 使用场景

- 💻 在不同电脑间快速共享代码片段
- 📱 手机和电脑间传输文本
- 🔗 团队内临时共享配置信息
- 📄 快速记录临时笔记

## License

MIT