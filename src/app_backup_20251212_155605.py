"""
FinRisk AI Agents - Gradio 6.0.2 兼容版
确保在所有Gradio 6.x版本上都能运行
"""
import os
import sys
import gradio as gr
import pandas as pd
import numpy as np
from datetime import datetime
import logging
import json

# 禁用遥测
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_gradio_version():
    try:
        return gr.__version__
    except:
        return "未知"

logger.info(f"启动 FinRisk AI Agents (Gradio {get_gradio_version()})")

class CompatibleRiskAnalyzer:
    """兼容版风险分析器"""
    
    def __init__(self):
        self.factors = [
            {"id": "market", "name": "市场风险", "weight": 0.3},
            {"id": "credit", "name": "信用风险", "weight": 0.25},
            {"id": "liquidity", "name": "流动性风险", "weight": 0.2},
            {"id": "operational", "name": "操作风险", "weight": 0.15},
            {"id": "compliance", "name": "合规风险", "weight": 0.1}
        ]
    
    def analyze(self, portfolio_value, risk_appetite="中等"):
        """风险分析"""
        try:
            results = []
            total_weighted = 0
            
            for factor in self.factors:
                # 生成随机分数（实际应用中使用真实模型）
                base_score = np.random.uniform(1, 10)
                
                # 风险偏好调整
                if risk_appetite == "保守":
                    adjusted_score = base_score * 1.2
                elif risk_appetite == "激进":
                    adjusted_score = base_score * 0.8
                else:
                    adjusted_score = base_score
                
                weighted_score = adjusted_score * factor["weight"]
                total_weighted += weighted_score
                
                # 确定等级
                if adjusted_score < 3:
                    level = "低"
                    color = "green"
                elif adjusted_score < 7:
                    level = "中等"
                    color = "orange"
                else:
                    level = "高"
                    color = "red"
                
                results.append({
                    "name": factor["name"],
                    "base_score": round(base_score, 2),
                    "adjusted_score": round(adjusted_score, 2),
                    "weight": factor["weight"],
                    "weighted_score": round(weighted_score, 2),
                    "level": level,
                    "color": color
                })
            
            # 总体评估
            avg_score = total_weighted * 2  # 换算到0-10分
            if avg_score < 3:
                overall = "低"
                overall_color = "green"
            elif avg_score < 7:
                overall = "中等"
                overall_color = "orange"
            else:
                overall = "高"
                overall_color = "red"
            
            # 生成建议
            recommendations = self.generate_recommendations(overall, results)
            
            return {
                "success": True,
                "portfolio_value": portfolio_value,
                "formatted_value": f"${portfolio_value:,.2f}",
                "analysis_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "risk_appetite": risk_appetite,
                "factors": results,
                "overall_risk": overall,
                "overall_color": overall_color,
                "average_score": round(avg_score, 2),
                "total_weighted_score": round(total_weighted, 2),
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"分析失败: {e}")
            return {"success": False, "error": str(e)}
    
    def generate_recommendations(self, overall, factors):
        """生成建议"""
        recs = []
        
        # 总体建议
        if overall == "低":
            recs.append("✅ 风险水平良好，继续保持")
            recs.append("📊 建议定期监控风险指标")
        elif overall == "中等":
            recs.append("⚠️  风险适中，建议加强监控")
            recs.append("🛡️  考虑增加对冲策略")
        else:
            recs.append("🚨 风险较高，建议立即采取措施")
            recs.append("🔄 调整资产配置")
        
        # 高风险因素建议
        for factor in factors:
            if factor["level"] == "高":
                recs.append(f"🎯 针对{factor['name']}：加强监控和管理")
        
        return recs

def create_compatible_interface():
    """创建完全兼容的界面"""
    
    analyzer = CompatibleRiskAnalyzer()
    
    # 使用内联样式替代css参数
    with gr.Blocks() as demo:
        
        # 标题 - 使用HTML和Markdown
        gr.Markdown("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin-bottom: 20px;">
            <h1 style="margin: 0;">🔍 FinRisk AI Agents</h1>
            <p style="margin: 5px 0; opacity: 0.9;">智能金融风险分析系统</p>
            <p style="margin: 0; font-size: 14px; opacity: 0.8;">版本 2.1 - 完全兼容版</p>
        </div>
        """)
        
        # 输入区域
        with gr.Row():
            portfolio_input = gr.Number(
                label="💰 投资组合价值 (USD)",
                value=1000000,
                minimum=1000,
                step=10000
            )
            
            risk_appetite = gr.Dropdown(
                label="🎯 风险偏好",
                choices=["保守", "中等", "激进"],
                value="中等"
            )
        
        # 分析按钮
        analyze_btn = gr.Button("🚀 开始风险分析", variant="primary")
        
        # 示例按钮
        example_btn = gr.Button("📋 加载示例", variant="secondary")
        
        # 结果显示区域
        with gr.Tabs():
            with gr.TabItem("📊 分析结果"):
                result_json = gr.JSON(label="详细数据")
                
                # 总体风险显示
                overall_display = gr.HTML(label="总体风险")
                
                # 建议列表
                recommendations_html = gr.HTML(label="建议")
            
            with gr.TabItem("📈 风险详情"):
                # 风险因素详情
                factors_html = gr.HTML(label="风险因素分析")
            
            with gr.TabItem("ℹ️ 系统信息"):
                gr.Markdown(f"""
                ### 系统配置
                - **版本**: 2.1 (兼容版)
                - **Gradio**: {get_gradio_version()}
                - **Python**: {sys.version.split()[0]}
                - **更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                
                ### 功能特点
                ✅ 完全兼容 Gradio 6.x  
                ✅ 多维度风险分析  
                ✅ 个性化建议  
                ✅ 无需网络连接  
                
                ### 使用说明
                1. 输入投资组合价值
                2. 选择风险偏好
                3. 点击"开始风险分析"
                4. 查看各选项卡中的详细结果
                """)
        
        # 事件处理函数
        def process_analysis(value, appetite):
            """处理分析请求"""
            result = analyzer.analyze(value, appetite)
            
            if result["success"]:
                # 构建HTML显示
                overall_html = f"""
                <div style="padding: 20px; background: #f8fafc; border-radius: 10px; text-align: center; border-left: 5px solid {result['overall_color']};">
                    <h2 style="margin: 0;">总体风险等级</h2>
                    <h1 style="margin: 10px 0; color: {result['overall_color']};">{result['overall_risk']}</h1>
                    <p>平均得分: {result['average_score']}/10</p>
                    <p>组合价值: {result['formatted_value']}</p>
                </div>
                """
                
                # 建议HTML
                rec_html = "<div style='padding: 15px; background: #f0f9ff; border-radius: 8px;'>"
                for i, rec in enumerate(result["recommendations"], 1):
                    rec_html += f"<p>{i}. {rec}</p>"
                rec_html += "</div>"
                
                # 风险因素HTML
                factors_html_content = ""
                for factor in result["factors"]:
                    factors_html_content += f"""
                    <div style="padding: 15px; margin: 10px 0; background: #f8fafc; border-radius: 8px; border-left: 4px solid {factor['color']};">
                        <h3 style="margin: 0;">{factor['name']}</h3>
                        <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                            <span>基础得分: <strong>{factor['base_score']}</strong>/10</span>
                            <span>调整得分: <strong>{factor['adjusted_score']}</strong>/10</span>
                            <span>权重: {factor['weight']*100}%</span>
                            <span style="color: {factor['color']}; font-weight: bold;">等级: {factor['level']}</span>
                        </div>
                    </div>
                    """
                
                return (
                    result,  # JSON数据
                    overall_html,
                    rec_html,
                    factors_html_content
                )
            else:
                error_html = f"<div style='color: red; padding: 20px;'>❌ 分析失败: {result['error']}</div>"
                return (
                    result,
                    error_html,
                    error_html,
                    error_html
                )
        
        # 连接事件
        analyze_btn.click(
            fn=process_analysis,
            inputs=[portfolio_input, risk_appetite],
            outputs=[result_json, overall_display, recommendations_html, factors_html]
        )
        
        example_btn.click(
            fn=lambda: (5000000, "保守"),
            outputs=[portfolio_input, risk_appetite]
        ).then(
            fn=process_analysis,
            inputs=[portfolio_input, risk_appetite],
            outputs=[result_json, overall_display, recommendations_html, factors_html]
        )
    
    return demo

def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("FinRisk AI Agents 兼容版启动")
    logger.info("=" * 60)
    
    try:
        # 创建界面
        demo = create_compatible_interface()
        
        # 尝试获取支持的启动参数
        try:
            import inspect
            params = inspect.signature(demo.launch).parameters
            
            # 构建安全参数
            safe_params = {}
            if "server_name" in params:
                safe_params["server_name"] = "0.0.0.0"
            if "server_port" in params:
                safe_params["server_port"] = 7860
            if "share" in params:
                safe_params["share"] = False
            
            logger.info(f"使用参数启动: {safe_params}")
            demo.launch(**safe_params)
            
        except:
            # 如果参数检测失败，使用最简启动
            logger.info("使用最简启动方式")
            demo.launch()
            
    except Exception as e:
        logger.error(f"启动失败: {e}")
        
        # 终极简化版本
        print("\n" + "="*60)
        print("FinRisk AI Agents - 紧急启动模式")
        print("="*60)
        
        # 创建最简界面
        with gr.Blocks() as simple_demo:
            gr.Markdown("# FinRisk AI Agents")
            portfolio = gr.Number(value=1000000, label="投资组合价值")
            output = gr.JSON()
            
            def simple_analyze(x):
                return {"value": x, "risk": "分析完成", "time": datetime.now().strftime("%H:%M:%S")}
            
            gr.Button("分析").click(simple_analyze, portfolio, output)
        
        simple_demo.launch()

if __name__ == "__main__":
    main()
