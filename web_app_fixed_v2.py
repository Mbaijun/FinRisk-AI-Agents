# web_app_fixed.py
import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import io

# 页面配置
st.set_page_config(
    page_title="FinRisk AI Agents - 专业金融风险分析系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 设置CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #374151;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3B82F6;
    }
    .success-box {
        background-color: #D1FAE5;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #10B981;
    }
    .error-box {
        background-color: #FEE2E2;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #EF4444;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown('<h1 class="main-header">📊 FinRisk AI Agents - 专业金融风险分析系统</h1>', unsafe_allow_html=True)
st.markdown("---")

# 初始化session state
if 'api_connected' not in st.session_state:
    st.session_state.api_connected = False
if 'available_stocks' not in st.session_state:
    st.session_state.available_stocks = []
if 'dashboard_data' not in st.session_state:
    st.session_state.dashboard_data = None

# API基础URL
API_BASE = "http://localhost:8000"

# 检查API连接
def check_api_connection():
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            st.session_state.api_connected = True
            return True
        else:
            st.session_state.api_connected = False
            return False
    except:
        st.session_state.api_connected = False
        return False

# 获取股票列表
def get_stocks_list():
    try:
        response = requests.get(f"{API_BASE}/stocks", timeout=5)
        if response.status_code == 200:
            data = response.json()
            st.session_state.available_stocks = [s["symbol"] for s in data.get("stocks", [])]
            return st.session_state.available_stocks
        else:
            return ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JPM", "JNJ", "WMT", "NVDA", "XOM", "BRK.B", "V"]
    except:
        return ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JPM", "JNJ", "WMT", "NVDA", "XOM", "BRK.B", "V"]

# 获取仪表板数据
def get_dashboard_data():
    try:
        response = requests.get(f"{API_BASE}/dashboard", timeout=10)
        if response.status_code == 200:
            st.session_state.dashboard_data = response.json()
            return st.session_state.dashboard_data
        else:
            return None
    except:
        return None

# 侧边栏
with st.sidebar:
    st.header("⚙️ 系统控制面板")
    
    # API状态
    api_status_container = st.container()
    
    with api_status_container:
        if check_api_connection():
            st.success("✅ API服务已连接")
        else:
            st.error("❌ API服务未连接")
            st.info(f"请确保API服务正在运行: {API_BASE}")
            if st.button("🔄 重新连接"):
                st.rerun()
    
    st.markdown("---")
    
    # 分析模式选择
    st.header("📈 选择分析模式")
    analysis_mode = st.radio(
        "选择分析模式:",
        ["仪表板", "单股票分析", "投资组合分析", "数据报告"],
        index=0,
        key="analysis_mode"
    )
    
    st.markdown("---")
    
    # 系统信息
    st.header("ℹ️ 系统信息")
    st.write(f"**API地址:** {API_BASE}")
    st.write(f"**系统时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if st.button("🔄 刷新数据"):
        st.rerun()

# 主内容区
if analysis_mode == "仪表板":
    st.markdown('<h2 class="sub-header">📈 市场仪表板</h2>', unsafe_allow_html=True)
    
    # 获取仪表板数据
    dashboard_data = get_dashboard_data()
    
    if dashboard_data:
        # 市场概览
        st.subheader("🏢 市场概览")
        
        market_overview = dashboard_data.get("market_overview", [])
        if market_overview:
            cols = st.columns(len(market_overview))
            for idx, stock in enumerate(market_overview):
                with cols[idx]:
                    change_color = "green" if stock["daily_change"] >= 0 else "red"
                    st.metric(
                        label=stock["symbol"],
                        value=f"${stock['current_price']:.2f}",
                        delta=f"{stock['daily_change']:.2f}%",
                        delta_color="normal"
                    )
                    st.caption(f"波动率: {stock['volatility']:.1f}%")
        
        # 风险指标
        st.subheader("⚠️ 风险指标")
        
        risk_indicators = dashboard_data.get("risk_indicators", {})
        if risk_indicators:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("市场波动率", f"{risk_indicators.get('market_volatility', 0):.1f}%")
            with col2:
                st.metric("VIX指数", f"{risk_indicators.get('vix_index', 0):.1f}")
            with col3:
                st.metric("涨跌家数", f"{risk_indicators.get('advancers', 0)}/{risk_indicators.get('decliners', 0)}")
            with col4:
                st.metric("PUT/CALL比率", f"{risk_indicators.get('put_call_ratio', 0):.2f}")
        
        # 行业分布
        st.subheader("🏭 行业分布")
        
        sector_dist = dashboard_data.get("sector_distribution", {})
        if sector_dist:
            sectors = list(sector_dist.keys())
            counts = list(sector_dist.values())
            
            fig = px.pie(
                values=counts,
                names=sectors,
                title="行业分布",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 最近更新
        st.caption(f"最后更新: {dashboard_data.get('timestamp', '')}")
        
    else:
        st.warning("无法获取仪表板数据")
        st.info("请检查API连接或稍后重试")

elif analysis_mode == "单股票分析":
    st.markdown('<h2 class="sub-header">📊 单股票分析</h2>', unsafe_allow_html=True)
    
    if not st.session_state.api_connected:
        st.error("请先连接API服务")
    else:
        # 获取股票列表
        stocks = get_stocks_list()
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            selected_stock = st.selectbox(
                "选择股票",
                stocks,
                index=0,
                key="single_stock"
            )
        with col2:
            analysis_days = st.slider(
                "分析天数",
                min_value=7,
                max_value=365,
                value=30,
                step=7,
                key="single_days"
            )
        with col3:
            st.write("")
            st.write("")
            analyze_btn = st.button("🚀 开始分析", type="primary", use_container_width=True)
        
        if analyze_btn:
            with st.spinner("正在分析中..."):
                try:
                    # 调用API
                    response = requests.post(
                        f"{API_BASE}/analyze",
                        json={
                            "symbol": selected_stock,
                            "days": analysis_days
                        },
                        timeout=15
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ {selected_stock} 分析完成")
                        
                        # 显示股票信息
                        st.subheader("📋 股票信息")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.info(f"**名称:** {result.get('name', 'N/A')}")
                        with col2:
                            st.info(f"**行业:** {result.get('sector', 'N/A')}")
                        with col3:
                            st.info(f"**分析周期:** {result.get('analysis_period', 0)}天")
                        
                        # 风险指标
                        st.subheader("📊 风险指标")
                        
                        metrics = result.get('risk_metrics', {})
                        if metrics:
                            cols = st.columns(5)
                            metric_config = [
                                ("波动率", "volatility", "{:.2%}"),
                                ("夏普比率", "sharpe_ratio", "{:.2f}"),
                                ("最大回撤", "max_drawdown", "{:.2%}"),
                                ("VaR (95%)", "var_95", "{:.2%}"),
                                ("CVaR (95%)", "cvar_95", "{:.2%}")
                            ]
                            
                            for idx, (label, key, fmt) in enumerate(metric_config):
                                with cols[idx]:
                                    value = metrics.get(key, 0)
                                    st.metric(label, fmt.format(value))
                        
                        # 价格摘要
                        st.subheader("💰 价格摘要")
                        
                        prices = result.get('price_summary', {})
                        if prices:
                            cols = st.columns(4)
                            price_config = [
                                ("初始价格", "initial_price", "${:.2f}"),
                                ("最终价格", "final_price", "${:.2f}"),
                                ("最低价格", "min_price", "${:.2f}"),
                                ("最高价格", "max_price", "${:.2f}")
                            ]
                            
                            for idx, (label, key, fmt) in enumerate(price_config):
                                with cols[idx]:
                                    value = prices.get(key, 0)
                                    st.metric(label, fmt.format(value))
                        
                        # 价格走势图
                        st.subheader("📈 价格走势")
                        
                        history = result.get('history', {})
                        if history and 'dates' in history and 'prices' in history:
                            fig = go.Figure()
                            fig.add_trace(go.Scatter(
                                x=history['dates'],
                                y=history['prices'],
                                mode='lines',
                                name=selected_stock,
                                line=dict(color='#3B82F6', width=2)
                            ))
                            
                            fig.update_layout(
                                title=f"{selected_stock} 价格走势 ({analysis_days}天)",
                                xaxis_title="日期",
                                yaxis_title="价格",
                                height=400
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # 收益率分布
                        st.subheader("📊 收益率分布")
                        
                        if history and 'returns' in history:
                            returns = history['returns']
                            fig = px.histogram(
                                x=returns,
                                nbins=30,
                                title="日收益率分布",
                                color_discrete_sequence=['#10B981']
                            )
                            fig.update_layout(
                                xaxis_title="日收益率",
                                yaxis_title="频率",
                                height=300
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                    elif response.status_code == 422:
                        st.error("输入参数错误，请检查股票代码和分析天数")
                    else:
                        st.error(f"分析失败: {response.text}")
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"网络错误: {str(e)}")
                except Exception as e:
                    st.error(f"分析出错: {str(e)}")

elif analysis_mode == "投资组合分析":
    st.markdown('<h2 class="sub-header">📈 投资组合分析</h2>', unsafe_allow_html=True)
    
    if not st.session_state.api_connected:
        st.error("请先连接API服务")
    else:
        stocks = get_stocks_list()
        
        # 选择股票
        st.subheader("1. 选择组合成分股")
        selected_stocks = st.multiselect(
            "选择股票 (可多选)",
            stocks,
            default=["AAPL", "MSFT", "GOOGL"],
            key="portfolio_stocks"
        )
        
        if selected_stocks:
            st.subheader("2. 设置权重")
            st.write("请设置各股票权重 (总和应为1.0):")
            
            weights = []
            cols = st.columns(len(selected_stocks))
            
            for i, stock in enumerate(selected_stocks):
                with cols[i]:
                    default_weight = 1.0 / len(selected_stocks)
                    weight = st.number_input(
                        f"{stock}",
                        min_value=0.0,
                        max_value=1.0,
                        value=default_weight,
                        step=0.05,
                        format="%.2f",
                        key=f"weight_{stock}"
                    )
                    weights.append(weight)
            
            # 检查权重总和
            total_weight = sum(weights)
            weight_status = st.empty()
            
            if abs(total_weight - 1.0) > 0.001:
                weight_status.error(f"⚠️ 权重总和为 {total_weight:.3f}，应为 1.0")
            else:
                weight_status.success(f"✅ 权重总和: {total_weight:.3f}")
            
            st.subheader("3. 分析设置")
            col1, col2 = st.columns(2)
            with col1:
                analysis_days = st.slider(
                    "分析天数",
                    min_value=7,
                    max_value=365,
                    value=30,
                    step=7,
                    key="portfolio_days"
                )
            with col2:
                st.write("")
                st.write("")
                analyze_portfolio_btn = st.button("🚀 分析投资组合", type="primary", use_container_width=True)
            
            if analyze_portfolio_btn and abs(total_weight - 1.0) <= 0.001:
                with st.spinner("正在分析投资组合..."):
                    try:
                        response = requests.post(
                            f"{API_BASE}/portfolio/analyze",
                            json={
                                "symbols": selected_stocks,
                                "weights": weights,
                                "days": analysis_days
                            },
                            timeout=20
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success("✅ 投资组合分析完成")
                            
                            # 组合摘要
                            st.subheader("📊 投资组合摘要")
                            
                            portfolio = result.get('portfolio_summary', {})
                            if portfolio:
                                cols = st.columns(4)
                                summary_config = [
                                    ("预期年化收益", "expected_return", "{:.2%}"),
                                    ("组合波动率", "volatility", "{:.2%}"),
                                    ("夏普比率", "sharpe_ratio", "{:.2f}"),
                                    ("分散化效益", "diversification_benefit", "{:.2%}")
                                ]
                                
                                for idx, (label, key, fmt) in enumerate(summary_config):
                                    with cols[idx]:
                                        value = portfolio.get(key, 0)
                                        st.metric(label, fmt.format(value))
                            
                            # 成分股分析
                            st.subheader("📋 成分股分析")
                            
                            stock_analysis = result.get('analysis', [])
                            if stock_analysis:
                                df_stocks = pd.DataFrame(stock_analysis)
                                st.dataframe(
                                    df_stocks,
                                    column_config={
                                        "symbol": "代码",
                                        "name": "名称",
                                        "weight": st.column_config.NumberColumn("权重", format="%.2f"),
                                        "volatility": st.column_config.NumberColumn("波动率", format="%.2%"),
                                        "sharpe_ratio": st.column_config.NumberColumn("夏普比率", format="%.2f"),
                                        "expected_return": st.column_config.NumberColumn("预期收益", format="%.2%"),
                                        "contribution_to_risk": st.column_config.NumberColumn("风险贡献", format="%.2%")
                                    },
                                    use_container_width=True,
                                    hide_index=True
                                )
                            
                            # 相关性矩阵
                            st.subheader("🔗 相关性矩阵")
                            
                            corr_matrix = result.get('correlation_matrix', [])
                            if corr_matrix:
                                df_corr = pd.DataFrame(
                                    corr_matrix,
                                    index=selected_stocks,
                                    columns=selected_stocks
                                )
                                
                                fig = px.imshow(
                                    df_corr,
                                    text_auto='.2f',
                                    aspect="auto",
                                    color_continuous_scale="RdBu",
                                    zmin=-1,
                                    zmax=1,
                                    title="股票相关性矩阵"
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            
                            # 风险贡献饼图
                            st.subheader("🥧 风险贡献分布")
                            
                            if stock_analysis:
                                risk_contrib = [s['contribution_to_risk'] for s in stock_analysis]
                                fig = px.pie(
                                    values=risk_contrib,
                                    names=selected_stocks,
                                    title="风险贡献分布",
                                    color_discrete_sequence=px.colors.sequential.Plasma
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            
                        elif response.status_code == 422:
                            st.error("输入参数错误，请检查股票代码、权重和分析天数")
                        else:
                            st.error(f"投资组合分析失败: {response.text}")
                            
                    except requests.exceptions.RequestException as e:
                        st.error(f"网络错误: {str(e)}")
                    except Exception as e:
                        st.error(f"分析出错: {str(e)}")

elif analysis_mode == "数据报告":
    st.markdown('<h2 class="sub-header">📄 数据报告</h2>', unsafe_allow_html=True)
    
    if not st.session_state.api_connected:
        st.error("请先连接API服务")
    else:
        stocks = get_stocks_list()
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            report_stock = st.selectbox(
                "选择股票",
                stocks,
                index=0,
                key="report_stock"
            )
        with col2:
            report_days = st.slider(
                "报告周期",
                min_value=7,
                max_value=90,
                value=30,
                step=7,
                key="report_days"
            )
        with col3:
            st.write("")
            st.write("")
            generate_report_btn = st.button("📊 生成报告", type="primary", use_container_width=True)
        
        if generate_report_btn:
            with st.spinner("正在生成报告..."):
                try:
                    # 生成报告
                    response = requests.post(
                        f"{API_BASE}/report/generate",
                        json={
                            "symbol": report_stock,
                            "days": report_days
                        },
                        timeout=15
                    )
                    
                    if response.status_code == 200:
                        report = response.json()
                        st.success("✅ 报告生成完成")
                        
                        # 显示报告信息
                        st.subheader("📋 报告概览")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.info(f"**报告ID:** {report.get('report_id', 'N/A')}")
                        with col2:
                            st.info(f"**生成时间:** {report.get('generated_at', 'N/A')}")
                        with col3:
                            st.info(f"**股票:** {report_stock}")
                        
                        # 投资建议
                        st.subheader("💡 投资建议")
                        
                        summary = report.get('summary', {})
                        if summary:
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("风险等级", summary.get('risk_level', 'N/A'))
                            with col2:
                                st.metric("投资建议", summary.get('investment_suggestion', 'N/A'))
                            
                            st.write("**主要风险:**")
                            for risk in summary.get('key_risks', []):
                                st.write(f"• {risk}")
                        
                        # 导出功能
                        st.subheader("💾 数据导出")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            export_format = st.selectbox(
                                "选择导出格式",
                                ["CSV", "JSON"],
                                key="export_format"
                            )
                        with col2:
                            st.write("")
                            st.write("")
                            export_btn = st.button("📥 导出数据", type="secondary")
                        
                        if export_btn:
                            with st.spinner("正在导出数据..."):
                                try:
                                    export_response = requests.post(
                                        f"{API_BASE}/export",
                                        json={
                                            "symbol": report_stock,
                                            "days": report_days,
                                            "format": export_format.lower()
                                        },
                                        timeout=15
                                    )
                                    
                                    if export_response.status_code == 200:
                                        export_data = export_response.json()
                                        
                                        if export_format == "CSV":
                                            csv_content = export_data.get('content', '')
                                            st.download_button(
                                                label="📥 下载CSV文件",
                                                data=csv_content,
                                                file_name=export_data.get('filename', 'data.csv'),
                                                mime="text/csv"
                                            )
                                        else:  # JSON
                                            json_content = json.dumps(export_data.get('content', {}), indent=2)
                                            st.download_button(
                                                label="📥 下载JSON文件",
                                                data=json_content,
                                                file_name=export_data.get('filename', 'data.json'),
                                                mime="application/json"
                                            )
                                        
                                        st.success(f"✅ 数据导出成功，文件大小: {export_data.get('size', 0)} 字节")
                                    else:
                                        st.error(f"导出失败: {export_response.text}")
                                        
                                except Exception as e:
                                    st.error(f"导出出错: {str(e)}")
                        
                    else:
                        st.error(f"报告生成失败: {response.text}")
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"网络错误: {str(e)}")
                except Exception as e:
                    st.error(f"报告生成出错: {str(e)}")

# 页脚
st.markdown("---")
st.caption("© 2024 FinRisk AI Agents - 专业金融风险分析系统 | 版本 3.0")
st.caption(f"最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
