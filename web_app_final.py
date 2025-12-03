# web_app_final.py - 修复编码问题的最终版
import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import io

# 页面配置（必须是第一个Streamlit命令）
st.set_page_config(
    page_title="FinRisk AI Agents - 专业金融风险分析系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 移除有问题的编码设置代码
# 不再修改 sys.stdout.encoding

# 自定义CSS样式
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #374151;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E5E7EB;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .success-box {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #10B981;
    }
    .error-box {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #EF4444;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown('<div class="main-title">📊 FinRisk AI Agents - 专业金融风险分析系统</div>', unsafe_allow_html=True)
st.markdown("---")

# 初始化session state
if 'api_connected' not in st.session_state:
    st.session_state.api_connected = False
if 'available_stocks' not in st.session_state:
    st.session_state.available_stocks = []

# API配置
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
    except Exception:
        st.session_state.api_connected = False
        return False

# 获取股票列表
def get_stocks_list():
    try:
        response = requests.get(f"{API_BASE}/stocks", timeout=5)
        if response.status_code == 200:
            data = response.json()
            stocks = [s["symbol"] for s in data.get("stocks", [])]
            st.session_state.available_stocks = stocks
            return stocks
        else:
            return ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JPM", "JNJ", "WMT", "NVDA", "XOM", "BRK.B", "V"]
    except:
        return ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JPM", "JNJ", "WMT", "NVDA", "XOM", "BRK.B", "V"]

# 侧边栏
with st.sidebar:
    st.header("⚙️ 系统控制面板")
    
    # API状态
    if check_api_connection():
        st.markdown('<div class="success-box">✅ API服务已连接</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-box">❌ API服务未连接</div>', unsafe_allow_html=True)
        st.info(f"请确保API服务正在运行: {API_BASE}")
        if st.button("🔄 重新连接"):
            st.rerun()
    
    st.markdown("---")
    
    # 分析模式选择
    st.header("📈 选择分析模式")
    analysis_mode = st.radio(
        "",
        ["仪表板", "单股票分析", "投资组合分析", "数据报告"],
        index=0,
        key="analysis_mode"
    )
    
    st.markdown("---")
    
    # 系统信息
    st.header("ℹ️ 系统信息")
    st.write(f"**API地址:** {API_BASE}")
    st.write(f"**系统时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if st.button("🔄 刷新数据", use_container_width=True):
        st.rerun()

# 主内容区
if analysis_mode == "仪表板":
    st.markdown('<div class="section-header">📈 市场仪表板</div>', unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{API_BASE}/dashboard", timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # 市场概览
            st.subheader("🏢 市场概览")
            market_data = data.get("market_overview", [])
            
            if market_data:
                cols = st.columns(len(market_data))
                for idx, stock in enumerate(market_data):
                    with cols[idx]:
                        change = stock.get("daily_change", 0)
                        st.metric(
                            label=stock.get("symbol", ""),
                            value=f"${stock.get('current_price', 0):.2f}",
                            delta=f"{change:.2f}%"
                        )
            
            # 风险指标
            st.subheader("⚠️ 风险指标")
            risk_data = data.get("risk_indicators", {})
            
            if risk_data:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("市场波动率", f"{risk_data.get('market_volatility', 0):.1f}%")
                with col2:
                    st.metric("VIX指数", f"{risk_data.get('vix_index', 0):.1f}")
                with col3:
                    advancers = risk_data.get('advancers', 0)
                    decliners = risk_data.get('decliners', 0)
                    st.metric("涨跌家数", f"{advancers}/{decliners}")
                with col4:
                    st.metric("PUT/CALL比率", f"{risk_data.get('put_call_ratio', 0):.2f}")
            
        else:
            st.error(f"获取仪表板数据失败: {response.status_code}")
            
    except Exception as e:
        st.error(f"仪表板加载失败: {str(e)}")

elif analysis_mode == "单股票分析":
    st.markdown('<div class="section-header">📊 单股票分析</div>', unsafe_allow_html=True)
    
    if not st.session_state.api_connected:
        st.error("请先连接API服务")
    else:
        stocks = get_stocks_list()
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            selected_stock = st.selectbox(
                "选择股票",
                stocks,
                index=0
            )
        with col2:
            days = st.slider(
                "分析天数",
                min_value=7,
                max_value=365,
                value=30,
                step=7
            )
        with col3:
            st.write("")
            st.write("")
            analyze_btn = st.button("🚀 开始分析", type="primary", use_container_width=True)
        
        if analyze_btn:
            with st.spinner("分析中..."):
                try:
                    response = requests.post(
                        f"{API_BASE}/analyze",
                        json={"symbol": selected_stock, "days": days},
                        timeout=15
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ {selected_stock} 分析完成")
                        
                        # 显示基本信息
                        st.subheader("📋 基本信息")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.info(f"**股票名称:** {result.get('name', 'N/A')}")
                        with col2:
                            st.info(f"**所属行业:** {result.get('sector', 'N/A')}")
                        with col3:
                            st.info(f"**分析周期:** {result.get('analysis_period', 0)}天")
                        
                        # 风险指标
                        st.subheader("📊 风险指标")
                        metrics = result.get("risk_metrics", {})
                        
                        if metrics:
                            cols = st.columns(5)
                            metric_items = [
                                ("波动率", "volatility", "{:.2%}"),
                                ("夏普比率", "sharpe_ratio", "{:.2f}"),
                                ("最大回撤", "max_drawdown", "{:.2%}"),
                                ("VaR (95%)", "var_95", "{:.2%}"),
                                ("CVaR (95%)", "cvar_95", "{:.2%}")
                            ]
                            
                            for idx, (label, key, fmt) in enumerate(metric_items):
                                with cols[idx]:
                                    value = metrics.get(key, 0)
                                    st.metric(label, fmt.format(value))
                        
                        # 价格走势图
                        st.subheader("📈 价格走势")
                        history = result.get("history", {})
                        if history and "dates" in history and "prices" in history:
                            fig = go.Figure()
                            fig.add_trace(go.Scatter(
                                x=history["dates"],
                                y=history["prices"],
                                mode='lines',
                                name=selected_stock,
                                line=dict(color='#3B82F6', width=2)
                            ))
                            
                            fig.update_layout(
                                title=f"{selected_stock} 价格走势",
                                xaxis_title="日期",
                                yaxis_title="价格",
                                height=400
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                    else:
                        st.error(f"分析失败: {response.text}")
                        
                except Exception as e:
                    st.error(f"分析错误: {str(e)}")

elif analysis_mode == "投资组合分析":
    st.markdown('<div class="section-header">📈 投资组合分析</div>', unsafe_allow_html=True)
    
    if not st.session_state.api_connected:
        st.error("请先连接API服务")
    else:
        stocks = get_stocks_list()
        
        # 选择股票
        selected_stocks = st.multiselect(
            "选择组合成分股",
            stocks,
            default=["AAPL", "MSFT", "GOOGL"]
        )
        
        if selected_stocks:
            # 设置权重
            st.write("设置权重 (总和应为1.0):")
            weights = []
            cols = st.columns(len(selected_stocks))
            
            for i, stock in enumerate(selected_stocks):
                with cols[i]:
                    default_weight = 1.0 / len(selected_stocks)
                    weight = st.number_input(
                        stock,
                        min_value=0.0,
                        max_value=1.0,
                        value=default_weight,
                        step=0.05,
                        format="%.2f"
                    )
                    weights.append(weight)
            
            # 检查权重
            total_weight = sum(weights)
            if abs(total_weight - 1.0) > 0.001:
                st.warning(f"⚠️ 权重总和: {total_weight:.3f} (应为1.0)")
            else:
                st.success(f"✅ 权重总和: {total_weight:.3f}")
            
            col1, col2 = st.columns(2)
            with col1:
                days = st.slider(
                    "分析天数",
                    min_value=7,
                    max_value=365,
                    value=30,
                    step=7
                )
            with col2:
                st.write("")
                st.write("")
                analyze_port = st.button("🚀 分析组合", type="primary", use_container_width=True)
            
            if analyze_port and abs(total_weight - 1.0) <= 0.001:
                with st.spinner("分析组合中..."):
                    try:
                        response = requests.post(
                            f"{API_BASE}/portfolio/analyze",
                            json={
                                "symbols": selected_stocks,
                                "weights": weights,
                                "days": days
                            },
                            timeout=20
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success("✅ 组合分析完成")
                            
                            # 组合摘要
                            st.subheader("📊 组合摘要")
                            portfolio = result.get("portfolio_summary", {})
                            
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("预期年化收益", f"{portfolio.get('expected_return', 0):.2%}")
                            with col2:
                                st.metric("组合波动率", f"{portfolio.get('volatility', 0):.2%}")
                            with col3:
                                st.metric("夏普比率", f"{portfolio.get('sharpe_ratio', 0):.2f}")
                            with col4:
                                st.metric("最大回撤", f"{portfolio.get('max_drawdown', 0):.2%}")
                            
                            # 成分股分析
                            st.subheader("📋 成分股分析")
                            stock_data = result.get("stock_analysis", [])
                            if stock_data:
                                df = pd.DataFrame(stock_data)
                                st.dataframe(
                                    df,
                                    column_config={
                                        "symbol": "股票代码",
                                        "weight": st.column_config.NumberColumn("权重", format="%.2f"),
                                        "volatility": st.column_config.NumberColumn("波动率", format="%.2%"),
                                        "expected_return": st.column_config.NumberColumn("预期收益", format="%.2%")
                                    },
                                    use_container_width=True,
                                    hide_index=True
                                )
                            
                        else:
                            st.error(f"组合分析失败: {response.text}")
                            
                    except Exception as e:
                        st.error(f"分析错误: {str(e)}")

elif analysis_mode == "数据报告":
    st.markdown('<div class="section-header">📄 数据报告</div>', unsafe_allow_html=True)
    
    if not st.session_state.api_connected:
        st.error("请先连接API服务")
    else:
        stocks = get_stocks_list()
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            selected_stock = st.selectbox(
                "选择股票",
                stocks,
                index=0
            )
        with col2:
            days = st.slider(
                "报告周期",
                min_value=7,
                max_value=90,
                value=30,
                step=7
            )
        with col3:
            st.write("")
            st.write("")
            generate_btn = st.button("📊 生成报告", type="primary", use_container_width=True)
        
        if generate_btn:
            with st.spinner("生成报告中..."):
                try:
                    response = requests.post(
                        f"{API_BASE}/report/generate",
                        json={"symbol": selected_stock, "days": days},
                        timeout=15
                    )
                    
                    if response.status_code == 200:
                        report = response.json()
                        st.success("✅ 报告生成成功")
                        
                        # 报告信息
                        st.subheader("📋 报告信息")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.info(f"**报告ID:** {report.get('report_id', '')}")
                        with col2:
                            st.info(f"**生成时间:** {report.get('generated_at', '')}")
                        with col3:
                            st.info(f"**股票代码:** {report.get('stock', '')}")
                        
                        # 投资建议
                        st.subheader("💡 投资建议")
                        summary = report.get("summary", {})
                        
                        if summary:
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("风险等级", summary.get("risk_level", "N/A"))
                            with col2:
                                st.metric("投资建议", summary.get("recommendation", "N/A"))
                            
                            if "key_points" in summary:
                                st.write("**关键指标:**")
                                for point in summary["key_points"]:
                                    st.write(f"• {point}")
                        
                        # 导出功能
                        st.subheader("💾 数据导出")
                        col1, col2 = st.columns(2)
                        with col1:
                            export_format = st.selectbox(
                                "导出格式",
                                ["CSV", "JSON"]
                            )
                        with col2:
                            st.write("")
                            st.write("")
                            export_btn = st.button("📥 导出数据", type="secondary")
                        
                        if export_btn:
                            with st.spinner("导出数据中..."):
                                try:
                                    export_response = requests.post(
                                        f"{API_BASE}/export",
                                        json={
                                            "symbol": selected_stock,
                                            "days": days,
                                            "format": export_format.lower()
                                        },
                                        timeout=15
                                    )
                                    
                                    if export_response.status_code == 200:
                                        export_data = export_response.json()
                                        
                                        if export_format == "CSV":
                                            st.download_button(
                                                label="📥 下载CSV文件",
                                                data=export_data.get("content", ""),
                                                file_name=export_data.get("filename", "data.csv"),
                                                mime="text/csv"
                                            )
                                        else:
                                            json_content = json.dumps(export_data.get("content", {}), indent=2, ensure_ascii=False)
                                            st.download_button(
                                                label="📥 下载JSON文件",
                                                data=json_content,
                                                file_name=export_data.get("filename", "data.json"),
                                                mime="application/json"
                                            )
                                        
                                        st.success(f"✅ 数据已准备，大小: {export_data.get('size', 0)} 字节")
                                    else:
                                        st.error(f"导出失败: {export_response.text}")
                                        
                                except Exception as e:
                                    st.error(f"导出错误: {str(e)}")
                        
                    else:
                        st.error(f"报告生成失败: {response.text}")
                        
                except Exception as e:
                    st.error(f"报告生成错误: {str(e)}")

# 页脚
st.markdown("---")
st.caption("© 2024 FinRisk AI Agents - 专业金融风险分析系统 | 版本 3.0")
st.caption(f"最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
