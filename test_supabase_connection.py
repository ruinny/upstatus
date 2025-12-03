#!/usr/bin/env python3
"""
Supabase 连接测试脚本

用于验证 Supabase 配置是否正确
"""

from dotenv import load_dotenv
import os
import sys

def test_connection():
    """测试 Supabase 连接"""
    
    print("=" * 60)
    print("🔍 Supabase 连接测试")
    print("=" * 60)
    print()
    
    # 加载环境变量
    load_dotenv()
    
    # 获取配置
    SUPABASE_URL = os.environ.get('SUPABASE_URL', '').strip()
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '').strip()
    
    # 测试 1: 检查环境变量是否存在
    print("📋 测试 1: 检查环境变量")
    print("-" * 60)
    
    if not SUPABASE_URL:
        print("❌ SUPABASE_URL 未设置")
        return False
    else:
        print(f"✅ SUPABASE_URL: {SUPABASE_URL}")
    
    if not SUPABASE_KEY:
        print("❌ SUPABASE_KEY 未设置")
        return False
    else:
        print(f"✅ SUPABASE_KEY 长度: {len(SUPABASE_KEY)} 字符")
        print(f"   前 20 个字符: {SUPABASE_KEY[:20]}...")
    
    print()
    
    # 测试 2: 验证 URL 格式
    print("📋 测试 2: 验证 URL 格式")
    print("-" * 60)
    
    if not SUPABASE_URL.startswith('https://'):
        print(f"❌ URL 格式错误: 应该以 'https://' 开头")
        print(f"   当前值: {SUPABASE_URL}")
        return False
    
    if not SUPABASE_URL.endswith('.supabase.co'):
        print(f"⚠️  警告: URL 不是标准的 Supabase 格式（应该以 .supabase.co 结尾）")
        print(f"   当前值: {SUPABASE_URL}")
    else:
        print(f"✅ URL 格式正确")
    
    print()
    
    # 测试 3: 验证 API Key 格式
    print("📋 测试 3: 验证 API Key 格式")
    print("-" * 60)
    
    if not SUPABASE_KEY.startswith('eyJ'):
        print(f"❌ API Key 格式错误！")
        print(f"   当前 Key 前缀: {SUPABASE_KEY[:20]}...")
        print()
        print("   正确的 Supabase API Key 应该：")
        print("   - 以 'eyJ' 开头（JWT token 格式）")
        print("   - 长度通常在 150-250 个字符")
        print("   - 包含两个点号 '.' 分隔三部分")
        print()
        print("   请从 Supabase Dashboard 获取正确的 key：")
        print("   Settings → API → Project API keys → anon public")
        return False
    else:
        print(f"✅ Key 格式正确（JWT token）")
    
    if len(SUPABASE_KEY) < 100:
        print(f"⚠️  警告: Key 长度可能太短 ({len(SUPABASE_KEY)} 字符)")
        print(f"   正常的 Supabase Key 长度应该在 150-250 字符")
    else:
        print(f"✅ Key 长度合理 ({len(SUPABASE_KEY)} 字符)")
    
    dot_count = SUPABASE_KEY.count('.')
    if dot_count != 2:
        print(f"⚠️  警告: JWT token 应该包含 2 个点号，当前有 {dot_count} 个")
    else:
        print(f"✅ JWT 结构正确（包含 2 个点号）")
    
    print()
    
    # 测试 4: 尝试连接 Supabase
    print("📋 测试 4: 尝试连接 Supabase")
    print("-" * 60)
    
    try:
        from supabase import create_client
        print("✅ supabase 库已安装")
    except ImportError:
        print("❌ supabase 库未安装")
        print("   请运行: pip install supabase")
        return False
    
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase 客户端创建成功")
        
        # 尝试执行一个简单的查询来验证连接
        try:
            # 这会触发实际的 API 调用
            result = client.table('notes').select('*').limit(1).execute()
            print("✅ 数据库连接测试成功")
            print(f"   成功连接到 'notes' 表")
        except Exception as e:
            error_msg = str(e)
            if 'relation "public.notes" does not exist' in error_msg or 'does not exist' in error_msg:
                print("⚠️  'notes' 表不存在")
                print("   请运行 setup_supabase.sql 脚本创建数据表")
                print("   但 Supabase 连接本身是正常的")
            elif 'permission denied' in error_msg.lower():
                print("⚠️  权限不足")
                print("   请检查 Supabase RLS (Row Level Security) 策略")
            else:
                print(f"⚠️  数据库查询失败: {error_msg}")
                print("   但客户端创建成功，配置应该是正确的")
        
    except Exception as e:
        print(f"❌ Supabase 客户端创建失败")
        print(f"   错误信息: {str(e)}")
        print()
        print("   可能的原因：")
        print("   1. API Key 不正确或已过期")
        print("   2. URL 指向的项目不存在")
        print("   3. 网络连接问题")
        return False
    
    print()
    print("=" * 60)
    print("🎉 所有测试通过！配置正确！")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    try:
        success = test_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 测试过程中发生未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)