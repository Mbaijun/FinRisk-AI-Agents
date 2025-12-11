# 备份原文件
Copy-Item ui/dashboard.py ui/dashboard_backup.py

# 读取原文件内容
$content = Get-Content ui/dashboard.py -Raw

# 找到侧边栏的开始位置（通常在 st.sidebar 后）
# 在合适位置插入智能体控制代码
$agentControlCode = @"
# ==================== 🤖 智能体控制中心 ====================
with st.sidebar.expander("🤖 智能体控制中心", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        agent1 = st.checkbox("风险评估", value=True, key="agent1")
        agent2 = st.checkbox("市场监控", value=True, key="agent2")
        agent3 = st.checkbox("组合管理", value=True, key="agent3")
    
    with col2:
        agent4 = st.checkbox("合规检查", value=False, key="agent4")
        agent5 = st.checkbox("报告生成", value=False, key="agent5")
    
    st.divider()
    
    # 智能体状态显示
    active_count = sum([agent1, agent2, agent3, agent4, agent5])
    st.metric("活跃智能体", f"{active_count}/5")
    
    # 控制按钮
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("启动全部", use_container_width=True, type="primary"):
            for key in ["agent1", "agent2", "agent3", "agent4", "agent5"]:
                st.session_state[key] = True
            st.rerun()
    
    with btn_col2:
        if st.button("停止全部", use_container_width=True):
            for key in ["agent1", "agent2", "agent3", "agent4", "agent5"]:
                st.session_state[key] = False
            st.rerun()

# ============================================================
"@

# 在合适位置插入代码（在侧边栏开始后）
if ($content -match "(with st\.sidebar:[\s\S]*?)(?=st\.)" -or $content -match "(st\.sidebar\.[\s\S]*?)(?=\n\n)") {
    $newContent = $content -replace $matches[0], "$($matches[0])`n`n$agentControlCode`n`n"
    $newContent | Out-File -FilePath "ui/dashboard.py" -Encoding UTF8
    Write-Host "✅ 智能体控制面板已添加！" -ForegroundColor Green
} else {
    Write-Host "❌ 未找到合适的插入位置，请手动编辑。" -ForegroundColor Red
}
