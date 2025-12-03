"""
离线风险分析器 - 完全离线运行
使用模拟数据进行风险分析
"""

import numpy as np
import pandas as pd
from typing import List, Dict
from data.data_simulator import DataSimulator

class OfflineRiskAnalyzer:
    """离线风险分析器"""
    
    def __init__(self, risk_free_rate: float = 0.02):
        self.risk_free_rate = risk_free_rate
        self.data_simulator = DataSimulator()
        print("离线风险分析器已初始化（使用模拟数据）")
    
    def analyze_portfolio(self, symbols: List[str], weights: List[float]) -> Dict:
        """
        分析投资组合风险 - 完全离线版本
        始终使用模拟数据
        """
        try:
            print(f"分析投资组合: {', '.join(symbols)}")
            print("模式: 离线模拟分析")
            
            # 验证输入
            if len(symbols) != len(weights):
                return {"success": False, "error": "股票代码和权重数量不匹配"}
            
            if abs(sum(weights) - 1.0) > 0.01:
                return {"success": False, "error": f"权重总和应为1.0，当前为{sum(weights):.4f}"}
            
            # 生成模拟数据
            portfolio_data = self.data_simulator.generate_portfolio_data(symbols, days=252)  # 一年数据
            
            if portfolio_data.empty:
                return {"success": False, "error": "无法生成模拟数据"}
            
            print(f"生成模拟数据: {len(portfolio_data)}个交易日")
            
            # 显示股票信息
            print("股票信息:")
            for symbol in symbols:
                info = self.data_simulator.get_stock_info(symbol)
                print(f"  {symbol}: {info['name']} ({info['sector']})")
            
            # 计算收益率
            returns = portfolio_data.pct_change().dropna()
            
            if returns.empty:
                # 如果收益率计算失败，生成模拟收益率
                np.random.seed(42)
                returns = pd.DataFrame(
                    np.random.normal(0.001, 0.02, (len(portfolio_data)-1, len(symbols))),
                    columns=symbols,
                    index=portfolio_data.index[1:]
                )
            
            # 计算组合收益率
            portfolio_returns = (returns * weights).sum(axis=1)
            
            # 计算各种风险指标
            metrics = self._calculate_risk_metrics(portfolio_returns)
            
            # 添加额外信息
            metrics.update({
                "success": True,
                "data_points": len(portfolio_returns),
                "analysis_mode": "offline_simulation",
                "note": "基于模拟数据的离线分析演示",
                "warning": "⚠️ 注意：这是模拟数据，仅用于演示目的",
                "simulation_info": {
                    "period_days": len(portfolio_data),
                    "symbols_count": len(symbols),
                    "data_source": "generated_simulation"
                }
            })
            
            print(f"分析完成: 波动率={metrics['volatility']:.4f}, VaR={metrics['var_95']:.4f}")
            return metrics
            
        except Exception as e:
            print(f"分析出错: {e}")
            return {"success": False, "error": str(e)}
    
    def _calculate_risk_metrics(self, returns: pd.Series) -> Dict:
        """计算各种风险指标"""
        
        # 基本指标
        volatility = returns.std() * np.sqrt(252)  # 年化波动率
        var_95 = -np.percentile(returns, 5)  # 95% VaR
        cvar_95 = -returns[returns <= -var_95].mean() if len(returns[returns <= -var_95]) > 0 else var_95
        
        # 收益率相关指标
        mean_return = returns.mean() * 252  # 年化收益率
        sharpe = (mean_return - self.risk_free_rate) / volatility if volatility > 0 else 0
        
        # 下行风险指标
        downside_returns = returns[returns < 0]
        sortino = (mean_return - self.risk_free_rate) / (downside_returns.std() * np.sqrt(252)) if len(downside_returns) > 0 else 0
        
        # 最大回撤
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # 偏度和峰度
        skewness = returns.skew()
        kurtosis = returns.kurtosis()
        
        return {
            "volatility": float(volatility),
            "var_95": float(var_95),
            "cvar_95": float(cvar_95),
            "mean_return": float(mean_return),
            "sharpe": float(sharpe),
            "sortino": float(sortino),
            "max_drawdown": float(max_drawdown),
            "skewness": float(skewness),
            "kurtosis": float(kurtosis),
            "positive_days": int((returns > 0).sum()),
            "negative_days": int((returns < 0).sum()),
            "total_days": len(returns)
        }
    
    def get_detailed_report(self, symbols: List[str], weights: List[float]) -> Dict:
        """生成详细的风险报告"""
        analysis = self.analyze_portfolio(symbols, weights)
        
        if not analysis.get("success", False):
            return analysis
        
        # 添加风险评估
        volatility = analysis["volatility"]
        if volatility < 0.15:
            risk_level = "低风险"
            risk_color = "green"
        elif volatility < 0.25:
            risk_level = "中风险"
            risk_color = "yellow"
        else:
            risk_level = "高风险"
            risk_color = "red"
        
        # 添加投资建议
        sharpe = analysis["sharpe"]
        if sharpe > 1.0:
            recommendation = "优秀 - 风险调整后收益很好"
            action = "可考虑持有或适度增加"
        elif sharpe > 0.5:
            recommendation = "良好 - 风险收益平衡"
            action = "适合长期持有"
        elif sharpe > 0:
            recommendation = "一般 - 需要优化"
            action = "建议重新平衡组合"
        else:
            recommendation = "较差 - 风险调整后收益为负"
            action = "建议重新评估投资策略"
        
        analysis.update({
            "risk_assessment": {
                "level": risk_level,
                "color": risk_color,
                "volatility_category": "低" if volatility < 0.15 else "中" if volatility < 0.25 else "高"
            },
            "recommendation": {
                "summary": recommendation,
                "action": action,
                "sharpe_interpretation": ">1.0:优秀, 0.5-1.0:良好, 0-0.5:一般, <0:较差"
            }
        })
        
        return analysis
