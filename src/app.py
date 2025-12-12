#!/usr/bin/env python3
"""
FinRisk AI Agents - 带速率限制处理的版本
解决 Yahoo Finance API 限制问题
"""

import gradio as gr
import sys
import os
import json
import time
import random
from datetime import datetime, timedelta
from functools import lru_cache

# ============================================================================
# 设置环境变量和缓存
# ============================================================================
os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"

print("=" * 70)
print("🚀 FinRisk AI Agents - 智能金融风险分析")
print("=" * 70)
print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Python版本: {sys.version.split()[0]}")
print("=" * 70)

# ============================================================================
# 带重试机制的股票数据获取
# ============================================================================
try:
    import yfinance as yf
    import pandas as pd
    import numpy as np
    
    STOCK_AVAILABLE = True
    print("✅ 股票分析模块已加载")
    
    # 缓存股票数据（5分钟）
    @lru_cache(maxsize=50)
    def get_cached_stock_data(ticker: str, period: str = "1mo") -> dict:
        """带缓存和重试的股票数据获取"""
        max_retries = 3
        base_delay = 2  # 基础延迟秒数
        
        for attempt in range(max_retries):
            try:
                # 添加随机延迟避免速率限制
                delay = base_delay + random.uniform(0, 3)
                print(f"🔄 获取 {ticker} 数据 (尝试 {attempt+1}/{max_retries}), 延迟: {delay:.1f}s")
                time.sleep(delay)
                
                stock = yf.Ticker(ticker)
                
                # 使用更保守的参数
                hist = stock.history(
                    period=period,
                    interval="1d",
                    prepost=False,  # 不获取盘前盘后数据
                    auto_adjust=True
                )
                
                info = {}
                try:
                    # 只获取必要信息，避免过多请求
                    info_keys = ['longName', 'sector', 'marketCap', 'currentPrice', 'regularMarketPrice']
                    for key in info_keys:
                        if key in stock.info:
                            info[key] = stock.info[key]
                except:
                    info = {'longName': ticker}
                
                return {
                    'success': True,
                    'history': hist,
                    'info': info,
                    'ticker': ticker
                }
                
            except Exception as e:
                error_msg = str(e)
                print(f"⚠️ 尝试 {attempt+1} 失败: {error_msg}")
                
                if "rate limit" in error_msg.lower() or "too many" in error_msg.lower():
                    # 如果是速率限制，增加延迟
                    wait_time = base_delay * (attempt + 2) + random.uniform(0, 5)
                    print(f"⏳ 速率限制，等待 {wait_time:.1f} 秒...")
                    time.sleep(wait_time)
                elif attempt < max_retries - 1:
                    time.sleep(base_delay)
                else:
                    return {
                        'success': False,
                        'error': error_msg,
                        'ticker': ticker
                    }
        
        return {
            'success': False,
            'error': f'获取 {ticker} 数据失败，请稍后重试',
            'ticker': ticker
        }
    
except ImportError as e:
    STOCK_AVAILABLE = False
    print(f"⚠️ 部分依赖缺失: {e}")

# ============================================================================
# 改进的分析函数
# ============================================================================
def analyze_stock_safe(ticker: str, period: str = "1mo") -> str:
    """安全的股票分析函数，处理速率限制"""
    if not STOCK_AVAILABLE:
        return "❌ 请安装依赖: pip install yfinance pandas numpy"
    
    ticker = ticker.strip().upper()
    if not ticker:
        return "⚠️ 请输入股票代码"
    
    # 常见股票映射（减少 API 调用）
    stock_db = {
        "AAPL": {"name": "苹果公司", "sector": "科技"},
        "MSFT": {"name": "微软公司", "sector": "科技"},
        "GOOGL": {"name": "谷歌(Alphabet)", "sector": "科技"},
        "TSLA": {"name": "特斯拉", "sector": "汽车"},
        "NVDA": {"name": "英伟达", "sector": "半导体"},
        "AMZN": {"name": "亚马逊", "sector": "电商"},
        "META": {"name": "Meta(Facebook)", "sector": "科技"},
        "000001.SZ": {"name": "平安银行", "sector": "金融"},
        "0700.HK": {"name": "腾讯控股", "sector": "科技"},
    }
    
    # 先从缓存/数据库获取基本信息
    stock_info = stock_db.get(ticker, {"name": ticker, "sector": "未知"})
    
    try:
        # 获取数据（带重试和缓存）
        data = get_cached_stock_data(ticker, period)
        
        if not data.get('success', False):
            error_msg = data.get('error', '未知错误')
            
            # 返回带缓存的友好信息
            return f"""
## 📊 {ticker} - {stock_info['name']}

**⚠️ 数据获取受限**

**错误信息**: {error_msg}

**可能原因**:
1. Yahoo Finance API 临时限制
2. 网络连接问题
3. 股票代码暂时不可用

**建议操作**:
1. 等待 1-2 分钟后重试
2. 尝试其他股票代码
3. 检查网络连接

**离线信息**:
- **公司**: {stock_info['name']}
- **行业**: {stock_info['sector']}
- **状态**: 数据获取受限，请稍后重试

---
*提示: 这是常见的 API 限制问题，通常几分钟后会自动恢复*
"""
        
        # 数据处理
        hist = data['history']
        info = data['info']
        
        if hist.empty:
            return f"❌ 未找到 {ticker} 的历史数据"
        
        # 计算指标
        if len(hist) > 0:
            current_price = float(hist['Close'].iloc[-1])
            price_str = f""
            
            if len(hist) > 1:
                prev_price = float(hist['Close'].iloc[-2])
                change_pct = ((current_price / prev_price) - 1) * 100
                change_str = f"{'📈' if change_pct > 0 else '📉'} {change_pct:+.2f}%"
                
                # 简单风险计算
                returns = hist['Close'].pct_change().dropna()
                if len(returns) > 1:
                    volatility = returns.std() * (252 ** 0.5)
                    risk_score = min(10, volatility * 8)
                else:
                    volatility = 0
                    risk_score = 5
            else:
                change_str = "数据不足"
                risk_score = 5
                volatility = 0
        else:
            price_str = "数据不足"
            change_str = "数据不足"
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
## 📊 {ticker} - {stock_info['name']}

### 💰 价格信息
- **当前价格**: {price_str}
- **价格变动**: {change_str}
- **分析周期**: {period}

### ⚠️ 风险分析
- **风险评分**: {risk_score:.1f}/10
- **风险等级**: {risk_level}
- **波动率**: {volatility*100:.2f}% (年化)

### 🏢 公司信息
- **公司名称**: {info.get('longName', stock_info['name'])}
- **所属行业**: {info.get('sector', stock_info['sector'])}
- **市值**: 

### 🎯 投资建议
{suggestion}

---
*分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*数据来源: Yahoo Finance (可能受速率限制)*
"""
        return result
        
    except Exception as e:
        return f"""
## ❌ 分析异常

**股票**: {ticker}
**错误**: {str(e)}

**即时建议**:
1. 点击右侧的 **"⚙️ 系统信息"** 标签页
2. 使用下面的 **"🧪 离线测试"** 功能
3. 或等待几分钟后重试

**常见解决方案**:
- Yahoo Finance 限制: 等待 1-5 分钟
- 网络问题: 检查网络连接
- 代码问题: 确保使用正确格式 (AAPL, 000001.SZ)
"""

# ============================================================================
# 创建界面
# ============================================================================
def create_app():
    """创建应用界面"""
    
    with gr.Blocks() as demo:
        # 样式
        gr.Markdown("""
        <style>
        .gradio-container { max-width: 1200px; margin: 0 auto; }
        .title-header {
            text-align: center;
            padding: 20px;
            background: linear-gradient(90deg, #1a237e, #283593);
            color: white;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .offline-test {
            background: #e8f5e9;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #4caf50;
            margin: 10px 0;
        }
        .rate-limit-note {
            background: #fff3e0;
            padding: 10px;
            border-radius: 5px;
            border-left: 5px solid #ff9800;
            font-size: 0.9em;
            margin: 10px 0;
        }
        </style>
        
        <div class="title-header">
            <h1>🚀 FinRisk AI Agents</h1>
            <h3>智能金融风险分析系统 | 版本 2.1 (带速率限制处理)</h3>
        </div>
        """)
        
        with gr.Tabs():
            # 主分析页面
            with gr.TabItem("📈 股票分析"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 🔍 输入股票信息")
                        
                        ticker_input = gr.Textbox(
                            label="股票代码",
                            placeholder="例如: AAPL, MSFT, 000001.SZ",
                            value="AAPL",
                        )
                        
                        period_select = gr.Dropdown(
                            choices=["1d", "5d", "1mo", "3mo"],
                            value="1mo",
                            label="分析周期 (短期减少限制)"
                        )
                        
                        gr.Markdown("""
                        <div class="rate-limit-note">
                        ⚠️ <strong>注意</strong>: Yahoo Finance 有 API 限制<br>
                        📌 建议: 每次分析间隔 5-10 秒<br>
                        🔄 如遇限制: 等待 1-2 分钟自动恢复
                        </div>
                        """)
                        
                        gr.Markdown("### ⚡ 推荐测试")
                        with gr.Row():
                            test_btns = []
                            for stock in ["AAPL", "MSFT", "TSLA", "NVDA"]:
                                btn = gr.Button(stock, size="sm", variant="secondary")
                                btn.click(lambda s=stock: s, outputs=ticker_input)
                                test_btns.append(btn)
                        
                        analyze_btn = gr.Button("🚀 开始分析", variant="primary")
                        
                        # 离线测试功能
                        gr.Markdown("""
                        <div class="offline-test">
                        ### 🧪 离线测试 (无API限制)
                        当遇到速率限制时，可以使用离线演示
                        </div>
                        """)
                        
                        offline_btn = gr.Button("📱 运行离线演示", variant="secondary")
                        
                        gr.Markdown("### 📋 示例")
                        gr.Examples(
                            examples=[["AAPL"], ["MSFT"], ["GOOGL"], ["TSLA"], ["000001.SZ"]],
                            inputs=ticker_input,
                            label="点击使用"
                        )
                    
                    with gr.Column(scale=2):
                        gr.Markdown("### 📊 分析结果")
                        result_output = gr.Markdown("""
                        <div class="rate-limit-note">
                        👈 **请输入股票代码并点击分析**
                        
                        **💡 使用技巧**:
                        1. 首次分析可能需要几秒钟
                        2. 如遇限制，请等待片刻重试
                        3. 可使用右侧的离线演示功能
                        4. 建议分析间隔 10 秒以上
                        </div>
                        """)
                
                # 事件绑定
                analyze_btn.click(
                    fn=analyze_stock_safe,
                    inputs=[ticker_input, period_select],
                    outputs=result_output
                )
                
                ticker_input.submit(
                    fn=analyze_stock_safe,
                    inputs=[ticker_input, period_select],
                    outputs=result_output
                )
                
                # 离线演示
                def offline_demo():
                    return """
## 📱 离线演示模式

### 💰 模拟股票分析 (AAPL)
- **当前价格**: .35
- **今日涨跌**: 📈 +1.25%
- **分析周期**: 1个月

### ⚠️ 风险分析
- **风险评分**: 6.5/10
- **风险等级**: 🟡 中风险
- **波动率**: 28.5% (年化)

### 🏢 公司信息
- **公司名称**: Apple Inc.
- **所属行业**: 科技
- **市值**: .65T

### 🎯 投资建议
适合适度配置，建议作为核心科技股持有，注意市场波动风险。

---
*这是离线演示数据，实际数据受 Yahoo Finance API 限制*
*如需实时数据，请等待 API 限制解除后重试*
"""
                
                offline_btn.click(
                    fn=offline_demo,
                    outputs=result_output
                )
            
            # 系统信息页面
            with gr.TabItem("⚙️ 系统信息"):
                gr.Markdown(f"""
                <div class="rate-limit-note">
                ## 🖥️ 系统状态
                
                **状态报告**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                
                ### ✅ 运行正常
                - **应用状态**: 已启动
                - **界面功能**: 正常
                - **Gradio版本**: {gr.__version__}
                
                ### ⚠️ 已知限制
                - **Yahoo Finance API**: 有速率限制 (非程序问题)
                - **数据获取**: 可能间歇性失败
                - **恢复时间**: 通常 1-5 分钟
                
                ### 🔧 解决方案
                1. **等待重试**: 限制通常很快解除
                2. **使用离线演示**: 点击左侧的"离线演示"按钮
                3. **更换股票**: 尝试不同的股票代码
                4. **延长间隔**: 每次请求间隔 10+ 秒
                
                ### 📞 技术支持
                - **问题**: "Too Many Requests" 错误
                - **原因**: Yahoo Finance 的 API 限制
                - **解决**: 内置了重试和缓存机制
                - **备用**: 离线演示功能可用
                
                ---
                
                **💡 专业建议**:
                对于生产环境，建议:
                1. 使用付费金融数据 API
                2. 搭建本地数据缓存
                3. 使用多个数据源轮询
                </div>
                """)
        
        # 页脚
        gr.Markdown(f"""
        ---
        <div style="text-align: center; color: #666; font-size: 0.9em;">
        <strong>📁</strong> {os.getcwd()} | 
        <strong>🕐</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
        <strong>🔄</strong> 带速率限制处理
        </div>
        """)
    
    return demo

# ============================================================================
# 主函数
# ============================================================================
def main():
    """主启动函数"""
    print("🔄 启动 FinRisk AI Agents...")
    print("⚠️  注意: 已添加 API 速率限制处理")
    print("💡  提示: 如遇限制，请等待片刻或使用离线演示")
    
    app = create_app()
    
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=True,
        show_error=True
    )

if __name__ == "__main__":
    main()
