# 📝 每日记事本 - 跨设备共享

一个简洁、优雅的在线记事本应用，支持按日期记录、自动保存、跨设备同步。基于 Flask + Supabase 构建。

## ✨ 特性

- 📅 **按日期记录** - 每天的笔记独立存储，方便回顾
- 💾 **自动保存** - 3秒无操作后自动保存，不用担心丢失内容
- 🔄 **跨设备同步** - 基于 Supabase 云数据库，多设备实时同步
- 📚 **历史记录** - 右侧侧边栏显示所有历史笔记，快速切换
- ✏️ **自定义标题** - 为笔记添加易记的标题
- 🗑️ **管理功能** - 重命名、删除笔记
- 📊 **实时统计** - 显示字符数和行数
- 🎨 **现代界面** - 简洁美观的用户界面
- 📱 **响应式设计** - 完美支持手机、平板、电脑

## 🚀 快速开始

### 方法 1：本地运行

1. **克隆项目**
```bash
git clone <your-repo-url>
cd upstatus
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置 Supabase**

参考 [QUICKSTART.md](./QUICKSTART.md) 完成 Supabase 设置。

创建 `.env` 文件：
```bash
cp .env.example .env
```

编辑 `.env` 并填入您的 Supabase 连接信息：
```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key
PORT=5000
```

4. **创建数据表**

在 Supabase SQL Editor 中执行 `setup_supabase.sql` 文件。

5. **运行应用**
```bash
python app.py
```

访问 `http://localhost:5000` 即可使用。

### 方法 2：Docker 部署

```bash
# 1. 创建 .env 文件
cp .env.example .env

# 2. 编辑 .env 填入 Supabase 信息

# 3. 使用 Docker Compose 启动
docker-compose up -d
```

## 📖 文档

- [快速开始指南](./QUICKSTART.md) - 5分钟快速部署
- [Supabase 设置详解](./SUPABASE_SETUP.md) - 完整的数据库配置说明

## 🔧 技术栈

- **后端**: Flask (Python)
- **数据库**: Supabase (PostgreSQL)
- **前端**: 原生 HTML/CSS/JavaScript
- **部署**: Docker, Heroku, Vercel, Railway

## 📋 项目结构

```
upstatus/
├── app.py                  # Flask 应用主文件
├── index.html              # 前端界面
├── requirements.txt        # Python 依赖
├── setup_supabase.sql      # 数据库建表 SQL
├── .env.example            # 环境变量模板
├── .gitignore              # Git 忽略文件
├── Dockerfile              # Docker 配置
├── docker-compose.yml      # Docker Compose 配置
├── Procfile                # Heroku 部署配置
├── README.md               # 项目说明
├── QUICKSTART.md           # 快速开始指南
└── SUPABASE_SETUP.md       # Supabase 设置指南
```

## 🔄 最近更新 (v2.0)

### ✅ 重大改进

1. **存储系统升级**
   - ❌ 移除本地文件存储 (`data/notes_data.json`)
   - ✅ 迁移到 Supabase 云数据库
   - ✅ 支持真正的跨设备同步

2. **Bug 修复**
   - ✅ 修复了自动保存后历史列表不更新的问题
   - ✅ 添加延迟刷新机制，确保数据同步

3. **文档完善**
   - ✅ 新增快速开始指南
   - ✅ 新增 Supabase 详细配置文档
   - ✅ 添加故障排查指南

## 🌐 部署选项

### Heroku

```bash
heroku create your-app-name
heroku config:set SUPABASE_URL=your-url
heroku config:set SUPABASE_KEY=your-key
git push heroku main
```

### Vercel

使用 Vercel CLI 或 在 Dashboard 中连接 GitHub 仓库，并设置环境变量。

### Railway

连接 GitHub 仓库，添加环境变量即可自动部署。

详细部署说明请参考 [QUICKSTART.md](./QUICKSTART.md)。

## 🔒 安全建议

1. ✅ 使用 `anon` key 而非 `service_role` key
2. ✅ 不要将 `.env` 文件提交到 Git
3. ✅ 在 Supabase 中配置 Row Level Security (RLS)
4. ✅ 定期轮换 API keys
5. ✅ 限制 API 请求速率

## 🐛 故障排查

### 无法连接到 Supabase

- 检查 `SUPABASE_URL` 和 `SUPABASE_KEY` 是否正确
- 确认 Supabase 项目状态正常
- 检查网络连接

### 历史记录不显示

- 确认已执行建表 SQL
- 检查浏览器控制台是否有错误
- 至少保存一条笔记

### 自动保存不工作

- 检查浏览器控制台的网络请求
- 确认服务器正在运行
- 查看服务器日志

更多问题请参考 [QUICKSTART.md](./QUICKSTART.md#-故障排查)。

## 📝 使用提示

- **快捷键**: `Ctrl+S` / `Cmd+S` 手动保存
- **自动保存**: 停止输入 3 秒后自动保存
- **空内容处理**: 空内容的笔记会自动删除
- **日期切换**: 点击历史记录中的日期快速切换

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [Flask](https://flask.palletsprojects.com/) - 轻量级 Web 框架
- [Supabase](https://supabase.com/) - 开源的 Firebase 替代品
- [Font Awesome](https://fontawesome.com/) - 图标库

---

**享受使用每日记事本！** 📝✨

如有问题，请查看 [QUICKSTART.md](./QUICKSTART.md) 或提交 Issue。