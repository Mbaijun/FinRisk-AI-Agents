# demo_app.py - FinRisk-AI-Agents 交互演示 (兼容版)
import gradio as gr
import time
import random
from datetime import datetime

# 模拟数据
RISK_EVENTS = [
    ("供应链延迟", "有未经证实的报告称其主要亚洲供应商面临生产瓶颈。", "medium"),
    ("管理层变动", "CFO在最近的财报电话会议中宣布将于下季度离职。", "high"),
    ("监管审查", "据行业媒体报道，该公司可能面临新的数据隐私法规调查。", "high"),
    ("市场竞争", "主要竞争对手发布了具有价格优势的替代产品。", "low"),
]

def generate_risk_briefing(company_name):
    """主处理函数：输入公司名，生成风险简报。"""
    if not company_name.strip():
        return "请输入有效的公司名称或股票代码。"
    
    # 模拟处理时间
    time.sleep(1)
    
    # 生成随机结果
    sentiment_score = random.randint(40, 85)
    risk_level = random.choice(["低", "中", "高"])
    num_events = random.randint(2, 4)
    selected_events = random.sample(RISK_EVENTS, num_events)
    
    # 生成Markdown
    events_md = ""
    for event, desc, level in selected_events:
        level_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(level, "⚪")
        events_md += f"- **{level_emoji} {event}**\n  *{desc}*\n"
    
    sentiment_emoji = "😊" if sentiment_score > 60 else "😐" if sentiment_score > 40 else "😟"
    
    briefing = f"""
## 📈 金融风险简报: **{company_name.upper()}**

**分析时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**覆盖范围:** 近7日新闻、社交媒体、财报及监管公告

### 📊 情绪与风险概览
- **市场情绪指数:** {sentiment_score}/100 {sentiment_emoji}
- **综合风险等级:** **{risk_level}**
- **监控信号:** 共检测到 **{len(selected_events)}** 个潜在风险事件

### ⚠️ 近期风险信号
{events_md}
### 💡 建议行动
1.  **验证高风险信号**：对“{selected_events[0][0] if selected_events else 'N/A'}”进行信源交叉验证。
2.  **关注财报发布**：留意下一季度财报中管理层对相关风险的说明。

---
*本简报由 FinRisk-AI-Agents 自动生成，数据来源于公开信息模拟。*
"""
    return briefing

# ========== 创建Gradio界面（兼容旧版本语法）==========
# 使用最基础的Interface，兼容性最好
demo = gr.Interface(
    fn=generate_risk_briefing,
    inputs=gr.Textbox(
        lines=1,
        placeholder="例如: Tesla, AAPL, 腾讯, 茅台...",
        label="🎯 分析目标"
    ),
    outputs=gr.Markdown(label="📄 生成的风险简报"),
    title="🤖 FinRisk-AI-Agents: 金融风险智能分析平台",
    description="体验开源多智能体系统的核心能力。输入公司名称或股票代码，获取自动化风险简报。",
    examples=[["Tesla"], ["Apple"], ["NVIDIA"], ["腾讯"]],
    theme="default"  # 旧版本可能支持的参数
)

# 启动应用
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)