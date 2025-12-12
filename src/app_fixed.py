"""
FinRisk AI Agents 主应用（修复版）
禁用网络检查，避免连接超时
"""
import gradio as gr
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from typing import Dict, List, Optional
import logging
import os

# 禁用 Gradio 的遥测和版本检查
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 风险分析器类（简化版）
class RiskAnalyzer:
    """风险分析核心类"""
    
    def __init__(self):
        self.risk_factors = {
            "market": {"name": "市场风险", "weight": 0.3},
            "credit": {"name": "信用风险", "weight": 0.25},
            "liquidity": {"name": "流动性风险", "weight": 0.2},
            "operational": {"name": "操作风险", "weight": 0.15}
        }
    
    def analyze_portfolio(self, portfolio_value: float) -> Dict:
        """分析投资组合风险"""
        try:
            results = {}
            total_score = 0
            
            for factor_id, factor in self.risk_factors.items():
                score = np.random.uniform(1, 10)
                weighted_score = score * factor["weight"]
                total_score += weighted_score
                
                if score < 4:
                    level = "低"
                elif score < 7:
                    level = "中等"
                else:
                    level = "高"
                
                results[factor_id] = {
                    "name": factor["name"],
                    "score": round(score, 2),
                    "weighted_score": round(weighted_score, 2),
                    "level": level,
                    "weight": factor["weight"]
                }
            
            overall_level = "低" if total_score < 10 else "中等" if total_score < 20 else "高"
            
            return {
                "success": True,
                "portfolio_value": portfolio_value,
                "risk_factors": results,
                "overall_risk": {
                    "score": round(total_score, 2),
                    "level": overall_level
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

# 创建Gradio应用（简化版）
def create_app():
    """创建主Gradio应用"""
    
    analyzer = RiskAnalyzer()
    
    # 创建界面 - 使用最简单的配置避免主题问题
    with gr.Blocks(title="FinRisk AI Agents") as demo:
        
        # 标题
        gr.Markdown("# 🔍 FinRisk AI Agents")
        gr.Markdown("## 智能金融风险分析系统")
        
        # 输入部分
        with gr.Row():
            with gr.Column():
                portfolio_value = gr.Number(
                    label="投资组合价值 (USD)",
                    value=1000000,
                    minimum=1000
                )
                
                analyze_btn = gr.Button("分析风险", variant="primary")
            
            with gr.Column():
                risk_output = gr.JSON(label="分析结果")
        
        # 分析功能
        def analyze_risk(value):
            return analyzer.analyze_portfolio(value)
        
        analyze_btn.click(
            fn=analyze_risk,
            inputs=[portfolio_value],
            outputs=[risk_output]
        )
        
        # 信息显示
        with gr.Accordion("系统信息", open=False):
            gr.Markdown("""
            ### 系统配置
            - **版本**: 1.0.0
            - **Python**: 3.11+
            - **内存**: 优化配置
            
            ### 使用说明
            1. 输入投资组合价值
            2. 点击"分析风险"按钮
            3. 查看详细风险分析结果
            """)
    
    # 禁用队列和网络功能
    demo.config = demo.config.copy()
    demo.config["show_api"] = False
    
    return demo

# 本地运行
if __name__ == "__main__":
    # 禁用更多网络检查
    os.environ["GRADIO_SERVER_NAME"] = "0.0.0.0"
    
    app = create_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        enable_queue=False,
        show_api=False,
        prevent_thread_lock=False
    )
