# 快速开始指南

## 🚀 快速部署步骤

### 1. 准备 Supabase 数据库

1. 访问 [Supabase](https://app.supabase.com/) 并登录
2. 创建新项目或选择现有项目
3. 进入 SQL Editor，执行以下 SQL：

```sql
CREATE TABLE IF NOT EXISTS notes (
  id SERIAL PRIMARY KEY,
  date TEXT UNIQUE NOT NULL,
  content TEXT,
  custom_title TEXT,
  last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_notes_date ON notes(date);
CREATE INDEX IF NOT EXISTS idx_notes_last_updated ON notes(last_updated DESC);
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，并填入您的 Supabase 连接信息：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key
PORT=5000
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

---

## 📋 功能说明

### ✅ 已实现的功能

1. **按日期记录笔记** - 每天的笔记独立存储
2. **自动保存** - 3秒无操作后自动保存
3. **历史记录** - 右侧显示所有历史笔记
4. **自定义标题** - 为笔记添加易记的标题
5. **重命名和删除** - 管理您的笔记
6. **跨设备同步** - 基于 Supabase 云数据库
7. **实时字符统计** - 显示字符数和行数

### 🔧 修复的问题

1. **存储系统迁移** - 从本地文件存储改为 Supabase 云数据库
2. **历史列表显示** - 修复了自动保存后历史列表不更新的问题
   - 添加了100ms延迟确保数据库已更新
   - 确保每次保存后都会刷新历史记录

---

## 🔑 获取 Supabase 密钥

### 方法 1：从 Dashboard 获取

1. 登录 [Supabase Dashboard](https://app.supabase.com/)
2. 选择您的项目
3. 点击左侧 **Settings** ⚙️
4. 选择 **API** 选项卡
5. 复制以下信息：
   - **Project URL** → 这是您的 `SUPABASE_URL`
   - **anon public** key → 这是您的 `SUPABASE_KEY`

### 方法 2：使用 Service Role Key（可选，完全访问权限）

如果需要完全访问权限（绕过 RLS），可以使用 `service_role` key 替代 `anon` key。

⚠️ **警告**：service_role key 拥有完全访问权限，请勿在客户端代码中使用！

---

## 🐳 Docker 部署

### 使用 Docker Compose

```bash
# 1. 创建 .env 文件并配置环境变量
cp .env.example .env

# 2. 启动容器
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 停止容器
docker-compose down
```

### 使用 Docker

```bash
# 构建镜像
docker build -t upstatus .

# 运行容器
docker run -d \
  -p 5000:5000 \
  -e SUPABASE_URL=your-url \
  -e SUPABASE_KEY=your-key \
  --name upstatus \
  upstatus
```

---

## 🌐 部署到云平台

### Heroku

```bash
# 1. 安装 Heroku CLI
# 2. 登录 Heroku
heroku login

# 3. 创建应用
heroku create your-app-name

# 4. 设置环境变量
heroku config:set SUPABASE_URL=your-url
heroku config:set SUPABASE_KEY=your-key

# 5. 部署
git push heroku main
```

### Vercel

1. 安装 Vercel CLI：`npm i -g vercel`
2. 在项目目录运行：`vercel`
3. 在 Vercel Dashboard 中设置环境变量

### Railway

1. 访问 [Railway](https://railway.app/)
2. 点击 "New Project" → "Deploy from GitHub repo"
3. 选择您的仓库
4. 添加环境变量：`SUPABASE_URL` 和 `SUPABASE_KEY`

---

## 🔧 故障排查

### 问题 1：连接 Supabase 失败

**解决方案：**
- 检查 `SUPABASE_URL` 和 `SUPABASE_KEY` 是否正确
- 确认 Supabase 项目状态正常
- 检查网络连接

### 问题 2：历史记录不显示

**解决方案：**
- 确认已执行建表 SQL
- 检查浏览器控制台是否有错误
- 查看服务器日志：`python app.py`
- 确认至少有一条笔记记录

### 问题 3：自动保存失败

**解决方案：**
- 检查浏览器控制台的网络请求
- 确认服务器正在运行
- 查看服务器日志中的错误信息

### 问题 4：数据未保存

**解决方案：**
- 确认笔记内容不为空（空内容会被删除）
- 检查 Supabase 权限设置
- 如果启用了 RLS，确认策略配置正确

---

## 📝 使用技巧

1. **快捷键**
   - `Ctrl + S` (Windows/Linux) 或 `Cmd + S` (Mac) - 手动保存

2. **自动保存**
   - 停止输入 3 秒后自动保存
   - 页面关闭前会尝试保存未保存的内容

3. **历史记录管理**
   - 点击日期可以快速切换到该日期
   - 使用重命名功能添加易记的标题
   - 空内容的笔记会自动删除

4. **多设备同步**
   - 只需在不同设备上配置相同的 Supabase 连接
   - 数据会自动同步

---

## 📚 更多文档

- [完整 Supabase 设置指南](./SUPABASE_SETUP.md)
- [项目 README](./README.md)

---

## 🆘 需要帮助？

如果遇到问题：

1. 查看 [故障排查](#-故障排查) 部分
2. 检查浏览器控制台和服务器日志
3. 确认环境变量配置正确
4. 验证 Supabase 数据表已创建

---

## 🎉 完成！

恭喜！您已成功部署每日记事本应用。现在可以：

- 📝 开始记录您的笔记
- 🔄 在多个设备间同步
- 📚 查看历史记录
- ✏️ 重命名和管理笔记

享受使用吧！