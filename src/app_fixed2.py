#!/usr/bin/env python3
"""
FinRisk AI Agents - 修复版
最小化功能，确保能运行
"""

import gradio as gr
import sys
import os
from datetime import datetime
import traceback

print("=" * 70)
print("FinRisk AI Agents - 修复版启动")
print("=" * 70)

def check_stock(ticker: str) -> str:
    """检查股票 - 简化版"""
    try:
        import yfinance as yf
        
        if not ticker or not ticker.strip():
            return "⚠️ 请输入股票代码"
        
        ticker = ticker.strip().upper()
        
        # 尝试获取数据
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return f"""
## 📊 {ticker} 股票信息

**公司名称**: {info.get('longName', '未知')}
**当前价格**: 
**市值**: 
**行业**: {info.get('sector', '未知')}
**市盈率**: {info.get('trailingPE', '未知')}

**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

> 💡 提示: 完整分析功能需要更多数据加载时间
"""
    except Exception as e:
        return f"""
## ❌ 分析失败

**股票代码**: {ticker}
**错误信息**: {str(e)}

**建议**:
1. 检查股票代码是否正确
2. 检查网络连接
3. 尝试常见股票: AAPL, MSFT, GOOGL
"""

# 创建极简但完整的界面
with gr.Blocks(title="FinRisk AI Agents", theme=gr.themes.Soft()) as demo:
    
    # 标题
    gr.Markdown("# 🚀 FinRisk AI Agents")
    gr.Markdown("### 智能金融风险分析系统 | 修复版")
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📈 输入股票")
            
            ticker_input = gr.Textbox(
                label="股票代码",
                placeholder="例如: AAPL, MSFT, 000001.SZ",
                value="AAPL"
            )
            
            analyze_btn = gr.Button("🔍 开始分析", variant="primary")
            
            # 示例
            gr.Markdown("#### 示例:")
            gr.Examples(
                examples=[["AAPL"], ["MSFT"], ["GOOGL"], ["TSLA"], ["000001.SZ"]],
                inputs=ticker_input,
                label="点击快速测试"
            )
            
        with gr.Column(scale=2):
            gr.Markdown("### 📊 分析结果")
            output = gr.Markdown("等待输入...")
    
    # 事件
    analyze_btn.click(check_stock, inputs=ticker_input, outputs=output)
    ticker_input.submit(check_stock, inputs=ticker_input, outputs=output)
    
    # 页脚
    gr.Markdown("---")
    gr.Markdown(f"**版本**: 修复版 | **时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    gr.Markdown(f"**路径**: {os.getcwd()}")

if __name__ == "__main__":
    try:
        print("🚀 启动参数:")
        print(f"- 地址: http://0.0.0.0:7860")
        print(f"- 本地访问: http://localhost:7860")
        print("- 按 Ctrl+C 停止")
        print("=" * 70)
        
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True,
            quiet=False,
            inbrowser=True  # 自动打开浏览器
        )
    except KeyboardInterrupt:
        print("\n👋 用户中断，应用停止")
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        traceback.print_exc()
        print("=" * 70)
        input("按回车退出...")
