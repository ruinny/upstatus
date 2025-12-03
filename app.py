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
SUPABASE_URL = os.environ.get('SUPABASE_URL', '').strip()
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '').strip()

# 详细的环境变量检查
if not SUPABASE_URL or not SUPABASE_KEY:
    error_msg = "❌ Supabase 环境变量未配置！\n"
    if not SUPABASE_URL:
        error_msg += "  - 缺少 SUPABASE_URL\n"
    if not SUPABASE_KEY:
        error_msg += "  - 缺少 SUPABASE_KEY\n"
    error_msg += "\n请在部署平台的环境变量中设置：\n"
    error_msg += "  SUPABASE_URL=https://your-project-id.supabase.co\n"
    error_msg += "  SUPABASE_KEY=your-supabase-anon-key\n"
    print(error_msg)
    raise ValueError(error_msg)

# 验证环境变量格式
if not SUPABASE_URL.startswith('https://'):
    error_msg = f"❌ SUPABASE_URL 格式错误: {SUPABASE_URL}\n应该以 https:// 开头"
    print(error_msg)
    raise ValueError(error_msg)

if len(SUPABASE_KEY) < 30:
    error_msg = f"❌ SUPABASE_KEY 似乎无效（长度太短: {len(SUPABASE_KEY)}）\n请检查是否完整复制了 API key"
    print(error_msg)
    raise ValueError(error_msg)

# 验证 SUPABASE_KEY 格式（应该是 JWT 格式，以 eyJ 开头）
if not SUPABASE_KEY.startswith('eyJ'):
    error_msg = f"❌ SUPABASE_KEY 格式错误！\n"
    error_msg += f"当前 KEY 前缀: {SUPABASE_KEY[:20]}...\n\n"
    error_msg += "正确的 Supabase API Key 应该：\n"
    error_msg += "1. 以 'eyJ' 开头（JWT token 格式）\n"
    error_msg += "2. 长度通常在 150-250 个字符\n"
    error_msg += "3. 包含两个点号 '.' 分隔三部分\n\n"
    error_msg += "请从 Supabase Dashboard 获取正确的 key：\n"
    error_msg += "  Settings → API → Project API keys → anon public\n\n"
    error_msg += "⚠️ 不要使用 'sb_secret_' 开头的 key，那是错误的格式\n"
    print(error_msg)
    raise ValueError(error_msg)

# 打印配置信息（用于调试）
print(f"✅ Supabase URL: {SUPABASE_URL}")
print(f"✅ Supabase KEY 长度: {len(SUPABASE_KEY)} 字符")
print(f"✅ Supabase KEY 前10位: {SUPABASE_KEY[:10]}...")

# 初始化 Supabase 客户端（使用延迟初始化避免启动时的错误）
supabase: Client = None

def get_supabase_client():
    """获取 Supabase 客户端实例，使用单例模式"""
    global supabase
    if supabase is None:
        try:
            # 创建客户端时不传递 proxy 参数
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            print("✅ Supabase 客户端初始化成功")
        except Exception as e:
            error_msg = f"❌ Supabase 客户端初始化失败: {str(e)}\n"
            error_msg += "请检查：\n"
            error_msg += "1. SUPABASE_URL 是否正确（从 Supabase Dashboard → Settings → API → Project URL 获取）\n"
            error_msg += "2. SUPABASE_KEY 是否正确（从 Supabase Dashboard → Settings → API → anon public key 获取）\n"
            error_msg += "3. API key 是否完整复制（没有多余的空格或换行）\n"
            error_msg += "4. 依赖包版本是否兼容（尝试运行：pip install --upgrade supabase httpx）\n"
            print(error_msg)
            raise
    return supabase

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/note', methods=['GET'])
def get_note():
    """获取指定日期的记事本内容"""
    try:
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        # 从 Supabase 查询数据
        response = get_supabase_client().table('notes').select('*').eq('date', date).execute()
        
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
            existing = get_supabase_client().table('notes').select('*').eq('date', date).execute()
            
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
                
                get_supabase_client().table('notes').update(update_data).eq('id', note_id).execute()
            else:
                # 插入新记录
                get_supabase_client().table('notes').insert({
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
            get_supabase_client().table('notes').delete().eq('date', date).execute()
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
        existing = get_supabase_client().table('notes').select('*').eq('date', date).execute()
        
        if existing.data and len(existing.data) > 0:
            get_supabase_client().table('notes').delete().eq('date', date).execute()
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
        existing = get_supabase_client().table('notes').select('*').eq('date', old_date).execute()
        
        if not existing.data or len(existing.data) == 0:
            return jsonify({
                'success': False,
                'message': '原记录不存在'
            })
        
        note = existing.data[0]
        note_id = note['id']
        
        # 如果日期改变，检查新日期是否已存在
        if old_date != new_date:
            new_date_check = get_supabase_client().table('notes').select('*').eq('date', new_date).execute()
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
        
        get_supabase_client().table('notes').update(update_data).eq('id', note_id).execute()
        
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
        response = get_supabase_client().table('notes').select('*').order('date', desc=True).execute()
        
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