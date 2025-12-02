from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 存储记事本内容的全局变量（生产环境建议使用数据库）
notepad_content = ""
last_updated = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/note', methods=['GET'])
def get_note():
    """获取记事本内容"""
    return jsonify({
        'content': notepad_content,
        'last_updated': last_updated
    })

@app.route('/api/note', methods=['POST'])
def save_note():
    """保存记事本内容"""
    global notepad_content, last_updated
    data = request.get_json()
    notepad_content = data.get('content', '')
    last_updated = datetime.now().isoformat()
    return jsonify({
        'success': True,
        'message': '保存成功',
        'last_updated': last_updated
    })

@app.route('/api/note', methods=['DELETE'])
def clear_note():
    """清空记事本内容"""
    global notepad_content, last_updated
    notepad_content = ""
    last_updated = datetime.now().isoformat()
    return jsonify({
        'success': True,
        'message': '已清空'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)