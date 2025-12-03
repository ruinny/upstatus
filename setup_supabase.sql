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