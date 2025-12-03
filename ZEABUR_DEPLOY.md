# Zeabur 部署指南

## 🚀 在 Zeabur 上部署此应用

### 步骤 1：准备 Supabase 数据库

1. 访问 [Supabase](https://app.supabase.com/) 并登录
2. 创建新项目或选择现有项目
3. 进入 **SQL Editor**，执行以下 SQL：

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

### 步骤 2：获取 Supabase 连接信息

1. 在 Supabase Dashboard 中，点击左侧的 **Settings** ⚙️
2. 选择 **API** 选项卡
3. 复制以下信息：
   - **Project URL** → 这是您的 `SUPABASE_URL`
   - **anon public** key → 这是您的 `SUPABASE_KEY`

**重要提示：**
- 确保复制完整的 URL（以 `https://` 开头）
- 确保复制完整的 API key（通常很长，100+ 字符）
- 不要有多余的空格或换行

### 步骤 3：在 Zeabur 中部署

#### 方法 1：通过 GitHub 部署（推荐）

1. 将代码推送到 GitHub 仓库
2. 访问 [Zeabur Dashboard](https://zeabur.com/)
3. 点击 **New Project**
4. 选择 **Import from GitHub**
5. 选择您的仓库
6. Zeabur 会自动检测并部署

#### 方法 2：通过 Zeabur CLI 部署

```bash
# 安装 Zeabur CLI
npm i -g zeabur

# 登录
zeabur auth login

# 部署
zeabur deploy
```

### 步骤 4：配置环境变量 ⚠️ 重要

在 Zeabur Dashboard 中：

1. 选择您的项目
2. 点击服务（Service）
3. 进入 **Variables** 或 **Environment Variables** 选项卡
4. 添加以下环境变量：

```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...（您的完整 API key）
PORT=5000
```

**配置要点：**
- ✅ 确保 `SUPABASE_URL` 以 `https://` 开头
- ✅ 确保 `SUPABASE_KEY` 完整（通常 100+ 字符）
- ✅ 不要有多余的空格、换行或引号
- ✅ 保存后重新部署服务

### 步骤 5：重新部署

配置环境变量后：

1. 在 Zeabur Dashboard 中找到您的服务
2. 点击 **Redeploy** 或 **Restart** 按钮
3. 等待部署完成

### 步骤 6：验证部署

1. 点击 Zeabur 提供的域名访问应用
2. 检查日志确认没有错误：
   - 应该看到 `✅ Supabase URL: https://...`
   - 应该看到 `✅ Supabase KEY 长度: xxx 字符`
   - 应该看到 `✅ Supabase 客户端初始化成功`

## 🔧 故障排查

### 错误：Invalid API key

**可能的原因：**

1. **环境变量未设置**
   - 检查 Zeabur Dashboard → Variables 中是否添加了环境变量
   - 确认变量名正确：`SUPABASE_URL` 和 `SUPABASE_KEY`（区分大小写）

2. **API Key 不完整**
   - API key 应该很长（100+ 字符）
   - 确保复制时没有截断
   - 检查是否有多余的空格或换行

3. **使用了错误的 Key**
   - 应该使用 **anon public** key
   - 不要使用 **service_role** key（除非您知道自己在做什么）

4. **URL 格式错误**
   - URL 应该是：`https://xxxxx.supabase.co`
   - 不要添加多余的路径或参数

### 如何检查环境变量

在 Zeabur 日志中查看：

```
✅ Supabase URL: https://xxxxx.supabase.co
✅ Supabase KEY 长度: 122 字符
✅ Supabase KEY 前10位: eyJhbGciOi...
```

如果看到：
```
❌ 缺少 SUPABASE_URL
❌ 缺少 SUPABASE_KEY
```

说明环境变量没有正确设置。

### 解决步骤

1. **重新复制 API 凭证**
   - 登录 Supabase Dashboard
   - Settings → API
   - 重新复制 Project URL 和 anon public key

2. **在 Zeabur 中更新环境变量**
   - 删除现有的变量（如果有）
   - 重新添加，确保没有多余空格
   - 格式示例：
     ```
     SUPABASE_URL=https://abcdefghijk.supabase.co
     SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODQ5MjE2MDAsImV4cCI6MjAwMDQ5NzYwMH0.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
     ```

3. **保存并重新部署**
   - 点击 Save
   - 点击 Redeploy 或 Restart
   - 查看日志确认成功

### 查看日志

在 Zeabur Dashboard 中：
1. 选择您的服务
2. 点击 **Logs** 或 **Runtime Logs**
3. 查看启动日志，确认：
   - ✅ 环境变量加载成功
   - ✅ Supabase 客户端初始化成功
   - ❌ 如果有错误，日志会显示详细信息

## 📝 环境变量清单

| 变量名 | 必需 | 说明 | 示例 |
|--------|------|------|------|
| `SUPABASE_URL` | ✅ 是 | Supabase 项目 URL | `https://xxxxx.supabase.co` |
| `SUPABASE_KEY` | ✅ 是 | Supabase anon public key | `eyJhbG...` (很长) |
| `PORT` | ❌ 否 | 端口号（Zeabur 会自动设置） | `5000` |

## 🎯 快速检查清单

部署前确认：
- [ ] 已在 Supabase 中创建数据表（执行 SQL）
- [ ] 已复制完整的 SUPABASE_URL
- [ ] 已复制完整的 SUPABASE_KEY（anon public）
- [ ] 在 Zeabur 中正确设置了环境变量
- [ ] 变量名正确（区分大小写）
- [ ] 没有多余的空格或引号
- [ ] 已重新部署服务

## 🔗 相关链接

- [Supabase Dashboard](https://app.supabase.com/)
- [Zeabur Dashboard](https://zeabur.com/)
- [项目文档](./README.md)
- [快速开始指南](./QUICKSTART.md)

## 💡 小贴士

1. **首次部署可能需要几分钟**，请耐心等待
2. **环境变量修改后必须重新部署**才能生效
3. **查看日志**是排查问题的最佳方式
4. 如果问题持续，尝试**删除服务并重新创建**

---

如有问题，请检查日志并参考上述故障排查步骤。