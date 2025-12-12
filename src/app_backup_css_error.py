#!/usr/bin/env python3
"""
FinRisk AI Agents - Gradio 6.0.2 完全兼容版
已修复 theme 参数问题，支持完整股票分析功能
"""

import gradio as gr
import sys
import os
import json
from datetime import datetime

# ============================================================================
# 设置环境变量（绕过可能的代理问题）
# ============================================================================
os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"
os.environ["GRADIO_SERVER_PORT"] = "7860"

print("=" * 70)
print("🚀 FinRisk AI Agents - 完全兼容版 v2.1")
print("=" * 70)
print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Python版本: {sys.version.split()[0]}")
print(f"工作目录: {os.getcwd()}")
print("=" * 70)

# ============================================================================
# 检查并导入股票分析模块
# ============================================================================
try:
    import yfinance as yf
    import pandas as pd
    import numpy as np
    STOCK_ANALYSIS_AVAILABLE = True
    print("✅ 股票分析模块已加载")
except ImportError as e:
    STOCK_ANALYSIS_AVAILABLE = False
    print(f"⚠️ 部分依赖缺失: {e}")
    print("请运行: pip install yfinance pandas numpy")

# ============================================================================
# 股票分析核心函数
# ============================================================================
def analyze_stock_simple(ticker: str, period: str = "1mo") -> str:
    """简化的股票分析函数"""
    if not STOCK_ANALYSIS_AVAILABLE:
        return "❌ 股票分析功能不可用，请安装 yfinance 库"
    
    if not ticker or not ticker.strip():
        return "⚠️ 请输入股票代码"
    
    ticker = ticker.strip().upper()
    
    try:
        # 获取股票数据
        stock = yf.Ticker(ticker)
        
        # 获取历史数据
        hist = stock.history(period=period)
        if hist.empty:
            return f"❌ 未找到股票数据: {ticker}"
        
        # 获取公司信息
        info = stock.info
        
        # 基础信息
        current_price = hist['Close'].iloc[-1] if not hist.empty else 0
        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        change_pct = ((current_price / prev_price) - 1) * 100
        
        # 计算简单风险指标
        returns = hist['Close'].pct_change().dropna()
        if len(returns) > 1:
            volatility = returns.std() * (252 ** 0.5)  # 年化波动率
            risk_score = min(10, volatility * 8)  # 简化风险评分
        else:
            volatility = 0
            risk_score = 5
        
        # 风险等级
        if risk_score >= 7:
            risk_level = "🔴 高风险"
            recommendation = "建议谨慎投资，设置止损"
        elif risk_score >= 4:
            risk_level = "🟡 中风险"
            recommendation = "适合适度配置，建议分散投资"
        else:
            risk_level = "🟢 低风险"
            recommendation = "适合稳健型投资者"
        
        # 格式化输出
        output = f"""
# 📊 {ticker} 股票分析报告

## 💰 价格信息
- **当前价格**: 
- **今日涨跌**: {'📈' if change_pct > 0 else '📉'} {change_pct:+.2f}%
- **分析周期**: {period}

## ⚠️ 风险分析
- **风险评分**: {risk_score:.1f}/10
- **风险等级**: {risk_level}
- **年化波动率**: {volatility*100:.2f}%

## 🏢 公司信息
- **公司名称**: {info.get('longName', ticker)}
- **所属行业**: {info.get('sector', '未知')}
- **市值**: 

## 🎯 投资建议
{recommendation}

---
*分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*数据来源: Yahoo Finance*
"""
        
        return output
        
    except Exception as e:
        return f"""
## ❌ 分析过程中出错

**错误信息**: {str(e)}

**建议操作**:
1. 检查股票代码格式（如: AAPL, MSFT, 000001.SZ）
2. 检查网络连接
3. 尝试更短的分析周期
4. 使用示例股票代码测试

**常见示例**:
- 美股: AAPL (苹果), MSFT (微软), GOOGL (谷歌)
- A股: 000001.SZ (平安银行), 600000.SS (浦发银行)
- 港股: 0700.HK (腾讯), 9988.HK (阿里巴巴)
"""

# ============================================================================
# 创建 Gradio 界面 - 使用 Gradio 6.x 兼容语法
# ============================================================================
def create_interface():
    """创建兼容 Gradio 6.x 的界面"""
    
    # 预定义股票分类
    stock_categories = {
        "科技巨头": ["AAPL", "MSFT", "GOOGL", "AMZN", "META"],
        "芯片制造": ["NVDA", "AMD", "INTC", "TSM"],
        "新能源汽车": ["TSLA", "NIO", "LI", "XPEV"],
        "金融股": ["JPM", "BAC", "GS", "MS"],
        "中概股": ["BABA", "PDD", "JD", "BIDU"]
    }
    
    # 创建 Blocks 界面 - 注意：Gradio 6.x 中 theme 参数用法已改变
    # 这里使用不带 theme 参数的版本确保兼容性
    with gr.Blocks(title="FinRisk AI Agents", css=".gradio-container { max-width: 1200px; }") as demo:
        
        # 标题区域
        gr.Markdown("""
        # 🚀 FinRisk AI Agents
        ## 智能金融风险分析系统 | 版本 2.1 完全兼容版
        
        ---
        """)
        
        # 标签页布局
        with gr.Tabs() as tabs:
            
            # 标签页 1: 单股票分析
            with gr.Tab("📈 单股票分析"):
                with gr.Row():
                    # 左侧输入区
                    with gr.Column(scale=1):
                        gr.Markdown("### 🔍 输入股票信息")
                        
                        ticker_input = gr.Textbox(
                            label="股票代码",
                            placeholder="例如: AAPL (苹果), MSFT (微软), 000001.SZ",
                            value="AAPL",
                            interactive=True
                        )
                        
                        period_select = gr.Dropdown(
                            choices=[
                                ("1天", "1d"),
                                ("5天", "5d"),
                                ("1个月", "1mo"),
                                ("3个月", "3mo"),
                                ("6个月", "6mo"),
                                ("1年", "1y")
                            ],
                            value="1mo",
                            label="分析周期"
                        )
                        
                        # 快速选择按钮
                        gr.Markdown("### ⚡ 快速选择")
                        with gr.Row():
                            for category, stocks in list(stock_categories.items())[:3]:
                                with gr.Column():
                                    gr.Markdown(f"**{category}**")
                                    for stock in stocks[:2]:
                                        btn = gr.Button(stock, size="sm", variant="secondary")
                                        btn.click(lambda s=stock: s, outputs=ticker_input)
                        
                        analyze_btn = gr.Button("🚀 开始分析", variant="primary", size="lg")
                        
                        # 示例
                        gr.Markdown("### 📋 示例")
                        example_stocks = [["AAPL"], ["MSFT"], ["GOOGL"], ["TSLA"], ["000001.SZ"]]
                        gr.Examples(examples=example_stocks, inputs=ticker_input, label="点击使用示例")
                    
                    # 右侧结果区
                    with gr.Column(scale=2):
                        gr.Markdown("### 📊 分析结果")
                        result_output = gr.Markdown("""
                        👈 **请输入股票代码并点击『开始分析』**
                        
                        **支持的股票代码格式:**
                        - 美股: AAPL, MSFT, GOOGL, AMZN, TSLA
                        - A股: 000001.SZ, 600000.SS (需要添加 .SZ 或 .SS 后缀)
                        - 港股: 0700.HK, 9988.HK (需要添加 .HK 后缀)
                        
                        **提示:** 首次获取数据可能需要几秒钟时间。
                        """)
                
                # 事件绑定
                analyze_btn.click(
                    fn=analyze_stock_simple,
                    inputs=[ticker_input, period_select],
                    outputs=result_output
                )
                
                ticker_input.submit(
                    fn=analyze_stock_simple,
                    inputs=[ticker_input, period_select],
                    outputs=result_output
                )
            
            # 标签页 2: 系统信息
            with gr.Tab("⚙️ 系统信息"):
                gr.Markdown(f"""
                ## 🖥️ 系统状态
                
                **FinRisk AI Agents v2.1 (Gradio {gr.__version__})**
                
                ### 📊 服务状态
                - **应用状态**: ✅ 运行正常
                - **股票分析**: {"✅ 可用" if STOCK_ANALYSIS_AVAILABLE else "❌ 需要安装 yfinance"}
                - **启动时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                
                ### 🔧 技术信息
                - **Python版本**: {sys.version.split()[0]}
                - **Gradio版本**: {gr.__version__}
                - **运行端口**: 7860
                
                ### 📈 功能状态
                1. ✅ 单股票风险分析
                2. ⚠️ 批量股票分析 (开发中)
                3. ⚠️ 投资组合分析 (开发中)
                4. ✅ 实时数据获取
                
                ### 🌐 访问信息
                - **本地地址**: http://localhost:7860
                - **项目路径**: {os.getcwd()}
                - **API状态**: 运行中
                
                ---
                
                **🔧 故障排除:**
                1. 如果股票分析失败，请运行: pip install yfinance pandas numpy
                2. 如果无法访问，请检查防火墙设置
                3. 确保网络连接正常
                
                **⚠️ 免责声明:**
                本系统提供的数据和分析仅供参考，不构成投资建议。
                股市有风险，投资需谨慎。
                """)
        
        # 页脚
        gr.Markdown("---")
        with gr.Row():
            gr.Markdown(f"""
            **📁 项目路径**: {os.getcwd()}  
            **🕐 当前时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
            **🚀 版本**: 2.1 完全兼容版 | **🔒 环境**: 开发模式
            """)
    
    return demo

# ============================================================================
# 主函数
# ============================================================================
def main():
    """主启动函数"""
    
    # 创建界面
    print("🔄 正在创建 Gradio 界面...")
    app = create_interface()
    
    # 启动参数
    launch_params = {
        "server_name": "0.0.0.0",
        "server_port": 7860,
        "share": False,
        "show_error": True,
        "inbrowser": True,
        "quiet": False
    }
    
    print("🌐 启动参数配置完成")
    print("=" * 70)
    print("✅ 应用准备就绪!")
    print(f"📡 本地访问: http://localhost:{launch_params['server_port']}")
    print(f"🌍 网络访问: http://{launch_params['server_name']}:{launch_params['server_port']}")
    print("=" * 70)
    print("🖱️ 按 Ctrl+C 停止应用")
    print("=" * 70)
    
    try:
        # 启动应用
        app.launch(**launch_params)
    except KeyboardInterrupt:
        print("\n👋 应用已由用户停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        print("尝试以下解决方案:")
        print("1. 检查端口 7860 是否被占用")
        print("2. 以管理员权限运行")
        print("3. 尝试其他端口: python src/app.py --port 7865")

if __name__ == "__main__":
    main()
