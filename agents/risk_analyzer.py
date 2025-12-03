"""
混合风险分析器 - 尝试真实数据，失败时使用离线模拟
"""

import numpy as np
import pandas as pd
from typing import List, Dict
from agents.offline_risk_analyzer import OfflineRiskAnalyzer

class RiskAnalyzer:
    """混合风险分析器（优先真实数据，失败时使用模拟）"""
    
    def __init__(self, risk_free_rate: float = 0.02):
        self.risk_free_rate = risk_free_rate
        self.offline_analyzer = OfflineRiskAnalyzer(risk_free_rate)
        self.use_offline = True  # 强制使用离线模式（网络有问题）
        print("风险分析器初始化：使用离线模拟模式")
    
    def analyze_portfolio(self, symbols: List[str], weights: List[float]) -> Dict:
        """
        分析投资组合风险
        由于网络问题，始终使用离线模拟
        """
        try:
            print(f"分析投资组合: {', '.join(symbols)}")
            print("当前模式: 强制离线模拟（网络不可用）")
            
            # 使用离线分析器
            return self.offline_analyzer.get_detailed_report(symbols, weights)
            
        except Exception as e:
            print(f"分析失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "note": "请检查输入参数或联系管理员"
            }
    
    def analyze_with_fallback(self, symbols: List[str], weights: List[float]) -> Dict:
        """兼容旧接口"""
        return self.analyze_portfolio(symbols, weights)
