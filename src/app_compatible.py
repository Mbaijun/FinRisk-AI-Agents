"""
FinRisk AI Agents - 完全兼容版本
适用于所有 Gradio 版本
"""
import os
import sys
import gradio as gr
import pandas as pd
import numpy as np
from datetime import datetime
import logging

# 禁用所有网络检查和遥测
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_gradio_version():
    """获取Gradio版本信息"""
    try:
        import gradio as gr
        return gr.__version__
    except:
        return "未知"

logger.info(f"Gradio版本: {get_gradio_version()}")
logger.info("启动 FinRisk AI Agents...")

class SimpleRiskAnalyzer:
    """简化的风险分析器"""
    
    def __init__(self):
        self.factors = ["市场风险", "信用风险", "流动性风险", "操作风险"]
    
    def analyze(self, portfolio_value):
        """简单的风险分析"""
        try:
            # 模拟分析逻辑
            import random
            results = []
            total_score = 0
            
            for factor in self.factors:
                score = random.uniform(1, 10)
                level = "低" if score < 4 else "中等" if score < 7 else "高"
                results.append({
                    "factor": factor,
                    "score": round(score, 2),
                    "level": level
                })
                total_score += score
            
            avg_score = total_score / len(self.factors)
            overall = "低" if avg_score < 4 else "中等" if avg_score < 7 else "高"
            
            return {
                "success": True,
                "portfolio_value": f"${portfolio_value:,.2f}",
                "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "factors": results,
                "overall_risk": overall,
                "average_score": round(avg_score, 2),
                "recommendation": self.get_recommendation(overall)
            }
        except Exception as e:
            logger.error(f"分析失败: {e}")
            return {"success": False, "error": str(e)}
    
    def get_recommendation(self, level):
        """根据风险等级获取建议"""
        recommendations = {
            "低": "风险可控，建议定期监控",
            "中等": "需要关注，建议加强风险管理措施",
            "高": "风险较高，建议立即采取风险缓解措施"
        }
        return recommendations.get(level, "请咨询专业风险管理顾问")

def create_interface():
    """创建Gradio界面"""
    
    analyzer = SimpleRiskAnalyzer()
    
    # 使用最简单的Blocks配置
    with gr.Blocks() as demo:
        
        # 标题
        gr.Markdown("""
        # 🔍 FinRisk AI Agents
        ### 智能金融风险分析系统
        """)
        
        # 输入区域
        with gr.Row():
            portfolio_input = gr.Number(
                label="投资组合价值 (USD)",
                value=1000000,
                minimum=1000,
                maximum=1000000000,
                step=10000
            )
        
        # 分析按钮
        analyze_btn = gr.Button("🚀 开始风险分析", variant="primary")
        
        # 输出区域
        with gr.Row():
            result_output = gr.JSON(label="分析结果")
        
        # 建议区域
        with gr.Row():
            recommendation_output = gr.Textbox(
                label="风险管理建议",
                interactive=False
            )
        
        # 系统信息
        with gr.Accordion("ℹ️ 系统信息", open=False):
            gr.Markdown(f"""
            - **应用版本**: 1.0.0
            - **Gradio版本**: {get_gradio_version()}
            - **Python版本**: {sys.version.split()[0]}
            - **启动时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            - **运行状态**: ✅ 正常
            """)
        
        # 事件处理
        def analyze_handler(value):
            result = analyzer.analyze(value)
            if result["success"]:
                recommendation = result.pop("recommendation", "")
                return result, recommendation
            else:
                return {"error": result["error"]}, "分析失败"
        
        analyze_btn.click(
            fn=analyze_handler,
            inputs=[portfolio_input],
            outputs=[result_output, recommendation_output]
        )
    
    return demo

def main():
    """主函数"""
    try:
        # 创建界面
        demo = create_interface()
        
        # 获取允许的参数
        import inspect
        launch_params = inspect.signature(demo.launch).parameters
        
        # 构建参数字典
        kwargs = {
            "server_name": "0.0.0.0",
            "server_port": 7860,
            "share": False
        }
        
        # 只传递支持的参数
        supported_kwargs = {}
        for key, value in kwargs.items():
            if key in launch_params:
                supported_kwargs[key] = value
        
        logger.info(f"使用参数启动: {supported_kwargs}")
        
        # 启动应用
        demo.launch(**supported_kwargs)
        
    except Exception as e:
        logger.error(f"应用启动失败: {e}")
        
        # 降级方案：使用最简启动
        try:
            demo = create_interface()
            demo.launch()
        except:
            # 最后尝试方案
            print("=" * 60)
            print("FinRisk AI Agents 启动失败")
            print(f"错误: {e}")
            print("=" * 60)
            print("\n建议:")
            print("1. 更新Gradio: pip install --upgrade gradio")
            print("2. 检查Python版本")
            print("3. 直接部署到Vercel")
            input("\n按回车键退出...")

if __name__ == "__main__":
    main()
