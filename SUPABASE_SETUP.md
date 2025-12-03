# Supabase 设置指南

## 1. 在 Supabase 中创建数据表

登录到您的 Supabase 项目，进入 SQL Editor，执行以下 SQL 语句：

```sql
-- 创建笔记表
CREATE TABLE IF NOT EXISTS notes (
  id SERIAL PRIMARY KEY,
  date TEXT UNIQUE NOT NULL,
  content TEXT,
  custom_title TEXT,
  last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_notes_date ON notes(date);
CREATE INDEX IF NOT EXISTS idx_notes_last_updated ON notes(last_updated DESC);

-- 添加注释
COMMENT ON TABLE notes IS '每日记事本数据表';
COMMENT ON COLUMN notes.date IS '日期，格式：YYYY-MM-DD';
COMMENT ON COLUMN notes.content IS '笔记内容';
COMMENT ON COLUMN notes.custom_title IS '自定义标题';
COMMENT ON COLUMN notes.last_updated IS '最后更新时间';
COMMENT ON COLUMN notes.created_at IS '创建时间';
```

或者直接运行项目中的 `setup_supabase.sql` 文件。

## 2. 配置环境变量

### 方法 1：创建 .env 文件（本地开发）

在项目根目录创建 `.env` 文件：

```bash
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-or-service-role-key
PORT=5000
```

### 方法 2：设置系统环境变量（生产环境）

**Windows:**
```cmd
set SUPABASE_URL=https://your-project-id.supabase.co
set SUPABASE_KEY=your-supabase-key
```

**Linux/Mac:**
```bash
export SUPABASE_URL=https://your-project-id.supabase.co
export SUPABASE_KEY=your-supabase-key
```

## 3. 获取 Supabase 连接信息

1. 登录 [Supabase Dashboard](https://app.supabase.com/)
2. 选择您的项目
3. 点击左侧菜单的 "Settings" → "API"
4. 复制以下信息：
   - **URL**: 在 "Project URL" 部分
   - **anon/public key**: 在 "Project API keys" 部分的 "anon public" key

**重要提示：**
- 对于公开应用，使用 `anon` key（有 Row Level Security 保护）
- 对于私有应用或服务端使用，可以使用 `service_role` key（完全访问权限）

## 4. 安装依赖

```bash
pip install -r requirements.txt
```

## 5. 运行应用

```bash
python app.py
```

## 6. 数据迁移（可选）

如果您之前使用文件存储（`data/notes_data.json`），需要手动迁移数据到 Supabase：

1. 打开您的 `data/notes_data.json` 文件
2. 在 Supabase Dashboard 的 Table Editor 中，手动添加记录
3. 或者使用以下 Python 脚本迁移：

```python
import json
from supabase import create_client
import os

# 配置
SUPABASE_URL = "your-url"
SUPABASE_KEY = "your-key"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 读取旧数据
with open('data/notes_data.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

# 迁移数据
for date, note_data in old_data.items():
    supabase.table('notes').insert({
        'date': date,
        'content': note_data.get('content', ''),
        'custom_title': note_data.get('custom_title', ''),
        'last_updated': note_data.get('last_updated')
    }).execute()

print("数据迁移完成！")
```

## 7. 部署到生产环境

### Heroku
在 Heroku Dashboard 的 Settings → Config Vars 中添加：
- `SUPABASE_URL`
- `SUPABASE_KEY`

### Vercel
在项目设置中添加环境变量。

### Railway/Render
在环境变量配置中添加相应的变量。

## 8. 故障排查

### 连接失败
- 检查 `SUPABASE_URL` 和 `SUPABASE_KEY` 是否正确
- 确认 Supabase 项目状态正常
- 检查网络连接

### 权限错误
- 确认使用了正确的 API key
- 检查 Supabase 的 Row Level Security (RLS) 策略
- 如果需要公开访问，可以暂时禁用 RLS（不推荐用于生产环境）

### 数据未显示
- 检查表名是否为 `notes`
- 确认数据已正确插入到数据库
- 查看浏览器控制台和服务器日志

## 9. 性能优化建议

1. 使用索引提高查询速度（已在 SQL 中创建）
2. 考虑添加数据缓存
3. 定期清理旧数据
4. 监控 Supabase 使用量

## 10. 安全建议

1. **不要**将 `.env` 文件提交到 Git
2. 使用 `anon` key 而不是 `service_role` key（除非必要）
3. 启用 Row Level Security (RLS)
4. 定期轮换 API keys
5. 限制 API 请求速率