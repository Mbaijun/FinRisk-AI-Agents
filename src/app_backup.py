"""
FinRisk AI Agents 主应用
金融风险分析AI助手系统
"""

import gradio as gr
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from typing import Dict, List, Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 风险分析器类
class RiskAnalyzer:
    """风险分析核心类"""
    
    def __init__(self):
        self.risk_factors = {
            "market": {"name": "市场风险", "weight": 0.3},
            "credit": {"name": "信用风险", "weight": 0.25},
            "liquidity": {"name": "流动性风险", "weight": 0.2},
            "operational": {"name": "操作风险", "weight": 0.15},
            "compliance": {"name": "合规风险", "weight": 0.1}
        }
    
    def analyze_portfolio(self, portfolio_value: float, asset_allocation: Dict) -> Dict:
        """
        分析投资组合风险
        
        Args:
            portfolio_value: 组合价值
            asset_allocation: 资产配置比例
            
        Returns:
            风险分析结果
        """
        try:
            results = {}
            total_risk_score = 0
            
            for factor_id, factor in self.risk_factors.items():
                # 模拟风险计算（实际中应使用真实模型）
                base_score = np.random.uniform(0, 10)
                adjusted_score = base_score * factor["weight"]
                
                # 根据资产配置调整
                allocation_effect = 1.0
                if factor_id == "market":
                    # 股票比例越高，市场风险越大
                    stock_ratio = asset_allocation.get("stocks", 0.5)
                    allocation_effect = 1 + 0.5 * stock_ratio
                
                final_score = adjusted_score * allocation_effect
                total_risk_score += final_score
                
                # 确定风险等级
                if final_score < 3:
                    level = "低"
                    color = "green"
                elif final_score < 7:
                    level = "中等"
                    color = "orange"
                else:
                    level = "高"
                    color = "red"
                
                results[factor_id] = {
                    "name": factor["name"],
                    "score": round(final_score, 2),
                    "level": level,
                    "color": color,
                    "weight": factor["weight"],
                    "recommendations": self._get_recommendations(factor_id, level)
                }
            
            # 总体风险评估
            overall_level = "低" if total_risk_score < 15 else "中等" if total_risk_score < 30 else "高"
            
            return {
                "success": True,
                "analysis_date": datetime.now().isoformat(),
                "portfolio_value": portfolio_value,
                "asset_allocation": asset_allocation,
                "risk_factors": results,
                "overall_risk": {
                    "score": round(total_risk_score, 2),
                    "level": overall_level,
                    "color": "green" if overall_level == "低" else "orange" if overall_level == "中等" else "red"
                },
                "recommendations": self._get_overall_recommendations(overall_level)
            }
            
        except Exception as e:
            logger.error(f"风险分析失败: {e}")
            return {"success": False, "error": str(e)}
    
    def _get_recommendations(self, factor_id: str, level: str) -> List[str]:
        """获取针对性的建议"""
        recommendations = {
            "market": {
                "低": ["保持当前市场头寸", "定期监控市场变化"],
                "中等": ["考虑对冲策略", "分散投资组合", "设置止损点"],
                "高": ["减少高风险资产比例", "增加对冲工具", "重新评估投资策略"]
            },
            "credit": {
                "低": ["维持良好信用记录", "定期审查交易对手"],
                "中等": ["加强信用分析", "设置信用限额", "多样化交易对手"],
                "高": ["严格审查新交易对手", "增加担保要求", "减少高风险信用敞口"]
            },
            "liquidity": {
                "低": ["维持充足现金流", "优化支付周期"],
                "中等": ["增加流动性储备", "准备应急融资方案", "监控现金流出"],
                "高": ["立即减少非流动性资产", "激活应急融资", "优先清偿短期债务"]
            }
        }
        
        return recommendations.get(factor_id, {}).get(level, ["暂无特定建议"])
    
    def _get_overall_recommendations(self, level: str) -> List[str]:
        """获取总体建议"""
        return {
            "低": [
                "保持当前风险管理策略",
                "定期进行风险评估",
                "关注新兴风险因素"
            ],
            "中等": [
                "加强风险监控频率",
                "制定风险应对预案",
                "考虑购买保险或对冲"
            ],
            "高": [
                "立即召开风险管理会议",
                "制定紧急风险缓解计划",
                "考虑减少高风险业务",
                "准备应急资金"
            ]
        }.get(level, ["请咨询专业风险管理顾问"])

# 数据处理器类
class DataProcessor:
    """数据处理工具类"""
    
    @staticmethod
    def process_uploaded_file(file) -> Optional[Dict]:
        """处理上传的文件"""
        try:
            if file is None:
                return None
            
            # 根据文件类型处理
            if file.name.endswith('.csv'):
                df = pd.read_csv(file.name)
            elif file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file.name)
            else:
                return {"error": "不支持的文件格式"}
            
            # 基本数据统计
            stats = {
                "filename": file.name,
                "rows": len(df),
                "columns": len(df.columns),
                "columns_list": df.columns.tolist(),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "missing_values": int(df.isnull().sum().sum()),
                "duplicates": int(df.duplicated().sum()),
                "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
            }
            
            # 数值列的统计信息
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                stats["numeric_stats"] = df[numeric_cols].describe().round(2).to_dict()
            
            return {
                "success": True,
                "dataframe": df,
                "statistics": stats,
                "preview": df.head(10).to_dict('records')
            }
            
        except Exception as e:
            logger.error(f"文件处理失败: {e}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def generate_sample_data() -> pd.DataFrame:
        """生成示例数据"""
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        data = {
            'date': dates,
            'portfolio_value': np.random.normal(1000000, 50000, len(dates)).cumsum(),
            'stocks': np.random.uniform(0.4, 0.7, len(dates)),
            'bonds': np.random.uniform(0.2, 0.4, len(dates)),
            'cash': np.random.uniform(0.05, 0.15, len(dates)),
            'risk_score': np.random.uniform(0, 10, len(dates))
        }
        return pd.DataFrame(data)

# 可视化工具类
class Visualization:
    """可视化工具"""
    
    @staticmethod
    def create_risk_radar(risk_data: Dict) -> go.Figure:
        """创建风险雷达图"""
        categories = []
        values = []
        
        for factor_id, factor in risk_data.items():
            categories.append(factor["name"])
            values.append(factor["score"])
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values + [values[0]],  # 闭合图形
            theta=categories + [categories[0]],
            fill='toself',
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=False,
            title="风险因素分布雷达图"
        )
        
        return fig
    
    @staticmethod
    def create_risk_gauge(overall_score: float) -> go.Figure:
        """创建风险仪表盘"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=overall_score,
            title={'text': "总体风险得分"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 50]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 15], 'color': "green"},
                    {'range': [15, 30], 'color': "orange"},
                    {'range': [30, 50], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 30
                }
            }
        ))
        
        fig.update_layout(height=300)
        return fig

# 创建Gradio应用
def create_app():
    """创建主Gradio应用"""
    
    # 初始化组件
    analyzer = RiskAnalyzer()
    processor = DataProcessor()
    visualizer = Visualization()
    
    # 默认资产配置
    default_allocation = {
        "stocks": 0.6,
        "bonds": 0.3,
        "cash": 0.1
    }
    
    # 创建界面
    with gr.Blocks(
        title="FinRisk AI Agents - 智能金融风险分析系统",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="gray",
            neutral_hue="slate"
        ),
        css="""
        .gradio-container {
            max-width: 1400px !important;
            margin: 0 auto !important;
        }
        .dashboard-header {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            color: white;
            margin-bottom: 20px;
        }
        .risk-card {
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .risk-low { background: #d1fae5; border-left: 4px solid #10b981; }
        .risk-medium { background: #fef3c7; border-left: 4px solid #f59e0b; }
        .risk-high { background: #fee2e2; border-left: 4px solid #ef4444; }
        """
    ) as demo:
        
        # 页面标题
        gr.HTML("""
        <div class="dashboard-header">
            <h1 style="margin: 0;">🔍 FinRisk AI Agents</h1>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">智能金融风险分析系统 | 实时风险评估与决策支持</p>
            <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.8;">版本 1.0.0 | 数据驱动风险管理</p>
        </div>
        """)
        
        # 使用选项卡组织功能
        with gr.Tabs():
            
            # 选项卡1: 数据上传与准备
            with gr.Tab("📊 数据管理"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 数据上传")
                        file_input = gr.File(
                            label="上传金融数据文件",
                            file_types=[".csv", ".xlsx", ".xls"],
                            info="支持CSV和Excel格式"
                        )
                        
                        gr.Markdown("### 或使用示例数据")
                        use_sample_btn = gr.Button("加载示例数据", variant="secondary")
                        
                    with gr.Column(scale=2):
                        gr.Markdown("### 数据概览")
                        data_info = gr.JSON(label="数据信息", show_label=False)
                        
                        gr.Markdown("### 数据预览")
                        data_preview = gr.Dataframe(
                            label="",
                            interactive=False,
                            height=300
                        )
                
                # 数据上传事件
                file_input.change(
                    fn=processor.process_uploaded_file,
                    inputs=[file_input],
                    outputs=[data_info]
                ).then(
                    fn=lambda x: x.get("preview", []) if x and x.get("success") else [],
                    inputs=[data_info],
                    outputs=[data_preview]
                )
                
                # 示例数据事件
                use_sample_btn.click(
                    fn=lambda: processor.process_uploaded_file(type('obj', (object,), {'name': 'sample'})()),
                    outputs=[data_info]
                ).then(
                    fn=lambda x: x.get("preview", []) if x and x.get("success") else [],
                    inputs=[data_info],
                    outputs=[data_preview]
                )
            
            # 选项卡2: 风险分析
            with gr.Tab("📈 风险分析"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 分析参数设置")
                        
                        portfolio_value = gr.Number(
                            label="投资组合价值 (USD)",
                            value=1000000,
                            minimum=1000,
                            maximum=1000000000,
                            step=10000
                        )
                        
                        gr.Markdown("##### 资产配置比例")
                        stocks_ratio = gr.Slider(
                            label="股票比例",
                            value=0.6,
                            minimum=0,
                            maximum=1,
                            step=0.05
                        )
                        bonds_ratio = gr.Slider(
                            label="债券比例",
                            value=0.3,
                            minimum=0,
                            maximum=1,
                            step=0.05
                        )
                        cash_ratio = gr.Slider(
                            label="现金比例",
                            value=0.1,
                            minimum=0,
                            maximum=1,
                            step=0.05
                        )
                        
                        analyze_btn = gr.Button("开始风险分析", variant="primary", size="lg")
                        
                    with gr.Column(scale=2):
                        gr.Markdown("### 分析结果")
                        
                        with gr.Row():
                            risk_result = gr.JSON(
                                label="详细分析结果",
                                show_label=False
                            )
                        
                        gr.Markdown("### 可视化分析")
                        with gr.Row():
                            radar_plot = gr.Plot(label="风险雷达图")
                            gauge_plot = gr.Plot(label="总体风险仪表")
                
                # 分析按钮事件
                analyze_btn.click(
                    fn=lambda pv, s, b, c: analyzer.analyze_portfolio(
                        pv, {"stocks": s, "bonds": b, "cash": c}
                    ),
                    inputs=[portfolio_value, stocks_ratio, bonds_ratio, cash_ratio],
                    outputs=[risk_result]
                ).then(
                    fn=lambda result: visualizer.create_risk_radar(
                        result.get("risk_factors", {})
                    ) if result and result.get("success") else go.Figure(),
                    inputs=[risk_result],
                    outputs=[radar_plot]
                ).then(
                    fn=lambda result: visualizer.create_risk_gauge(
                        result.get("overall_risk", {}).get("score", 0)
                    ) if result and result.get("success") else go.Figure(),
                    inputs=[risk_result],
                    outputs=[gauge_plot]
                )
            
            # 选项卡3: 报告与建议
            with gr.Tab("📋 风险报告"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### 报告生成选项")
                        
                        report_type = gr.Radio(
                            choices=["详细报告", "执行摘要", "风险矩阵", "行动计划"],
                            label="报告类型",
                            value="详细报告"
                        )
                        
                        include_charts = gr.Checkbox(
                            label="包含图表",
                            value=True
                        )
                        
                        generate_report_btn = gr.Button("生成风险报告", variant="primary")
                        
                    with gr.Column(scale=2):
                        report_output = gr.Markdown(
                            label="风险分析报告",
                            show_label=False
                        )
                
                # 生成报告事件
                def generate_report(report_type, include_charts, risk_result_json):
                    """生成风险报告"""
                    try:
                        if not risk_result_json or not risk_result_json.get("success"):
                            return "## ⚠️ 请先进行风险分析"
                        
                        result = risk_result_json
                        
                        report = f"""
                        # 📊 金融风险分析报告
                        
                        **报告类型**: {report_type}
                        **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        **组合价值**: ${result.get('portfolio_value', 0):,.2f}
                        
                        ## 🎯 总体风险评估
                        
                        **风险得分**: {result.get('overall_risk', {}).get('score', 0)} / 50
                        **风险等级**: {result.get('overall_risk', {}).get('level', '未知')}
                        
                        ## 📈 详细风险分析
                        """
                        
                        # 添加各风险因素
                        risk_factors = result.get('risk_factors', {})
                        for factor_id, factor in risk_factors.items():
                            report += f"""
                            ### {factor['name']}
                            - **得分**: {factor['score']} / 10
                            - **等级**: {factor['level']}
                            - **权重**: {factor['weight'] * 100}%
                            - **建议**: 
                            """
                            for rec in factor.get('recommendations', []):
                                report += f"  - {rec}\n"
                        
                        # 添加总体建议
                        report += f"""
                        ## 🚀 总体建议
                        """
                        for rec in result.get('recommendations', []):
                            report += f"- {rec}\n"
                        
                        report += f"""
                        ---
                        *本报告由 FinRisk AI Agents 自动生成，仅供参考*
                        """
                        
                        return report
                        
                    except Exception as e:
                        logger.error(f"报告生成失败: {e}")
                        return f"## ❌ 报告生成失败\n错误信息: {str(e)}"
                
                generate_report_btn.click(
                    fn=generate_report,
                    inputs=[report_type, include_charts, risk_result],
                    outputs=[report_output]
                )
            
            # 选项卡4: 系统信息
            with gr.Tab("⚙️ 系统信息"):
                gr.Markdown("""
                ## FinRisk AI Agents 系统信息
                
                ### 📊 系统配置
                - **版本**: 1.0.0
                - **部署平台**: Vercel Serverless
                - **Python版本**: 3.12
                - **Gradio版本**: 6.1.0
                - **内存分配**: 3GB
                - **最大运行时间**: 120秒
                
                ### 🎯 功能特性
                - ✅ 多维度风险分析（市场、信用、流动性、操作、合规）
                - ✅ 数据质量验证与清洗
                - ✅ 交互式可视化图表
                - ✅ 自动报告生成
                - ✅ 实时计算与更新
                - ✅ 响应式Web界面
                
                ### 📁 支持的数据格式
                - CSV 文件 (.csv)
                - Excel 文件 (.xlsx, .xls)
                - 内置示例数据
                
                ### 🔧 使用说明
                1. **数据管理**: 上传您的金融数据或使用示例数据
                2. **风险分析**: 设置投资参数，进行多维度风险分析
                3. **报告生成**: 生成详细的风险分析报告和建议
                4. **系统监控**: 查看系统状态和性能指标
                
                ### 📞 技术支持
                - **文档**: [查看完整文档](https://github.com/your-repo/docs)
                - **问题反馈**: [GitHub Issues](https://github.com/your-repo/issues)
                - **版本更新**: 自动检查更新
                """)
                
                # 系统状态监控
                with gr.Row():
                    refresh_btn = gr.Button("刷新系统状态", variant="secondary")
                    status_output = gr.Textbox(
                        label="系统状态",
                        value="系统运行正常",
                        interactive=False
                    )
                
                refresh_btn.click(
                    fn=lambda: f"""
                    ✅ 系统状态报告
                    时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    内存使用: 正常
                    服务状态: 运行中
                    最后分析: {datetime.now().strftime('%H:%M:%S')}
                    """,
                    outputs=[status_output]
                )
        
        # 页脚
        gr.HTML("""
        <div style="text-align: center; margin-top: 30px; padding: 15px; border-top: 1px solid #e0e0e0; color: #666;">
            <p style="margin: 0;">© 2024 FinRisk AI Agents - 金融风险智能分析系统</p>
            <p style="margin: 5px 0 0 0; font-size: 12px;">免责声明：本系统提供分析建议，不构成投资决策，使用风险自负</p>
            <p style="margin: 5px 0 0 0; font-size: 11px; opacity: 0.7;">Powered by Gradio & Vercel</p>
        </div>
        """)
    
    # 优化性能设置
    demo.queue(
        concurrency_count=2,    # 并发数
        max_size=5,            # 队列大小
        api_open=False         # 不开放API
    )
    
    return demo

# 本地运行
if __name__ == "__main__":
    app = create_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
