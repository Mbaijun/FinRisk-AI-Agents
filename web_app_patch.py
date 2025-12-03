# web_app_patch.py - 修复Web应用中的字段引用
import re

def fix_web_app():
    with open("web_app_fixed.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 修复字段引用
    fixes = [
        ('analysis_data\\["stock_analysis"\\]\\["sector"\\]', 'analysis_data.get("sector")'),
        ("'stock_analysis'", "'analysis'"),
        ('report.get\\(\\"stock_analysis\\"\\)', 'report.get("analysis")'),
    ]
    
    for old, new in fixes:
        if re.search(old, content):
            content = re.sub(old, new, content)
            print(f"已修复: {old} -> {new}")
    
    # 保存修复后的文件
    with open("web_app_fixed_v2.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ 已创建修复版Web应用: web_app_fixed_v2.py")

if __name__ == "__main__":
    fix_web_app()
