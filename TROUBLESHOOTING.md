# 故障排除指南

## ❌ 错误：Invalid API key

### 错误信息
```
supabase._sync.client.SupabaseException: Invalid API key
```

### 原因分析
这个错误表示 Supabase 客户端认为你提供的 API key 格式不正确或无效。最常见的原因是：

1. **使用了错误格式的 key** - 使用了 `sb_secret_` 开头的格式（这是错误的）
2. **环境变量未正确设置** - `.env` 文件中的值不正确
3. **复制 key 时出错** - key 不完整或包含额外的空格/换行符
4. **使用了错误类型的 key** - 混淆了不同类型的 Supabase keys

---

## ✅ 解决方案

### 步骤 1: 获取正确的 API Key

1. 登录 [Supabase Dashboard](https://app.supabase.com)
2. 选择你的项目
3. 点击左侧菜单 **Settings** → **API**
4. 在 **Project API keys** 部分找到 **anon public** key
5. 点击复制按钮，确保复制完整的 key

**重要提示：**
- ✅ 正确的 key 以 `eyJ` 开头（JWT token 格式）
- ✅ 长度通常在 150-250 个字符
- ✅ 包含两个点号 `.` 分隔三个部分
- ❌ 不要使用 `sb_secret_` 开头的 key
- ❌ 不要使用 `service_role` key（除非你明确需要管理员权限）

**示例格式：**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN5bG9sYXJzaHdicHViZmR1dXltIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODkxNTQ4ODUsImV4cCI6MjAwNDczMDg4NX0.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 步骤 2: 配置环境变量

#### 本地开发

创建或编辑 `.env` 文件：

```bash
# .env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.your-actual-key-here
```

**注意：**
- 不要在 key 前后添加引号
- 确保 URL 以 `https://` 开头，以 `.supabase.co` 结尾
- 检查是否有多余的空格或换行符

#### 部署平台（Zeabur/Heroku/等）

在部署平台的环境变量设置中添加：

**Zeabur:**
1. 进入项目设置
2. 点击 "Environment Variables"
3. 添加环境变量：
   - `SUPABASE_URL` = `https://your-project-id.supabase.co`
   - `SUPABASE_KEY` = `eyJhbGciOi...`（完整的 anon key）

**Heroku:**
```bash
heroku config:set SUPABASE_URL=https://your-project-id.supabase.co
heroku config:set SUPABASE_KEY=eyJhbGciOi...
```

### 步骤 3: 验证配置

运行应用，检查启动日志：

```bash
python app.py
```

你应该看到：
```
✅ Supabase URL: https://your-project-id.supabase.co
✅ Supabase KEY 长度: XXX 字符
✅ Supabase KEY 前10位: eyJhbGciOi...
✅ Supabase 客户端初始化成功
```

如果看到错误信息，请仔细阅读错误提示并按照说明修复。

---

## 🔍 常见问题

### Q1: 我的 key 是 `sb_secret_` 开头的，这是什么？
**A:** 这可能是你自己生成的测试 key，不是 Supabase 官方的格式。请从 Supabase Dashboard 的 API 设置页面获取正确的 `anon public` key。

### Q2: 我应该使用 anon key 还是 service_role key？
**A:** 对于大多数应用，使用 `anon public` key。它提供了行级安全（RLS）保护。只有在需要绕过 RLS 规则时才使用 `service_role` key（通常不推荐在客户端使用）。

### Q3: 我已经正确配置了，但仍然报错？
**A:** 请检查：
1. `.env` 文件是否在项目根目录
2. 是否重启了应用
3. 环境变量是否正确加载（打印 `os.environ.get('SUPABASE_KEY')` 检查）
4. Supabase 项目是否处于活跃状态（未暂停）
5. 网络连接是否正常

### Q4: 在 Docker 中如何配置？
**A:** 在 `docker-compose.yml` 中设置环境变量：

```yaml
services:
  web:
    environment:
      - SUPABASE_URL=https://your-project-id.supabase.co
      - SUPABASE_KEY=eyJhbGciOi...
```

或使用 `.env` 文件并在 `docker-compose.yml` 中引用：

```yaml
services:
  web:
    env_file:
      - .env
```

---

## 🛠️ 调试技巧

### 检查环境变量是否正确加载

在 `app.py` 的开头添加调试代码：

```python
import os
print("DEBUG - SUPABASE_URL:", os.environ.get('SUPABASE_URL'))
print("DEBUG - SUPABASE_KEY length:", len(os.environ.get('SUPABASE_KEY', '')))
print("DEBUG - SUPABASE_KEY prefix:", os.environ.get('SUPABASE_KEY', '')[:10])
```

### 测试 Supabase 连接

创建一个简单的测试脚本：

```python
# test_supabase.py
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.environ.get('SUPABASE_URL', '').strip()
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '').strip()

print(f"URL: {SUPABASE_URL}")
print(f"Key length: {len(SUPABASE_KEY)}")
print(f"Key starts with 'eyJ': {SUPABASE_KEY.startswith('eyJ')}")
print(f"Key preview: {SUPABASE_KEY[:50]}...")

if SUPABASE_URL and SUPABASE_KEY:
    from supabase import create_client
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ 连接成功！")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
else:
    print("❌ 环境变量未设置")
```

运行：
```bash
python test_supabase.py
```

---

## 📚 相关文档

- [Supabase API 设置文档](https://supabase.com/docs/guides/api)
- [环境变量最佳实践](https://12factor.net/config)
- [Python dotenv 库文档](https://github.com/theskumar/python-dotenv)

---

## 💡 需要更多帮助？

如果按照以上步骤仍然无法解决问题，请提供以下信息：

1. 完整的错误日志
2. `SUPABASE_KEY` 的前 20 个字符（不要泄露完整 key）
3. Python 版本和依赖版本
4. 部署环境（本地/Docker/云平台）

创建 issue 时请包含这些信息以便快速定位问题。