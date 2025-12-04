# demo_gradio.py - 独立轻量演示 (与app.py并存)
import gradio as gr
import time
import random
from datetime import datetime

def generate_risk_briefing(company_name):
    if not company_name.strip():
        return "请输入公司名称或股票代码。"
    
    time.sleep(1.5)
    
    sentiment = random.choice(["积极", "谨慎乐观", "中性", "谨慎", "消极"])
    risk = random.choice(["低", "中", "高"])
    events = random.sample(["供应链传闻", "管理层变动", "监管关注", "市场波动", "财报预期"], random.randint(2, 4))
    
    briefing = f"""
## 金融风险简报: **{company_name.upper()}**

**分析时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**市场情绪:** {sentiment}
**综合风险等级:** **{risk}**

### 近期关注点
"""
    for e in events:
        briefing += f"- {e}\n"
    
    briefing += """
---
*由 FinRisk-AI-Agents 生成 | 此为功能演示*
"""
    return briefing

demo = gr.Interface(
    fn=generate_risk_briefing,
    inputs=gr.inputs.Textbox(label="输入公司名称", placeholder="例如: Tesla"),
    outputs=gr.outputs.Textbox(label="风险简报"),
    title="FinRisk-AI-Agents 快速演示",
    examples=[["Tesla"], ["Apple"], ["NVIDIA"]]
)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port, share=False)