import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go

# 页面配置
st.set_page_config(
    page_title="FinRisk独立版",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 标题
st.title("📊 FinRisk AI Agents - 独立运行版")
st.markdown("**完全本地运行，无需额外服务**")

# 风险分析类
class StandaloneAnalyzer:
    def __init__(self):
        self.name = "独立风险分析器"
    
    def analyze(self, symbols, days=252):
        """分析投资组合"""
        try:
            # 生成模拟数据
            np.random.seed(42)
            end_date = datetime.now()
            dates = pd.date_range(end=end_date, periods=days, freq='B')
            
            # 生成价格数据
            data = {}
            base_prices = {'AAPL': 175, 'MSFT': 330, 'GOOGL': 135, 
                          'AMZN': 145, 'TSLA': 235, 'META': 325}
            
            for symbol in symbols:
                base = base_prices.get(symbol, 100)
                returns = np.random.normal(0.0005, 0.02, days)
                prices = base * np.exp(np.cumsum(returns))
                data[symbol] = pd.Series(prices, index=dates)
            
            prices_df = pd.DataFrame(data)
            returns = prices_df.pct_change().dropna()
            portfolio_returns = returns.mean(axis=1)  # 等权重
            
            # 计算指标
            vol = portfolio_returns.std() * np.sqrt(252)
            sharpe = portfolio_returns.mean() / portfolio_returns.std() * np.sqrt(252) if portfolio_returns.std() != 0 else 0
            var_95 = np.percentile(portfolio_returns, 5)
            
            # 最大回撤
            cumulative = (1 + portfolio_returns).cumprod()
            peak = cumulative.expanding(min_periods=1).max()
            drawdown = (cumulative - peak) / peak
            max_dd = drawdown.min()
            
            # 风险评分
            risk_score = min(vol * 100, 10)
            if risk_score < 3:
                risk_level = "🟢 低风险"
            elif risk_score < 6:
                risk_level = "🟡 中风险"
            else:
                risk_level = "🔴 高风险"
            
            return {
                'success': True,
                'symbols': symbols,
                'volatility': float(vol),
                'sharpe_ratio': float(sharpe),
                'var_95': float(var_95),
                'max_drawdown': float(max_dd),
                'risk_score': float(risk_score),
                'risk_level': risk_level,
                'prices': prices_df,
                'returns': portfolio_returns,
                'data_points': len(prices_df)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

# 侧边栏
with st.sidebar:
    st.header("⚙️ 配置面板")
    
    symbols = st.multiselect(
        "选择股票代码",
        ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM", "JNJ"],
        default=["AAPL", "MSFT", "GOOGL"]
    )
    
    if not symbols:
        st.warning("请选择至少一支股票")
        st.stop()
    
    days = st.slider("分析天数", 30, 1000, 252)

# 主界面
analyzer = StandaloneAnalyzer()

if st.button("🚀 开始风险分析", type="primary", use_container_width=True):
    with st.spinner("正在分析中..."):
        result = analyzer.analyze(symbols, days)
        
        if result['success']:
            st.success("✅ 分析完成！")
            
            # 显示指标
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("波动率", f"{result['volatility']:.2%}")
            
            with col2:
                st.metric("夏普比率", f"{result['sharpe_ratio']:.2f}")
            
            with col3:
                st.metric("VaR (95%)", f"{result['var_95']:.2%}")
            
            with col4:
                st.metric("最大回撤", f"{result['max_drawdown']:.2%}")
            
            # 价格图表
            st.subheader("📈 价格走势")
            st.line_chart(result['prices'])
            
            # 风险评分
            st.subheader("🎯 风险评分")
            
            col_left, col_right = st.columns([1, 2])
            
            with col_left:
                # 仪表盘
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=result['risk_score'],
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "风险评分"},
                    gauge={
                        'axis': {'range': [0, 10]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 3], 'color': "#10B981"},
                            {'range': [3, 6], 'color': "#F59E0B"},
                            {'range': [6, 10], 'color': "#EF4444"}
                        ]
                    }
                ))
                fig.update_layout(height=250)
                st.plotly_chart(fig, use_container_width=True)
            
            with col_right:
                st.markdown(f"### {result['risk_level']}")
                st.markdown(f"**综合评分:** {result['risk_score']:.1f}/10")
                
                # 建议
                st.markdown("#### 💡 投资建议")
                if result['risk_score'] < 3:
                    st.info("适合保守型投资者，当前配置风险较低")
                elif result['risk_score'] < 6:
                    st.warning("适合平衡型投资者，建议定期再平衡")
                else:
                    st.error("适合激进型投资者，建议设置止损点")
            
            st.info(f"分析基于 {result['data_points']} 个交易日数据")
            
        else:
            st.error(f"分析失败: {result.get('error', '未知错误')}")

# 页脚
st.divider()
st.caption("FinRisk AI Agents v1.0 | 独立版本 | 数据为模拟生成")
