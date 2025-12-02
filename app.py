from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime
from collections import OrderedDict

app = Flask(__name__)
CORS(app)

# 存储记事本内容的字典，按日期组织（生产环境建议使用数据库）
# 格式: {'2024-12-02': {'content': '...', 'last_updated': '...'}}
notes_by_date = {}
DATA_FILE = 'notes_data.json'

# 加载保存的数据
def load_notes():
    global notes_by_date
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                notes_by_date = json.load(f)
        except Exception as e:
            print(f"加载数据失败: {e}")
            notes_by_date = {}
    else:
        notes_by_date = {}

# 保存数据到文件
def save_notes():
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(notes_by_date, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存数据失败: {e}")

# 启动时加载数据
load_notes()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/note', methods=['GET'])
def get_note():
    """获取指定日期的记事本内容"""
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    note_data = notes_by_date.get(date, {'content': '', 'last_updated': None})
    return jsonify({
        'content': note_data.get('content', ''),
        'last_updated': note_data.get('last_updated'),
        'date': date
    })

@app.route('/api/note', methods=['POST'])
def save_note():
    """保存记事本内容"""
    data = request.get_json()
    content = data.get('content', '')
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    last_updated = datetime.now().isoformat()
    
    # 只有当内容不为空时才保存
    if content.strip():
        notes_by_date[date] = {
            'content': content,
            'last_updated': last_updated
        }
        save_notes()
        return jsonify({
            'success': True,
            'message': '保存成功',
            'last_updated': last_updated,
            'date': date
        })
    else:
        # 如果内容为空，删除该日期的记录
        if date in notes_by_date:
            del notes_by_date[date]
            save_notes()
        return jsonify({
            'success': True,
            'message': '内容为空，已删除记录',
            'last_updated': last_updated,
            'date': date
        })

@app.route('/api/note', methods=['DELETE'])
def clear_note():
    """清空指定日期的记事本内容"""
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    if date in notes_by_date:
        del notes_by_date[date]
        save_notes()
    return jsonify({
        'success': True,
        'message': '已清空',
        'date': date
    })

@app.route('/api/dates', methods=['GET'])
def get_dates():
    """获取所有有记录的日期列表"""
    # 按日期倒序排列
    sorted_dates = sorted(notes_by_date.keys(), reverse=True)
    date_list = []
    for date in sorted_dates:
        note = notes_by_date[date]
        date_list.append({
            'date': date,
            'last_updated': note.get('last_updated'),
            'preview': note.get('content', '')[:50]  # 预览前50个字符
        })
    return jsonify({
        'dates': date_list,
        'count': len(date_list)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)