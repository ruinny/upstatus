from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)

# Supabase 配置
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("请在 .env 文件中设置 SUPABASE_URL 和 SUPABASE_KEY")

# 初始化 Supabase 客户端
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/note', methods=['GET'])
def get_note():
    """获取指定日期的记事本内容"""
    try:
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        # 从 Supabase 查询数据
        response = supabase.table('notes').select('*').eq('date', date).execute()
        
        if response.data and len(response.data) > 0:
            note = response.data[0]
            return jsonify({
                'content': note.get('content', ''),
                'last_updated': note.get('last_updated'),
                'date': date
            })
        else:
            return jsonify({
                'content': '',
                'last_updated': None,
                'date': date
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
        
        # 只有当内容不为空时才保存
        if content.strip():
            # 检查该日期是否已存在记录
            existing = supabase.table('notes').select('*').eq('date', date).execute()
            
            if existing.data and len(existing.data) > 0:
                # 更新现有记录，保留 custom_title
                note_id = existing.data[0]['id']
                custom_title = existing.data[0].get('custom_title', '')
                
                update_data = {
                    'content': content,
                    'last_updated': last_updated
                }
                if custom_title:
                    update_data['custom_title'] = custom_title
                
                supabase.table('notes').update(update_data).eq('id', note_id).execute()
            else:
                # 插入新记录
                supabase.table('notes').insert({
                    'date': date,
                    'content': content,
                    'last_updated': last_updated
                }).execute()
            
            return jsonify({
                'success': True,
                'message': '保存成功',
                'last_updated': last_updated,
                'date': date
            })
        else:
            # 如果内容为空，删除该日期的记录
            supabase.table('notes').delete().eq('date', date).execute()
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
        
        # 检查记录是否存在
        existing = supabase.table('notes').select('*').eq('date', date).execute()
        
        if existing.data and len(existing.data) > 0:
            supabase.table('notes').delete().eq('date', date).execute()
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
        custom_title = data.get('custom_title', '')
        
        if not old_date or not new_date:
            return jsonify({
                'success': False,
                'message': '缺少必要参数'
            })
        
        # 查询原记录
        existing = supabase.table('notes').select('*').eq('date', old_date).execute()
        
        if not existing.data or len(existing.data) == 0:
            return jsonify({
                'success': False,
                'message': '原记录不存在'
            })
        
        note = existing.data[0]
        note_id = note['id']
        
        # 如果日期改变，检查新日期是否已存在
        if old_date != new_date:
            new_date_check = supabase.table('notes').select('*').eq('date', new_date).execute()
            if new_date_check.data and len(new_date_check.data) > 0:
                return jsonify({
                    'success': False,
                    'message': '目标日期已存在记录'
                })
        
        # 更新记录
        update_data = {
            'date': new_date,
            'last_updated': datetime.now().isoformat()
        }
        
        if custom_title.strip():
            update_data['custom_title'] = custom_title.strip()
        else:
            update_data['custom_title'] = None
        
        supabase.table('notes').update(update_data).eq('id', note_id).execute()
        
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
        # 从 Supabase 查询所有记录，按日期倒序排列
        response = supabase.table('notes').select('*').order('date', desc=True).execute()
        
        date_list = []
        if response.data:
            for note in response.data:
                date_list.append({
                    'date': note.get('date'),
                    'custom_title': note.get('custom_title', ''),
                    'last_updated': note.get('last_updated'),
                    'preview': note.get('content', '')[:50]  # 预览前50个字符
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