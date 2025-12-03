from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from contextlib import contextmanager

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)

# SQLite 数据库配置
DB_PATH = os.environ.get('DB_PATH', 'notes.db')

# 数据库上下文管理器
@contextmanager
def get_db():
    """获取数据库连接的上下文管理器"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 使结果可以像字典一样访问
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """初始化数据库表"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL,
                custom_title TEXT,
                last_updated TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # 创建日期索引以提高查询性能
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_date ON notes(date)
        ''')
        print("✅ 数据库初始化成功")

# 应用启动时初始化数据库
init_db()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/note', methods=['GET'])
def get_note():
    """获取指定日期的记事本内容"""
    try:
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT content, last_updated, custom_title FROM notes WHERE date = ?',
                (date,)
            )
            row = cursor.fetchone()
            
            if row:
                return jsonify({
                    'content': row['content'],
                    'last_updated': row['last_updated'],
                    'date': date,
                    'custom_title': row['custom_title']
                })
            else:
                return jsonify({
                    'content': '',
                    'last_updated': None,
                    'date': date,
                    'custom_title': None
                })
    except Exception as e:
        print(f"获取笔记失败: {e}")
        return jsonify({
            'content': '',
            'last_updated': None,
            'date': date,
            'error': str(e)
        }), 500

@app.route('/api/note', methods=['POST'])
def save_note():
    """保存记事本内容"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        last_updated = datetime.now().isoformat()
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # 只有当内容不为空时才保存
            if content.strip():
                # 检查该日期是否已存在记录
                cursor.execute('SELECT id, custom_title FROM notes WHERE date = ?', (date,))
                existing = cursor.fetchone()
                
                if existing:
                    # 更新现有记录，保留 custom_title
                    custom_title = existing['custom_title']
                    cursor.execute(
                        'UPDATE notes SET content = ?, last_updated = ? WHERE date = ?',
                        (content, last_updated, date)
                    )
                else:
                    # 插入新记录
                    cursor.execute(
                        'INSERT INTO notes (date, content, last_updated, created_at) VALUES (?, ?, ?, ?)',
                        (date, content, last_updated, last_updated)
                    )
                
                return jsonify({
                    'success': True,
                    'message': '保存成功',
                    'last_updated': last_updated,
                    'date': date
                })
            else:
                # 如果内容为空，删除该日期的记录
                cursor.execute('DELETE FROM notes WHERE date = ?', (date,))
                return jsonify({
                    'success': True,
                    'message': '内容为空，已删除记录',
                    'last_updated': last_updated,
                    'date': date
                })
    except Exception as e:
        print(f"保存笔记失败: {e}")
        return jsonify({
            'success': False,
            'message': f'保存失败: {str(e)}'
        }), 500

@app.route('/api/note', methods=['DELETE'])
def delete_note():
    """删除指定日期的记事本记录"""
    try:
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        with get_db() as conn:
            cursor = conn.cursor()
            # 检查记录是否存在
            cursor.execute('SELECT id FROM notes WHERE date = ?', (date,))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute('DELETE FROM notes WHERE date = ?', (date,))
                return jsonify({
                    'success': True,
                    'message': '记录已删除',
                    'date': date
                })
            else:
                return jsonify({
                    'success': False,
                    'message': '记录不存在',
                    'date': date
                })
    except Exception as e:
        print(f"删除笔记失败: {e}")
        return jsonify({
            'success': False,
            'message': f'删除失败: {str(e)}'
        }), 500

@app.route('/api/note/rename', methods=['POST'])
def rename_note():
    """重命名记事本记录（修改日期或添加自定义标题）"""
    try:
        data = request.get_json()
        old_date = data.get('old_date')
        new_date = data.get('new_date')
        custom_title = data.get('custom_title', '').strip()
        
        if not old_date or not new_date:
            return jsonify({
                'success': False,
                'message': '缺少必要参数'
            }), 400
        
        with get_db() as conn:
            cursor = conn.cursor()
            
            # 查询原记录
            cursor.execute('SELECT id FROM notes WHERE date = ?', (old_date,))
            existing = cursor.fetchone()
            
            if not existing:
                return jsonify({
                    'success': False,
                    'message': '原记录不存在'
                }), 404
            
            # 如果日期改变，检查新日期是否已存在
            if old_date != new_date:
                cursor.execute('SELECT id FROM notes WHERE date = ?', (new_date,))
                new_date_exists = cursor.fetchone()
                if new_date_exists:
                    return jsonify({
                        'success': False,
                        'message': '目标日期已存在记录'
                    }), 409
            
            # 更新记录
            last_updated = datetime.now().isoformat()
            cursor.execute(
                'UPDATE notes SET date = ?, custom_title = ?, last_updated = ? WHERE date = ?',
                (new_date, custom_title if custom_title else None, last_updated, old_date)
            )
            
            return jsonify({
                'success': True,
                'message': '重命名成功',
                'old_date': old_date,
                'new_date': new_date
            })
    except Exception as e:
        print(f"重命名笔记失败: {e}")
        return jsonify({
            'success': False,
            'message': f'重命名失败: {str(e)}'
        }), 500

@app.route('/api/dates', methods=['GET'])
def get_dates():
    """获取所有有记录的日期列表"""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT date, custom_title, last_updated, 
                       substr(content, 1, 50) as preview
                FROM notes 
                ORDER BY date DESC
            ''')
            rows = cursor.fetchall()
            
            date_list = []
            for row in rows:
                date_list.append({
                    'date': row['date'],
                    'custom_title': row['custom_title'] or '',
                    'last_updated': row['last_updated'],
                    'preview': row['preview']
                })
            
            return jsonify({
                'dates': date_list,
                'count': len(date_list)
            })
    except Exception as e:
        print(f"获取日期列表失败: {e}")
        return jsonify({
            'dates': [],
            'count': 0,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)