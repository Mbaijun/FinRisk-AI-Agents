import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import time

# 页面配置
st.set_page_config(
    page_title="FinRisk AI Agents - 专业版",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API基础URL
API_BASE = "http://localhost:8000"

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
        font-size: 1.5rem;
        color: #3B82F6;
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #D1FAE5;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #10B981;
    }
    .warning-box {
        background-color: #FEF3C7;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #F59E0B;
    }
    .stButton>button {
        width: 100%;
        background-color: #3B82F6;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = None
if 'stocks_list' not in st.session_state:
    st.session_state.stocks_list = []

# ========== 工具函数 ==========
def check_api_health():
    """检查API健康状态"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except:
        return False, None

def load_stocks():
    """加载股票列表"""
    try:
        response = requests.get(f"{API_BASE}/stocks", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [(s['code'], s['name']) for s in data['stocks']]
    except:
        pass
    # 默认列表
    return [
        ("AAPL", "Apple Inc."),
        ("MSFT", "Microsoft Corporation"),
        ("GOOGL", "Alphabet Inc."),
        ("AMZN", "Amazon.com Inc."),
        ("TSLA", "Tesla Inc."),
        ("JPM", "JPMorgan Chase & Co."),
        ("JNJ", "Johnson & Johnson"),
        ("NVDA", "NVIDIA Corporation"),
        ("WMT", "Walmart Inc."),
        ("XOM", "Exxon Mobil Corporation")
    ]

def analyze_stock(stock_code, analysis_days):
    """分析单只股票"""
    payload = {
        "stock_code": stock_code,
        "analysis_days": analysis_days,
        "simulation_count": 10000
    }
    
    with st.spinner(f"正在分析 {stock_code}..."):
        try:
            response = requests.post(f"{API_BASE}/analyze", json=payload, timeout=30)
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, f"API错误: {response.status_code}"
        except Exception as e:
            return False, f"连接错误: {str(e)}"

def analyze_portfolio(stocks, weights, days):
    """分析投资组合"""
    payload = {
        "stocks": stocks,
        "weights": weights,
        "analysis_days": days
    }
    
    with st.spinner("正在分析投资组合..."):
        try:
            response = requests.post(f"{API_BASE}/analyze/portfolio", json=payload, timeout=30)
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, f"API错误: {response.status_code}"
        except Exception as e:
            return False, f"连接错误: {str(e)}"

# ========== 可视化函数 ==========
def create_returns_chart(data):
    """创建收益率图表"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('日收益率序列', '累计收益率', '回撤曲线', '收益分布'),
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    # 日收益率序列
    returns = data['simulated_data']['daily_returns']
    fig.add_trace(
        go.Scatter(y=returns, mode='lines', name='日收益率', line=dict(color='blue', width=1)),
        row=1, col=1
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=1)
    
    # 累计收益率
    cum_returns = data['simulated_data']['cumulative_returns']
    fig.add_trace(
        go.Scatter(y=cum_returns, mode='lines', name='累计收益', line=dict(color='green', width=2)),
        row=1, col=2
    )
    
    # 回撤曲线
    drawdown = data['simulated_data']['drawdown_series']
    fig.add_trace(
        go.Scatter(y=drawdown, mode='lines', name='回撤', fill='tozeroy', 
                  fillcolor='rgba(255,0,0,0.2)', line=dict(color='red', width=1)),
        row=2, col=1
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=1)
    
    # 收益分布
    dist_returns = data['simulated_data']['simulated_distribution']
    fig.add_trace(
        go.Histogram(x=dist_returns, nbinsx=50, name='收益分布', 
                    marker_color='purple', opacity=0.7),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    return fig

def create_metrics_display(metrics):
    """创建指标显示"""
    cols = st.columns(4)
    
    with cols[0]:
        st.metric("📈 年化收益率", f"{metrics['basic_metrics']['annual_return']}%")
        st.metric("📊 夏普比率", f"{metrics['basic_metrics']['sharpe_ratio']}")
    
    with cols[1]:
        st.metric("⚡ 年化波动率", f"{metrics['basic_metrics']['annual_volatility']}%")
        st.metric("🎯 索提诺比率", f"{metrics['basic_metrics']['sortino_ratio']}")
    
    with cols[2]:
        st.metric("⚠️ 最大回撤", f"{metrics['performance_metrics']['max_drawdown']}%")
        st.metric("🔄 95% VaR", f"{metrics['var_metrics']['var_95']}%")
    
    with cols[3]:
        st.metric("🔥 95% CVaR", f"{metrics['var_metrics']['cvar_95']}%")
        st.metric("📐 偏度", f"{metrics['distribution_stats']['skewness']}")

def create_portfolio_charts(data):
    """创建投资组合图表"""
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('组合成分权重', '相关性热图'),
        specs=[[{'type': 'pie'}, {'type': 'heatmap'}]]
    )
    
    # 饼图 - 权重分布
    fig.add_trace(
        go.Pie(labels=data['portfolio'], values=data['weights'], hole=0.3),
        row=1, col=1
    )
    
    # 热图 - 相关性矩阵
    corr_matrix = data['correlation_matrix']
    fig.add_trace(
        go.Heatmap(z=corr_matrix, x=data['portfolio'], y=data['portfolio'],
                  colorscale='RdBu', zmid=0),
        row=1, col=2
    )
    
    fig.update_layout(height=400)
    return fig

# ========== 主应用 ==========
def main():
    # 标题
    st.markdown('<h1 class="main-header">📊 FinRisk AI Agents - 专业金融风险分析系统</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 侧边栏
    with st.sidebar:
        st.markdown('<h3 class="sub-header">⚙️ 系统控制面板</h3>', unsafe_allow_html=True)
        
        # API状态检查
        api_healthy, api_info = check_api_health()
        if api_healthy:
            st.markdown('<div class="success-box">✅ API服务运行正常</div>', unsafe_allow_html=True)
            if api_info:
                st.caption(f"版本: {api_info.get('version', 'N/A')}")
                st.caption(f"时间: {api_info.get('timestamp', 'N/A')}")
        else:
            st.markdown('<div class="warning-box">❌ API服务未连接</div>', unsafe_allow_html=True)
            st.info("请确保API服务正在运行")
        
        st.markdown("---")
        
        # 导航
        page = st.radio(
            "选择分析模式",
            ["🏠 仪表板", "📈 单股票分析", "🏦 投资组合分析", "📋 数据报告"],
            index=0
        )
        
        # 加载股票列表
        stocks_list = load_stocks()
        st.session_state.stocks_list = stocks_list
        
        st.markdown("---")
        st.caption("FinRisk AI Agents v2.0")
        st.caption("© 2025 金融风险智能分析系统")
    
    # 主内容区域
    if page == "🏠 仪表板":
        show_dashboard()
    elif page == "📈 单股票分析":
        show_single_stock_analysis()
    elif page == "🏦 投资组合分析":
        show_portfolio_analysis()
    elif page == "📋 数据报告":
        show_data_report()

def show_dashboard():
    """显示仪表板"""
    st.markdown('<h2 class="sub-header">📈 市场概况</h2>', unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{API_BASE}/dashboard", timeout=5)
        if response.status_code == 200:
            dashboard_data = response.json()
            
            # 市场概要
            cols = st.columns(4)
            with cols[0]:
                st.metric("📊 股票总数", dashboard_data['market_summary']['total_stocks'])
            with cols[1]:
                st.metric("📉 平均波动率", f"{dashboard_data['market_summary']['avg_volatility']}%")
            with cols[2]:
                st.metric("📈 平均收益率", f"{dashboard_data['market_summary']['avg_return']}%")
            with cols[3]:
                st.metric("🕐 更新时间", dashboard_data['market_summary']['update_time'][11:16])
            
            # 表现最佳股票
            st.markdown('<h3 class="sub-header">🏆 表现最佳股票</h3>', unsafe_allow_html=True)
            top_df = pd.DataFrame(dashboard_data['top_performers'])
            st.dataframe(top_df.style.format({
                'return': '{:.1f}%',
                'volatility': '{:.1f}%',
                'sharpe': '{:.2f}'
            }), use_container_width=True)
            
            # 行业分布
            st.markdown('<h3 class="sub-header">🏭 行业分布</h3>', unsafe_allow_html=True)
            sector_data = dashboard_data['sector_breakdown']
            fig = px.pie(values=list(sector_data.values()), names=list(sector_data.keys()),
                        title="股票行业分布")
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("无法获取仪表板数据")
    except:
        st.warning("仪表板数据暂不可用")
    
    # 快速分析
    st.markdown('<h3 class="sub-header">⚡ 快速分析</h3>', unsafe_allow_html=True)
    
    quick_cols = st.columns(3)
    with quick_cols[0]:
        quick_stock = st.selectbox("选择股票", [s[0] for s in st.session_state.stocks_list])
    with quick_cols[1]:
        quick_days = st.selectbox("分析天数", [30, 90, 180, 252, 500], index=3)
    with quick_cols[2]:
        st.write("")
        st.write("")
        if st.button("开始快速分析", type="primary"):
            success, result = analyze_stock(quick_stock, quick_days)
            if success:
                st.session_state.analysis_data = result
                st.rerun()
            else:
                st.error(result)

def show_single_stock_analysis():
    """显示单股票分析"""
    st.markdown('<h2 class="sub-header">📈 单股票风险分析</h2>', unsafe_allow_html=True)
    
    # 分析参数
    col1, col2, col3 = st.columns(3)
    
    with col1:
        stock_options = [f"{code} - {name}" for code, name in st.session_state.stocks_list]
        selected_stock = st.selectbox("选择股票", stock_options, index=0)
        stock_code = selected_stock.split(" - ")[0]
    
    with col2:
        analysis_days = st.selectbox(
            "分析天数",
            [30, 90, 180, 252, 500, 1000],
            index=3,
            help="用于分析的历史数据天数"
        )
    
    with col3:
        st.write("")
        st.write("")
        analyze_clicked = st.button("🚀 开始深度分析", type="primary", use_container_width=True)
    
    if analyze_clicked:
        success, result = analyze_stock(stock_code, analysis_days)
        if success:
            st.session_state.analysis_data = result
        else:
            st.error(f"分析失败: {result}")
    
    # 显示分析结果
    if st.session_state.analysis_data:
        data = st.session_state.analysis_data
        
        st.markdown(f"### 📊 {data['stock_code']} 风险分析报告")
        st.caption(f"分析周期: {data['analysis_days']}天 | 生成时间: {data['timestamp']}")
        
        # 关键指标
        create_metrics_display(data)
        
        # 可视化图表
        st.markdown("### 📈 可视化分析")
        fig = create_returns_chart(data)
        st.plotly_chart(fig, use_container_width=True)
        
        # 详细数据
        with st.expander("📋 查看详细数据"):
            tab1, tab2, tab3, tab4 = st.tabs(["基本指标", "风险指标", "表现指标", "分布统计"])
            
            with tab1:
                st.json(data['basic_metrics'])
            with tab2:
                st.json(data['var_metrics'])
            with tab3:
                st.json(data['performance_metrics'])
            with tab4:
                st.json(data['distribution_stats'])
        
        # 模拟价格路径
        st.markdown("### 💹 模拟价格路径")
        price_paths = data['simulated_data']['price_paths']
        fig_paths = go.Figure()
        for i, path in enumerate(price_paths):
            fig_paths.add_trace(go.Scatter(y=path, mode='lines', 
                                          name=f'路径 {i+1}', line=dict(width=1)))
        
        fig_paths.update_layout(title="蒙特卡洛模拟价格路径",
                               xaxis_title="交易日",
                               yaxis_title="价格",
                               showlegend=True)
        st.plotly_chart(fig_paths, use_container_width=True)

def show_portfolio_analysis():
    """显示投资组合分析"""
    st.markdown('<h2 class="sub-header">🏦 投资组合风险分析</h2>', unsafe_allow_html=True)
    
    # 组合配置
    st.markdown("### ⚙️ 投资组合配置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_stocks = st.multiselect(
            "选择组合成分股",
            [s[0] for s in st.session_state.stocks_list],
            default=["AAPL", "MSFT", "GOOGL"],
            max_selections=5
        )
    
    with col2:
        analysis_days = st.selectbox(
            "分析天数",
            [90, 180, 252, 500, 1000],
            index=2
        )
    
    # 权重配置
    if selected_stocks:
        st.markdown("### ⚖️ 配置权重")
        cols = st.columns(len(selected_stocks))
        weights = []
        
        for i, stock in enumerate(selected_stocks):
            with cols[i]:
                weight = st.slider(
                    f"{stock} 权重",
                    min_value=0,
                    max_value=100,
                    value=100//len(selected_stocks),
                    key=f"weight_{stock}"
                )
                st.caption(f"{stock}")
                weights.append(weight/100)
        
        # 调整权重总和
        total_weight = sum(weights)
        if abs(total_weight - 1.0) > 0.01:
            st.warning(f"权重总和为 {total_weight:.2f}，请调整至1.0")
        
        # 分析按钮
        if st.button("📊 分析投资组合", type="primary", disabled=abs(total_weight-1.0)>0.01):
            success, result = analyze_portfolio(selected_stocks, weights, analysis_days)
            if success:
                st.session_state.portfolio_data = result
            else:
                st.error(f"分析失败: {result}")
    
    # 显示组合分析结果
    if st.session_state.portfolio_data:
        data = st.session_state.portfolio_data
        
        st.markdown("### 📈 投资组合分析结果")
        
        # 组合指标
        cols = st.columns(4)
        with cols[0]:
            st.metric("📊 组合波动率", f"{data['metrics']['portfolio_volatility']}%")
        with cols[1]:
            st.metric("🎯 组合夏普比率", f"{data['metrics']['sharpe_ratio']}")
        with cols[2]:
            st.metric("📈 组合收益率", f"{data['metrics']['annual_return']}%")
        with cols[3]:
            st.metric("🔄 分散化收益", f"{data['metrics']['diversification_benefit']}%")
        
        # 可视化
        fig = create_portfolio_charts(data)
        st.plotly_chart(fig, use_container_width=True)
        
        # 成分股波动率
        st.markdown("### 📊 成分股风险贡献")
        vol_df = pd.DataFrame({
            '股票': list(data['component_volatilities'].keys()),
            '波动率%': list(data['component_volatilities'].values())
        })
        st.bar_chart(vol_df.set_index('股票'))

def show_data_report():
    """显示数据报告"""
    st.markdown('<h2 class="sub-header">📋 数据报告与导出</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 系统状态")
        api_healthy, api_info = check_api_health()
        if api_healthy:
            st.success("✅ API服务正常")
            st.json(api_info)
        else:
            st.error("❌ API服务异常")
    
    with col2:
        st.markdown("### 📈 可用股票")
        stocks_list = st.session_state.stocks_list
        stocks_df = pd.DataFrame(stocks_list, columns=['代码', '名称'])
        st.dataframe(stocks_df, use_container_width=True)
    
    # 导出功能
    st.markdown("### 💾 数据导出")
    
    if st.session_state.analysis_data:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("导出单股票分析结果"):
                data_str = json.dumps(st.session_state.analysis_data, indent=2, ensure_ascii=False)
                st.download_button(
                    label="下载JSON文件",
                    data=data_str,
                    file_name=f"finrisk_analysis_{st.session_state.analysis_data['stock_code']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            # 生成简要报告
            report = f"""
            FinRisk 分析报告
            =================
            股票代码: {st.session_state.analysis_data['stock_code']}
            分析天数: {st.session_state.analysis_data['analysis_days']}
            生成时间: {st.session_state.analysis_data['timestamp']}
            
            关键指标:
            - 年化收益率: {st.session_state.analysis_data['basic_metrics']['annual_return']}%
            - 年化波动率: {st.session_state.analysis_data['basic_metrics']['annual_volatility']}%
            - 夏普比率: {st.session_state.analysis_data['basic_metrics']['sharpe_ratio']}
            - 最大回撤: {st.session_state.analysis_data['performance_metrics']['max_drawdown']}%
            - 95% VaR: {st.session_state.analysis_data['var_metrics']['var_95']}%
            
            风险等级: {'高风险' if st.session_state.analysis_data['basic_metrics']['annual_volatility'] > 30 else '中风险' if st.session_state.analysis_data['basic_metrics']['annual_volatility'] > 20 else '低风险'}
            
            建议:
            { '注意：该股票波动性较高，建议控制仓位并设置止损。' if st.session_state.analysis_data['basic_metrics']['annual_volatility'] > 30 else '该股票风险收益比较为均衡，适合中长期投资。' if st.session_state.analysis_data['basic_metrics']['annual_volatility'] > 20 else '该股票相对稳定，适合稳健型投资者。'}
            """
            
            st.download_button(
                label="下载文本报告",
                data=report,
                file_name=f"finrisk_report_{st.session_state.analysis_data['stock_code']}.txt",
                mime="text/plain"
            )
    
    # 系统信息
    st.markdown("### ℹ️ 系统信息")
    info_cols = st.columns(3)
    with info_cols[0]:
        st.metric("Python版本", "3.8+")
    with info_cols[1]:
        st.metric("数据更新", "实时模拟")
    with info_cols[2]:
        st.metric("支持股票", len(stocks_list))

if __name__ == "__main__":
    main()
