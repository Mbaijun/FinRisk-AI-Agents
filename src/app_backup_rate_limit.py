#!/usr/bin/env python3
"""
FinRisk AI Agents - Gradio 6.x 完全兼容版
修复了所有 API 兼容性问题
"""

import gradio as gr
import sys
import os
import json
from datetime import datetime

# ============================================================================
# 设置环境变量
# ============================================================================
os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"

print("=" * 70)
print("🚀 FinRisk AI Agents - Gradio 6.x 兼容版")
print("=" * 70)
print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Python版本: {sys.version.split()[0]}")
print(f"Gradio版本: {gr.__version__}")
print(f"工作目录: {os.getcwd()}")
print("=" * 70)

# ============================================================================
# 检查依赖
# ============================================================================
try:
    import yfinance as yf
    import pandas as pd
    import numpy as np
    STOCK_AVAILABLE = True
    print("✅ 股票分析模块已加载")
except ImportError as e:
    STOCK_AVAILABLE = False
    print(f"⚠️ 部分依赖缺失: {e}")

# ============================================================================
# 核心分析函数
# ============================================================================
def analyze_stock(ticker: str, period: str = "1mo") -> str:
    """分析股票数据"""
    if not STOCK_AVAILABLE:
        return "❌ 请安装依赖: pip install yfinance pandas numpy"
    
    ticker = ticker.strip().upper()
    if not ticker:
        return "⚠️ 请输入股票代码"
    
    try:
        # 获取数据
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if hist.empty:
            return f"❌ 未找到数据: {ticker}"
        
        info = stock.info
        
        # 计算指标
        current_price = float(hist['Close'].iloc[-1])
        prev_price = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
        change_pct = ((current_price / prev_price) - 1) * 100
        
        # 风险计算
        returns = hist['Close'].pct_change().dropna()
        if len(returns) > 1:
            volatility = returns.std() * (252 ** 0.5)
            risk_score = min(10, volatility * 8)
        else:
            volatility = 0
            risk_score = 5
        
        # 风险等级
        if risk_score >= 7:
            risk_level = "🔴 高风险"
            suggestion = "建议谨慎投资，设置止损"
        elif risk_score >= 4:
            risk_level = "🟡 中风险"
            suggestion = "适合适度配置，建议分散投资"
        else:
            risk_level = "🟢 低风险"
            suggestion = "适合稳健型投资者"
        
        # 格式化结果
        result = f"""
# 📊 {ticker} 分析报告

## 💰 价格信息
- **当前价格**: 
- **今日涨跌**: {'📈' if change_pct > 0 else '📉'} {change_pct:+.2f}%
- **分析周期**: {period}

## ⚠️ 风险分析
- **风险评分**: {risk_score:.1f}/10
- **风险等级**: {risk_level}
- **年化波动率**: {volatility*100:.2f}%

## 🏢 公司信息
- **公司**: {info.get('longName', ticker)}
- **行业**: {info.get('sector', '未知')}
- **市值**: 

## 🎯 投资建议
{suggestion}

---
*分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return result
        
    except Exception as e:
        return f"""
## ❌ 分析失败

**股票**: {ticker}
**错误**: {str(e)}

**建议**:
1. 检查代码格式 (AAPL, MSFT, 000001.SZ)
2. 检查网络连接
3. 尝试常见股票

**示例**:
- AAPL (苹果), MSFT (微软), TSLA (特斯拉)
- 000001.SZ (平安银行), 0700.HK (腾讯)
"""

# ============================================================================
# 创建兼容界面 - 关键修复部分
# ============================================================================
def create_app():
    """创建完全兼容 Gradio 6.x 的界面"""
    
    # Gradio 6.x 中，Blocks 不再直接支持 css 参数
    # 我们需要通过其他方式设置样式
    
    # 使用最简化的 Blocks 初始化
    with gr.Blocks() as demo:
        # 通过 Markdown 和样式类来设置
        gr.Markdown("""
        <style>
        .gradio-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
        }
        .title-header {
            text-align: center;
            padding: 20px;
            background: linear-gradient(90deg, #1a237e, #283593);
            color: white;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .stock-input {
            font-family: 'Consolas', monospace;
            font-size: 16px;
        }
        .result-box {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #2196f3;
        }
        </style>
        
        <div class="title-header">
            <h1>🚀 FinRisk AI Agents</h1>
            <h3>智能金融风险分析系统 | 版本 2.1 (Gradio 6.x 兼容版)</h3>
        </div>
        """)
        
        # 使用 Tabs 组织内容
        with gr.Tabs():
            # 标签页 1: 股票分析
            with gr.TabItem("📈 股票分析"):
                with gr.Row():
                    # 左侧输入区
                    with gr.Column(scale=1):
                        gr.Markdown("### 🔍 输入股票信息")
                        
                        ticker_input = gr.Textbox(
                            label="股票代码",
                            placeholder="例如: AAPL, MSFT, 000001.SZ",
                            value="AAPL",
                            elem_classes=["stock-input"]
                        )
                        
                        period_select = gr.Dropdown(
                            choices=["1d", "5d", "1mo", "3mo", "6mo", "1y"],
                            value="1mo",
                            label="分析周期"
                        )
                        
                        gr.Markdown("### ⚡ 快速选择")
                        with gr.Row():
                            gr.Button("AAPL").click(lambda: "AAPL", outputs=ticker_input)
                            gr.Button("MSFT").click(lambda: "MSFT", outputs=ticker_input)
                            gr.Button("TSLA").click(lambda: "TSLA", outputs=ticker_input)
                            gr.Button("NVDA").click(lambda: "NVDA", outputs=ticker_input)
                        
                        analyze_btn = gr.Button("🚀 开始分析", variant="primary")
                        
                        gr.Markdown("### 📋 示例")
                        gr.Examples(
                            examples=[["AAPL"], ["MSFT"], ["GOOGL"], ["TSLA"], ["000001.SZ"]],
                            inputs=ticker_input,
                            label="点击使用示例"
                        )
                    
                    # 右侧结果区
                    with gr.Column(scale=2):
                        gr.Markdown("### 📊 分析结果")
                        result_output = gr.Markdown("""
                        <div class="result-box">
                        👈 **请输入股票代码并点击分析**
                        
                        **支持格式:**
                        - 美股: AAPL, MSFT, GOOGL
                        - A股: 000001.SZ, 600000.SS
                        - 港股: 0700.HK, 9988.HK
                        
                        **提示:** 首次获取可能需要几秒钟。
                        </div>
                        """)
                
                # 事件绑定
                analyze_btn.click(
                    fn=analyze_stock,
                    inputs=[ticker_input, period_select],
                    outputs=result_output
                )
                
                ticker_input.submit(
                    fn=analyze_stock,
                    inputs=[ticker_input, period_select],
                    outputs=result_output
                )
            
            # 标签页 2: 系统信息
            with gr.TabItem("⚙️ 系统信息"):
                gr.Markdown(f"""
                <div class="result-box">
                ## 🖥️ 系统状态
                
                **FinRisk AI Agents v2.1**
                
                ### 📊 服务状态
                - **状态**: ✅ 运行正常
                - **股票分析**: {"✅ 可用" if STOCK_AVAILABLE else "❌ 需安装依赖"}
                - **启动时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                - **Python**: {sys.version.split()[0]}
                - **Gradio**: {gr.__version__}
                
                ### 🌐 访问信息
                - **本地地址**: http://localhost:7860
                - **项目路径**: {os.getcwd()}
                
                ### 📈 功能状态
                1. ✅ 单股票风险分析
                2. ✅ 实时数据获取
                3. ✅ 风险评分计算
                4. ✅ 投资建议生成
                
                ---
                
                **🔧 如需安装依赖:**
                `ash
                pip install yfinance pandas numpy
                `
                
                **⚠️ 免责声明:**
                本工具仅供参考，不构成投资建议。
                </div>
                """)
        
        # 页脚
        gr.Markdown(f"""
        ---
        <div style="text-align: center; color: #666; font-size: 0.9em;">
        <strong>📁</strong> {os.getcwd()} | 
        <strong>🕐</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
        <strong>🚀</strong> Gradio 6.x 兼容版
        </div>
        """)
    
    return demo

# ============================================================================
# 主函数
# ============================================================================
def main():
    """主启动函数"""
    print("🔄 创建兼容界面...")
    app = create_app()
    
    # 启动参数
    launch_params = {
        "server_name": "0.0.0.0",
        "server_port": 7860,
        "share": False,
        "show_error": True,
        "inbrowser": True,
        "quiet": False
    }
    
    print("=" * 70)
    print("✅ 准备启动!")
    print(f"📡 访问: http://localhost:{launch_params['server_port']}")
    print("=" * 70)
    
    try:
        app.launch(**launch_params)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("尝试备用端口 7865...")
        launch_params["server_port"] = 7865
        app.launch(**launch_params)

if __name__ == "__main__":
    main()
