# finrisk_ai/risk_analyzer.py
import logging
from datetime import datetime

class RiskAnalyzer:
    """主风险分析器"""
    
    def __init__(self, offline_mode=True):
        self.offline_mode = offline_mode
        self.logger = self._setup_logger()
        
        # 导入离线分析器
        from finrisk_ai.offline_analyzer import OfflineRiskAnalyzer
        self.offline_analyzer = OfflineRiskAnalyzer()
        
        mode = "离线模拟模式" if offline_mode else "在线模式"
        self.logger.info(f"风险分析器初始化: {mode}")
    
    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def analyze_portfolio(self, symbols, weights=None, days=252):
        """分析投资组合"""
        self.logger.info(f"分析投资组合: {', '.join(symbols)}")
        
        try:
            if self.offline_mode:
                result = self.offline_analyzer.analyze_portfolio(symbols, weights, days)
                result['mode'] = 'offline_simulation'
                result['message'] = '使用离线模拟数据进行分析'
            else:
                # 这里可以添加在线模式的实现
                result = self.offline_analyzer.analyze_portfolio(symbols, weights, days)
                result['mode'] = 'online'
                result['message'] = '使用实时市场数据进行分析'
            
            # 添加格式化输出
            if result['success']:
                result['formatted'] = {
                    'volatility': f"{result['volatility']:.2%}",
                    'sharpe_ratio': f"{result['sharpe_ratio']:.2f}",
                    'var_95': f"{result['var_95']:.2%}",
                    'max_drawdown': f"{result['max_drawdown']:.2%}",
                    'beta': f"{result['beta']:.2f}",
                    'expected_return': f"{(result['sharpe_ratio'] * 0.02 + 0.02):.2%}"  # 简化计算
                }
            
            return result
            
        except Exception as e:
            self.logger.error(f"分析失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'symbols': symbols,
                'mode': 'offline_simulation' if self.offline_mode else 'online',
                'analysis_date': datetime.now().isoformat()
            }
    
    def get_risk_score(self, symbols, weights=None):
        """获取风险评分"""
        self.logger.info(f"计算风险评分: {', '.join(symbols)}")
        return self.offline_analyzer.get_risk_score(symbols, weights)
    
    def monte_carlo_simulation(self, symbols, initial_investment=10000, simulations=10000, days=30):
        """蒙特卡洛模拟"""
        self.logger.info(f"蒙特卡洛模拟: {len(symbols)}支股票, {simulations}次模拟")
        return self.offline_analyzer.monte_carlo_simulation(symbols, initial_investment, simulations, days)