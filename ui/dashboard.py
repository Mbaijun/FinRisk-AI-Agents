# ui/dashboard.py - 修复版本
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# 1. 确保页面配置在最开始设置，且只设置一次
st.set_page_config(
    page_title="FinRisk AI Agents",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"  # 明确指定侧边栏状态
)
with st.sidebar.expander("🤖 智能体控制中心", expanded=True):
    agent1 = st.checkbox("风险评估智能体", value=True)
    agent2 = st.checkbox("市场监控智能体", value=True)
    agent3 = st.checkbox("组合管理智能体", value=True)
    agent4 = st.checkbox("合规检查智能体", value=False)
    agent5 = st.checkbox("报告生成智能体", value=False)
    
    st.divider()
    
    # 智能体协同控制
    if st.button("🔌 启动所有智能体", use_container_width=True):
        st.session_state.agent1 = True
        st.session_state.agent2 = True
        st.session_state.agent3 = True
        st.session_state.agent4 = True
        st.session_state.agent5 = True
        st.rerun()
    
    if st.button("🛑 停止所有智能体", use_container_width=True):
        st.session_state.agent1 = False
        st.session_state.agent2 = False
        st.session_state.agent3 = False
        st.session_state.agent4 = False
        st.session_state.agent5 = False
        st.rerun()
# 2. 初始化 session_state，避免条件判断时引用不存在的键
if 'agents_running' not in st.session_state:
    st.session_state.agents_running = False

# 3. 使用明确的容器和列布局，避免动态创建/销毁
main_container = st.container()

with main_container:
    # 标题区 - 使用固定容器
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.title("🚀 FinRisk AI Agents 仪表板")
        st.markdown("### 金融风险管理多智能体系统")
    with header_col2:
        st.caption(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    st.divider()
    
    # 控制面板区 - 使用固定容器
    control_container = st.container()
    with control_container:
        st.subheader("⚙️ 系统控制")
        control_col1, control_col2, control_col3 = st.columns(3)
        
        with control_col1:
            model_type = st.selectbox(
                "选择风险模型",
                ["VaR模型", "压力测试", "情景分析", "Copula模型"],
                key="model_select"  # 添加唯一key
            )
        
        with control_col2:
            time_range = st.slider(
                "分析时间范围（天）",
                7, 365, 30,
                key="time_slider"
            )
        
        with control_col3:
            st.markdown("#### 智能体状态")
            status_text = "🟢 运行中" if st.session_state.agents_running else "🔴 已停止"
            st.markdown(f"**{status_text}**")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("启动系统", type="primary", use_container_width=True):
                    st.session_state.agents_running = True
                    st.rerun()  # 使用rerun而不是直接操作DOM
            with col_b:
                if st.button("停止系统", use_container_width=True):
                    st.session_state.agents_running = False
                    st.rerun()
    
    st.divider()
    
    # 内容标签页 - 使用固定结构
    tab_container = st.container()
    with tab_container:
        tab1, tab2, tab3 = st.tabs(["📈 市场监控", "🛡️ 风险评估", "📊 投资组合"])
        
        with tab1:
            st.subheader("市场数据概览")
            # 使用固定的数据生成逻辑
            dates = pd.date_range('2024-01-01', periods=30, freq='D')
            market_data = pd.DataFrame({
                '日期': dates,
                '股票指数': np.random.randn(30).cumsum() + 100,
                '债券收益': np.random.randn(30).cumsum() + 50,
            })
            
            fig1 = px.line(market_data, x='日期', y=['股票指数', '债券收益'],
                          title='资产价格走势', labels={'value': '价格', 'variable': '资产类别'})
            fig1.update_layout(height=400, showlegend=True)
            st.plotly_chart(fig1, use_container_width=True, key="market_chart")
        
        with tab2:
            st.subheader("风险评估")
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            
            with metrics_col1:
                st.metric("风险等级", "中等", "+2%", delta_color="inverse")
            with metrics_col2:
                st.metric("VaR (95%)", "¥125,000", "-5%")
            with metrics_col3:
                st.metric("夏普比率", "1.25", "+0.1")
            
            # 固定的图表数据
            risk_data = pd.DataFrame({
                '风险类型': ['市场风险', '信用风险', '流动性风险', '操作风险'],
                '风险值': [45, 30, 15, 10]
            })
            fig2 = px.pie(risk_data, values='风险值', names='风险类型',
                         title='风险类型分布', hole=0.3)
            st.plotly_chart(fig2, use_container_width=True, key="risk_chart")
        
        with tab3:
            st.subheader("投资组合")
            portfolio_data = pd.DataFrame({
                '资产': ['股票A', '股票B', '债券C', '黄金', '现金'],
                '权重 (%)': [25, 20, 30, 15, 10],
                '收益率 (%)': [8.5, 6.2, 3.1, 2.5, 1.2],
                '波动率 (%)': [15.2, 12.8, 5.1, 8.4, 0.5]
            })
            st.dataframe(portfolio_data, use_container_width=True, hide_index=True)
    
    # 页脚 - 固定位置
    st.divider()
    footer_container = st.container()
    with footer_container:
        st.info("💡 **提示**: 这是 FinRisk-AI-Agents 系统的在线演示版本。")
        st.caption("版本: 1.0.0 | 技术支持: Streamlit Cloud")