# api_report_fix.py - 修复数据报告问题
import json
import re

def fix_api_file():
    """修复API文件中的报告生成问题"""
    with open("complete_fixed_api.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 找到报告生成函数
    report_pattern = r'@app\.post\("/report/generate"\).*?def generate_report.*?\n(.*?)\n\n'
    
    # 检查问题
    if '"stock_analysis"' in content:
        print("找到问题：报告中引用了不存在的字段 'stock_analysis'")
        
        # 修复报告生成函数
        old_report_code = '''        # 生成报告内容
        report = {
            "report_id": f"REPORT_{request.symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "generated_at": datetime.now().isoformat(),
            "stock_analysis": analysis_data,
            "summary": {
                "risk_level": "中等" if analysis_data["risk_metrics"]["volatility"] < 0.25 else "较高",
                "investment_suggestion": "适合长期投资" if analysis_data["risk_metrics"]["sharpe_ratio"] > 1.0 else "建议谨慎投资",
                "key_risks": ["市场波动风险", "行业政策风险", "汇率风险"] if analysis_data["stock_analysis"]["sector"] == "Technology" else ["市场波动风险"]
            },
            "charts": {
                "price_chart": f"data:image/png;base64,{generate_chart_base64(request.symbol, request.days)}",
                "distribution_chart": f"data:image/png;base64,{generate_distribution_base64(analysis_data['history']['returns'])}"
            }
        }'''
        
        new_report_code = '''        # 生成报告内容
        report = {
            "report_id": f"REPORT_{request.symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "generated_at": datetime.now().isoformat(),
            "analysis_data": analysis_data,
            "summary": {
                "risk_level": "中等" if analysis_data["risk_metrics"]["volatility"] < 0.25 else "较高",
                "investment_suggestion": "适合长期投资" if analysis_data["risk_metrics"]["sharpe_ratio"] > 1.0 else "建议谨慎投资",
                "key_risks": ["市场波动风险", "行业政策风险", "汇率风险"] if analysis_data.get("sector") == "Technology" else ["市场波动风险"]
            },
            "charts": {
                "price_chart": f"data:image/png;base64,{generate_chart_base64(request.symbol, request.days)}",
                "distribution_chart": f"data:image/png;base64,{generate_distribution_base64(analysis_data.get('history', {}).get('returns', []))}"
            }
        }'''
        
        if old_report_code in content:
            content = content.replace(old_report_code, new_report_code)
            print("已修复报告生成代码")
        else:
            print("未找到要替换的代码，将手动修复...")
            
            # 手动修复错误行
            content = content.replace('analysis_data["stock_analysis"]["sector"]', 'analysis_data.get("sector")')
            content = content.replace("'stock_analysis'", "'analysis_data'")
    
    # 保存修复后的文件
    with open("complete_fixed_api_v2.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ 已创建修复版API文件: complete_fixed_api_v2.py")

if __name__ == "__main__":
    fix_api_file()
