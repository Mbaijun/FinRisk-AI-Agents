# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="FinRisk AI Agents",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-low { color: #10B981; font-weight: bold; }
    .risk-medium { color: #F59E0B; font-weight: bold; }
    .risk-high { color: #EF4444; font-weight: bold; }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown('<h1 class="main-header">📊 FinRisk AI Agents</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">智能金融风险分析系统 | 离线模拟模式</p>', unsafe_allow_html=True)

# 初始化
API_URL = "http://localhost:8000"

# 侧边栏
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/stock-share.png", width=80)
    st.title("⚙️ 配置面板")
    
    # 分析模式选择
    analysis_mode = st.selectbox(
        "选择分析模式",
        ["📊 投资组合分析", "🎯 风险评分", "🎲 蒙特卡洛模拟"]
    )
    
    # 获取常用股票
    try:
        response = requests.get(f"{API_URL}/symbols/popular", timeout=2)
        popular_symbols = response.json().get("symbols", [])
    except:
        popular_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA"]
    
    st.subheader("📈 选择股票")
    symbols = st.multiselect(
        "选择股票代码（支持多选）",
        popular_symbols,
        default=["AAPL", "MSFT", "GOOGL"]
    )
    
    if not symbols:
        st.warning("⚠️ 请选择至少一支股票")
        st.stop()
    
    # 权重设置
    st.subheader("⚖️ 配置权重")
    st.info("调整每支股票的权重百分比")
    
    weights = []
    cols = st.columns(min(len(symbols), 3))
    for i, symbol in enumerate(symbols):
        col_idx = i % 3
        with cols[col_idx]:
            default_weight = 100 // len(symbols)
            weight = st.slider(
                f"{symbol}",
                min_value=0,
                max_value=100,
                value=default_weight,
                key=f"weight_{i}"
            )
            weights.append(weight)
    
    # 标准化权重
    total_weight = sum(weights)
    if total_weight > 0:
        weights = [w/total_weight for w in weights]
    
    # 显示权重总结
    weight_summary = ", ".join([f"{symbol}: {weight*100:.0f}%" 
                              for symbol, weight in zip(symbols, weights)])
    st.caption(f"📋 权重分配: {weight_summary}")
    
    # 分析参数
    st.subheader("⚙️ 分析参数")
    
    if analysis_mode == "📊 投资组合分析":
        days = st.slider("历史数据天数", 30, 1000, 252, help="使用多少天的历史数据进行分析")
    
    elif analysis_mode == "🎲 蒙特卡洛模拟":
        col1, col2 = st.columns(2)
        with col1:
            initial_investment = st.number_input(
                "初始投资 ($)", 
                min_value=1000, 
                max_value=1000000, 
                value=10000,
                step=1000
            )
        with col2:
            simulations = st.selectbox(
                "模拟次数", 
                [1000, 5000, 10000, 20000, 50000], 
                index=2
            )
        sim_days = st.slider("预测天数", 10, 365, 30)

# 主内容区
if analysis_mode == "📊 投资组合分析":
    st.header("📊 投资组合分析")
    
    # 投资组合概览
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 权重饼图
        fig_pie = go.Figure(data=[go.Pie(
            labels=symbols,
            values=[w*100 for w in weights],
            hole=0.4,
            textinfo='label+percent',
            marker=dict(colors=px.colors.qualitative.Set3)
        )])
        fig_pie.update_layout(
            title="投资组合权重分布",
            height=400,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("📋 组合详情")
        df_weights = pd.DataFrame({
            '股票': symbols,
            '权重': [f"{w:.1%}" for w in weights],
            '数值权重': weights
        })
        st.dataframe(df_weights[['股票', '权重']], use_container_width=True, hide_index=True)
        
        # 风险多样性指示器
        if len(symbols) >= 3:
            st.success(f"✅ 分散投资: {len(symbols)} 支股票")
        elif len(symbols) == 2:
            st.warning(f"⚠️ 中度集中: {len(symbols)} 支股票")
        else:
            st.error(f"❌ 高度集中: 只有 {len(symbols)} 支股票")
    
    # 分析按钮
    if st.button("🚀 开始风险分析", type="primary", use_container_width=True):
        with st.spinner("正在分析投资组合风险..."):
            try:
                # 调用API
                response = requests.post(
                    f"{API_URL}/analyze/portfolio",
                    json={
                        "symbols": symbols,
                        "weights": weights,
                        "days": days
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get('success'):
                        st.success("✅ 分析完成！")
                        
                        # 显示关键指标
                        st.subheader("📈 关键风险指标")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            vol = result.get('volatility', 0)
                            st.metric(
                                "波动率",
                                f"{vol:.2%}",
                                help="年化波动率，衡量价格波动程度"
                            )
                        
                        with col2:
                            sharpe = result.get('sharpe_ratio', 0)
                            st.metric(
                                "夏普比率",
                                f"{sharpe:.2f}",
                                delta="优秀" if sharpe > 1 else "一般" if sharpe > 0 else "较差",
                                help="风险调整后收益"
                            )
                        
                        with col3:
                            var_95 = result.get('var_95', 0)
                            st.metric(
                                "VaR (95%)",
                                f"{var_95:.2%}",
                                delta_color="inverse",
                                help="在95%置信度下最大单日损失"
                            )
                        
                        with col4:
                            max_dd = result.get('max_drawdown', 0)
                            st.metric(
                                "最大回撤",
                                f"{max_dd:.2%}",
                                delta_color="inverse",
                                help="历史最大跌幅"
                            )
                        
                        # 更多指标
                        col5, col6, col7, col8 = st.columns(4)
                        
                        with col5:
                            beta = result.get('beta', 0)
                            st.metric(
                                "Beta系数",
                                f"{beta:.2f}",
                                delta="高波动" if beta > 1.2 else "低波动" if beta < 0.8 else "市场一致",
                                help="相对于市场的波动性"
                            )
                        
                        with col6:
                            skew = result.get('skewness', 0)
                            st.metric(
                                "偏度",
                                f"{skew:.2f}",
                                delta="右偏" if skew > 0.2 else "左偏" if skew < -0.2 else "对称",
                                help="收益分布的不对称性"
                            )
                        
                        with col7:
                            info_ratio = result.get('information_ratio', 0)
                            st.metric(
                                "信息比率",
                                f"{info_ratio:.2f}",
                                delta="优秀" if info_ratio > 0.5 else "一般",
                                help="主动管理能力"
                            )
                        
                        with col8:
                            data_pts = result.get('data_points', 0)
                            st.metric(
                                "数据点数",
                                f"{data_pts}",
                                help="分析使用的数据点数量"
                            )
                        
                        # 相关性热图
                        st.subheader("🔄 相关性分析")
                        corr_matrix = pd.DataFrame(result.get('correlation_matrix', {}))
                        
                        fig_heatmap = go.Figure(data=go.Heatmap(
                            z=corr_matrix.values,
                            x=corr_matrix.columns,
                            y=corr_matrix.index,
                            text=np.round(corr_matrix.values, 2),
                            texttemplate='%{text}',
                            textfont={"size": 12},
                            colorscale='RdBu_r',
                            zmin=-1,
                            zmax=1,
                            colorbar=dict(title="相关系数")
                        ))
                        
                        fig_heatmap.update_layout(
                            height=500,
                            title="股票相关性矩阵",
                            xaxis_title="",
                            yaxis_title=""
                        )
                        
                        st.plotly_chart(fig_heatmap, use_container_width=True)
                        
                        # 风险评分
                        st.subheader("🎯 风险综合评分")
                        
                        risk_response = requests.post(
                            f"{API_URL}/analyze/risk-score",
                            json={
                                "symbols": symbols,
                                "weights": weights
                            }
                        )
                        
                        if risk_response.status_code == 200:
                            risk_result = risk_response.json()
                            
                            if risk_result.get('success'):
                                risk_score = risk_result.get('risk_score', 0)
                                risk_level = risk_result.get('risk_level', '未知')
                                risk_color = risk_result.get('risk_color', '#6B7280')
                                
                                # 风险评分仪表盘
                                col_left, col_right = st.columns([1, 2])
                                
                                with col_left:
                                    # 仪表盘
                                    fig_gauge = go.Figure(go.Indicator(
                                        mode="gauge+number",
                                        value=risk_score,
                                        domain={'x': [0, 1], 'y': [0, 1]},
                                        title={'text': "风险评分", 'font': {'size': 24}},
                                        number={'font': {'size': 40, 'color': risk_color}},
                                        gauge={
                                            'axis': {'range': [0, 10], 'tickwidth': 1},
                                            'bar': {'color': risk_color, 'thickness': 0.3},
                                            'bgcolor': "white",
                                            'borderwidth': 2,
                                            'bordercolor': "gray",
                                            'steps': [
                                                {'range': [0, 3], 'color': '#D1FAE5'},
                                                {'range': [3, 6], 'color': '#FEF3C7'},
                                                {'range': [6, 10], 'color': '#FEE2E2'}
                                            ],
                                            'threshold': {
                                                'line': {'color': "black", 'width': 4},
                                                'thickness': 0.75,
                                                'value': risk_score
                                            }
                                        }
                                    ))
                                    
                                    fig_gauge.update_layout(
                                        height=300,
                                        margin=dict(l=20, r=20, t=50, b=20)
                                    )
                                    
                                    st.plotly_chart(fig_gauge, use_container_width=True)
                                
                                with col_right:
                                    # 风险等级和建议
                                    st.markdown(f"### 风险等级: **{risk_level}**")
                                    
                                    # 风险分解
                                    components = risk_result.get('components', {})
                                    df_components = pd.DataFrame({
                                        '风险类型': ['波动率风险', '回撤风险', 'VaR风险', '偏度风险', '峰度风险'],
                                        '评分': [
                                            components.get('volatility_score', 0),
                                            components.get('drawdown_score', 0),
                                            components.get('var_score', 0),
                                            components.get('skewness_score', 0),
                                            components.get('kurtosis_score', 0)
                                        ]
                                    })
                                    
                                    fig_bar = px.bar(
                                        df_components,
                                        x='风险类型',
                                        y='评分',
                                        color='评分',
                                        color_continuous_scale=[(0, "green"), (0.5, "yellow"), (1, "red")],
                                        range_color=[0, 10],
                                        text_auto='.1f'
                                    )
                                    fig_bar.update_layout(
                                        height=300,
                                        title="风险分解分析",
                                        xaxis_title="",
                                        yaxis_title="评分",
                                        showlegend=False
                                    )
                                    
                                    st.plotly_chart(fig_bar, use_container_width=True)
                                    
                                    # 投资建议
                                    st.subheader("💡 投资建议")
                                    recommendations = risk_result.get('recommendations', [])
                                    for rec in recommendations:
                                        st.info(f"• {rec}")
                        
                    else:
                        st.error(f"分析失败: {result.get('error', '未知错误')}")
                
                else:
                    st.error(f"API请求失败: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ 无法连接到API服务")
                st.info("请确保已启动API服务，运行: `python -m uvicorn finrisk_ai.api:app`")
            except Exception as e:
                st.error(f"分析过程出错: {str(e)}")

elif analysis_mode == "🎯 风险评分":
    st.header("🎯 风险评分分析")
    
    st.info("风险评分系统综合考虑波动率、回撤、VaR等多个维度，给出0-10分的风险评分")
    
    if st.button("📊 计算风险评分", type="primary", use_container_width=True):
        with st.spinner("正在计算综合风险评分..."):
            try:
                response = requests.post(
                    f"{API_URL}/analyze/risk-score",
                    json={
                        "symbols": symbols,
                        "weights": weights
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get('success'):
                        risk_score = result.get('risk_score', 0)
                        risk_level = result.get('risk_level', '未知')
                        risk_color = result.get('risk_color', '#6B7280')
                        
                        # 顶部展示
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                            st.metric("综合风险评分", f"{risk_score:.1f}/10.0")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                            st.markdown(f"### 风险等级")
                            if risk_level == "低风险":
                                st.markdown('<h1 class="risk-low">🟢 低风险</h1>', unsafe_allow_html=True)
                            elif risk_level == "中风险":
                                st.markdown('<h1 class="risk-medium">🟡 中风险</h1>', unsafe_allow_html=True)
                            else:
                                st.markdown('<h1 class="risk-high">🔴 高风险</h1>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        with col3:
                            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                            st.markdown("### 适合投资者")
                            if risk_level == "低风险":
                                st.markdown("**保守型投资者**")
                                st.caption("风险承受能力较低")
                            elif risk_level == "中风险":
                                st.markdown("**平衡型投资者**")
                                st.caption("中等风险承受能力")
                            else:
                                st.markdown("**激进型投资者**")
                                st.caption("高风险承受能力")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # 详细分析
                        st.subheader("📊 风险分解")
                        
                        components = result.get('components', {})
                        
                        # 创建雷达图
                        categories = ['波动率', '回撤', 'VaR', '偏度', '峰度']
                        values = [
                            components.get('volatility_score', 0),
                            components.get('drawdown_score', 0),
                            components.get('var_score', 0),
                            components.get('skewness_score', 0),
                            components.get('kurtosis_score', 0)
                        ]
                        
                        fig_radar = go.Figure(data=go.Scatterpolar(
                            r=values + [values[0]],  # 闭合图形
                            theta=categories + [categories[0]],
                            fill='toself',
                            name='风险评分',
                            line=dict(color=risk_color, width=3)
                        ))
                        
                        fig_radar.update_layout(
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[0, 10]
                                )
                            ),
                            showlegend=False,
                            height=400,
                            title="风险维度雷达图"
                        )
                        
                        st.plotly_chart(fig_radar, use_container_width=True)
                        
                        # 投资建议
                        st.subheader("💡 投资建议")
                        recommendations = result.get('recommendations', [])
                        
                        for i, rec in enumerate(recommendations, 1):
                            st.success(f"{i}. {rec}")
                        
                        # 风险对比
                        st.subheader("📈 风险对比参考")
                        
                        risk_comparison = pd.DataFrame({
                            '风险等级': ['极低风险', '低风险', '中风险', '高风险', '极高风险'],
                            '评分范围': ['0-2', '2-4', '4-6', '6-8', '8-10'],
                            '典型投资': [
                                '国债、货币基金',
                                '蓝筹股、高评级债券',
                                '混合型基金、ETF',
                                '科技股、新兴市场',
                                '加密货币、杠杆产品'
                            ]
                        })
                        
                        st.dataframe(risk_comparison, use_container_width=True, hide_index=True)
                    
                    else:
                        st.error(f"计算失败: {result.get('error', '未知错误')}")
                
                else:
                    st.error(f"API请求失败: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ 无法连接到API服务")
            except Exception as e:
                st.error(f"计算过程出错: {str(e)}")

elif analysis_mode == "🎲 蒙特卡洛模拟":
    st.header("🎲 蒙特卡洛模拟")
    
    st.info(f"""
    **蒙特卡洛模拟说明:**
    - 将对 **{len(symbols)}支股票** 进行 **{simulations:,}次** 模拟
    - 预测 **{sim_days}个交易日** 后的投资价值
    - 基于历史波动率和相关性生成随机路径
    """)
    
    if st.button("🎯 开始模拟预测", type="primary", use_container_width=True):
        with st.spinner(f"正在进行蒙特卡洛模拟 ({simulations:,}次)..."):
            try:
                response = requests.post(
                    f"{API_URL}/simulate/monte-carlo",
                    json={
                        "symbols": symbols,
                        "initial_investment": initial_investment,
                        "simulations": simulations,
                        "days": sim_days
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get('success'):
                        st.success("✅ 模拟完成！")
                        
                        # 关键结果
                        st.subheader("📊 模拟结果概览")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            mean_value = result.get('mean_final_value', initial_investment)
                            expected_return = (mean_value - initial_investment) / initial_investment
                            st.metric(
                                "预期最终价值",
                                f"${mean_value:,.0f}",
                                f"{expected_return:.1%}",
                                help="所有模拟路径的平均结果"
                            )
                        
                        with col2:
                            var_95 = result.get('var_95', initial_investment)
                            var_loss = (var_95 - initial_investment) / initial_investment
                            st.metric(
                                "VaR (95%)",
                                f"${var_95:,.0f}",
                                f"{var_loss:.1%}",
                                delta_color="inverse",
                                help="95%置信度下的最差情况"
                            )
                        
                        with col3:
                            prob_loss = result.get('probability_loss', 0)
                            st.metric(
                                "亏损概率",
                                f"{prob_loss:.1%}",
                                delta_color="inverse",
                                help="最终价值低于初始投资的概率"
                            )
                        
                        with col4:
                            prob_gain_10 = result.get('probability_gain_10', 0)
                            st.metric(
                                "盈利10%+概率",
                                f"{prob_gain_10:.1%}",
                                delta="良好" if prob_gain_10 > 0.5 else "一般",
                                help="获得10%以上收益的概率"
                            )
                        
                        # 更多指标
                        col5, col6, col7, col8 = st.columns(4)
                        
                        with col5:
                            cvar_95 = result.get('cvar_95', initial_investment)
                            cvar_loss = (cvar_95 - initial_investment) / initial_investment
                            st.metric(
                                "CVaR (95%)",
                                f"${cvar_95:,.0f}",
                                f"{cvar_loss:.1%}",
                                delta_color="inverse",
                                help="最差5%情况的平均损失"
                            )
                        
                        with col6:
                            best_case = result.get('best_case', initial_investment)
                            best_return = (best_case - initial_investment) / initial_investment
                            st.metric(
                                "最佳情况",
                                f"${best_case:,.0f}",
                                f"{best_return:.1%}",
                                help="所有模拟中的最好结果"
                            )
                        
                        with col7:
                            worst_case = result.get('worst_case', initial_investment)
                            worst_return = (worst_case - initial_investment) / initial_investment
                            st.metric(
                                "最差情况",
                                f"${worst_case:,.0f}",
                                f"{worst_return:.1%}",
                                delta_color="inverse",
                                help="所有模拟中的最差结果"
                            )
                        
                        with col8:
                            conf_95 = result.get('confidence_95', [initial_investment, initial_investment])
                            st.metric(
                                "95%置信区间",
                                f"${conf_95[0]:,.0f}-{conf_95[1]:,.0f}",
                                help="95%模拟结果落在此区间"
                            )
                        
                        # 分布图
                        st.subheader("📈 投资价值分布")
                        
                        # 生成模拟数据用于可视化
                        np.random.seed(42)
                        mean_return = result.get('expected_return', 0)
                        std_return = result.get('std_final_value', 0) / initial_investment
                        
                        # 生成模拟值
                        simulated_returns = np.random.normal(mean_return, std_return, 10000)
                        simulated_values = initial_investment * (1 + simulated_returns)
                        
                        # 直方图
                        fig_dist = px.histogram(
                            x=simulated_values,
                            nbins=50,
                            title="最终投资价值分布",
                            labels={'x': '投资价值 ($)', 'y': '频率'},
                            color_discrete_sequence=['#6366F1']
                        )
                        
                        # 添加参考线
                        fig_dist.add_vline(
                            x=mean_value,
                            line_dash="dash",
                            line_color="green",
                            annotation_text=f"均值: ${mean_value:,.0f}",
                            annotation_position="top right"
                        )
                        
                        fig_dist.add_vline(
                            x=var_95,
                            line_dash="dash",
                            line_color="red",
                            annotation_text=f"VaR(95%): ${var_95:,.0f}",
                            annotation_position="top left"
                        )
                        
                        fig_dist.add_vline(
                            x=initial_investment,
                            line_dash="solid",
                            line_color="black",
                            annotation_text=f"初始: ${initial_investment:,.0f}",
                            annotation_position="bottom right"
                        )
                        
                        fig_dist.update_layout(
                            height=500,
                            showlegend=False,
                            bargap=0.1
                        )
                        
                        st.plotly_chart(fig_dist, use_container_width=True)
                        
                        # 概率分析
                        st.subheader("🎯 概率分析")
                        
                        # 创建概率表
                        probability_data = {
                            '情景': [
                                '亏损超过20%',
                                '亏损超过10%',
                                '发生亏损',
                                '盈亏平衡',
                                '盈利超过5%',
                                '盈利超过10%',
                                '盈利超过20%',
                                '盈利超过30%'
                            ],
                            '概率': [
                                np.mean(simulated_values < initial_investment * 0.8),
                                np.mean(simulated_values < initial_investment * 0.9),
                                np.mean(simulated_values < initial_investment),
                                np.mean(simulated_values == initial_investment),
                                np.mean(simulated_values > initial_investment * 1.05),
                                np.mean(simulated_values > initial_investment * 1.10),
                                np.mean(simulated_values > initial_investment * 1.20),
                                np.mean(simulated_values > initial_investment * 1.30)
                            ]
                        }
                        
                        df_prob = pd.DataFrame(probability_data)
                        df_prob['概率'] = df_prob['概率'].apply(lambda x: f"{x:.1%}")
                        
                        st.dataframe(df_prob, use_container_width=True, hide_index=True)
                        
                        # 投资建议
                        st.subheader("💡 模拟结果建议")
                        
                        if prob_loss > 0.3:
                            st.warning("⚠️ **高风险警告**: 亏损概率较高，建议:")
                            st.markdown("""
                            - 降低高风险资产配置
                            - 增加止损机制
                            - 考虑对冲策略
                            """)
                        elif expected_return > 0.15:
                            st.success("✅ **高收益机会**: 预期收益良好，建议:")
                            st.markdown("""
                            - 可以适度增加投资
                            - 设置止盈点
                            - 定期再平衡
                            """)
                        else:
                            st.info("📊 **稳健配置**: 风险收益平衡，建议:")
                            st.markdown("""
                            - 保持当前配置
                            - 定期监控
                            - 考虑定投策略
                            """)
                    
                    else:
                        st.error(f"模拟失败: {result.get('error', '未知错误')}")
                
                else:
                    st.error(f"API请求失败: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ 无法连接到API服务")
                st.info("请确保已启动API服务")
            except Exception as e:
                st.error(f"模拟过程出错: {str(e)}")

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #6B7280; font-size: 0.9rem;'>
    <p>FinRisk AI Agents v1.0.0 | 金融风险智能分析系统 | 离线模拟模式</p>
    <p>⚠️ 提示: 本系统使用模拟数据进行分析，实际投资请咨询专业顾问</p>
    </div>
    """,
    unsafe_allow_html=True
)