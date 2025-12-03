# finrisk_ai/offline_analyzer.py
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging

class OfflineRiskAnalyzer:
    """离线风险分析器（使用模拟数据）"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.logger.info("离线风险分析器初始化完成")
    
    def _setup_logger(self):
        """设置日志记录器"""
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
    
    def _calculate_returns(self, prices):
        """计算收益率"""
        return prices.pct_change().dropna()
    
    def _calculate_volatility(self, returns):
        """计算年化波动率"""
        return returns.std() * np.sqrt(252)
    
    def _calculate_sharpe_ratio(self, returns, risk_free_rate=0.02):
        """计算夏普比率"""
        excess_returns = returns.mean() - risk_free_rate/252
        volatility = returns.std()
        if volatility == 0:
            return 0
        return excess_returns / volatility * np.sqrt(252)
    
    def _calculate_var(self, returns, confidence_level=0.95):
        """计算VaR"""
        return np.percentile(returns, (1 - confidence_level) * 100)
    
    def simulate_market_data(self, symbols, days=252):
        """模拟市场数据 - 修复数据长度问题"""
        try:
            # 确保至少有days个交易日
            end_date = datetime.now()
            start_date = end_date - timedelta(days=int(days * 1.5))  # 多生成50%的数据
            
            # 生成工作日（确保我们得到足够的交易日）
            all_dates = pd.date_range(start=start_date, end=end_date, freq='B')
            
            # 如果生成的日期不足，扩展日期范围
            while len(all_dates) < days:
                start_date = start_date - timedelta(days=30)
                all_dates = pd.date_range(start=start_date, end=end_date, freq='B')
            
            # 取最后days个交易日
            dates = all_dates[-days:]
            self.logger.info(f"生成{len(dates)}个交易日数据，请求{days}天")
            
            # 基础价格配置
            base_prices = {
                'AAPL': 175, 'MSFT': 330, 'GOOGL': 135, 'AMZN': 145,
                'TSLA': 235, 'META': 325, 'NVDA': 485, 'JPM': 155,
                'JNJ': 150, 'V': 245, 'WMT': 165, 'PG': 155,
                'MA': 390, 'UNH': 525, 'HD': 310, 'BAC': 30,
                'XOM': 105, 'CVX': 150, 'KO': 60, 'PEP': 170
            }
            
            # 波动率配置
            volatilities = {
                'TSLA': 0.035, 'NVDA': 0.032, 'META': 0.028,
                'AAPL': 0.022, 'MSFT': 0.020, 'GOOGL': 0.021,
                'AMZN': 0.024, 'JPM': 0.018, 'JNJ': 0.015,
                'V': 0.019, 'WMT': 0.016, 'PG': 0.015,
                'XOM': 0.020, 'KO': 0.014, 'PEP': 0.016
            }
            
            # 生成数据
            data = {}
            np.random.seed(42)  # 确保可重复性
            
            for symbol in symbols:
                base_price = base_prices.get(symbol, 100)
                volatility = volatilities.get(symbol, 0.02)
                drift = 0.0005  # 每日漂移
                
                # 生成收益率
                daily_returns = np.random.normal(drift, volatility, len(dates))
                
                # 添加一些自相关性（更真实）
                for i in range(1, len(daily_returns)):
                    daily_returns[i] = 0.3 * daily_returns[i-1] + 0.7 * daily_returns[i]
                
                # 生成价格序列
                price_series = base_price * np.exp(np.cumsum(daily_returns))
                
                # 添加随机跳跃
                jumps = np.random.poisson(0.05, len(dates))
                jump_sizes = np.random.normal(0, 0.03, len(dates)) * jumps
                price_series *= np.exp(jump_sizes)
                
                data[symbol] = pd.Series(price_series, index=dates)
            
            df = pd.DataFrame(data)
            self.logger.info(f"模拟数据生成完成: {df.shape}")
            return df
            
        except Exception as e:
            self.logger.error(f"模拟数据生成失败: {str(e)}")
            # 返回简单数据作为备用
            dates = pd.date_range(end=datetime.now(), periods=days, freq='B')
            data = {}
            for symbol in symbols:
                data[symbol] = pd.Series(np.random.normal(100, 10, days), index=dates)
            return pd.DataFrame(data)
    
    def analyze_portfolio(self, symbols, weights=None, days=252):
        """分析投资组合风险"""
        try:
            self.logger.info(f"分析投资组合: {', '.join(symbols)}")
            
            # 生成模拟数据
            prices = self.simulate_market_data(symbols, days)
            
            # 确保数据长度正确
            if len(prices) < 10:
                raise ValueError(f"数据不足: 只有{len(prices)}个数据点")
            
            # 计算收益率
            returns = self._calculate_returns(prices)
            
            # 设置默认权重
            if weights is None or len(weights) != len(symbols):
                weights = np.ones(len(symbols)) / len(symbols)
            else:
                weights = np.array(weights)
                weights = weights / weights.sum()
            
            # 计算组合收益率
            portfolio_returns = (returns * weights).sum(axis=1)
            
            # 计算风险指标
            volatility = self._calculate_volatility(portfolio_returns)
            sharpe_ratio = self._calculate_sharpe_ratio(portfolio_returns)
            var_95 = self._calculate_var(portfolio_returns)
            
            # 计算相关性矩阵
            correlation_matrix = returns.corr()
            
            # 计算最大回撤
            cumulative_returns = (1 + portfolio_returns).cumprod()
            peak = cumulative_returns.expanding(min_periods=1).max()
            drawdown = (cumulative_returns - peak) / peak
            max_drawdown = drawdown.min()
            
            # 计算Beta（相对市场）
            market_returns = returns.mean(axis=1)
            covariance = portfolio_returns.cov(market_returns)
            market_variance = market_returns.var()
            beta = covariance / market_variance if market_variance != 0 else 1
            
            # 计算偏度和峰度
            skewness = portfolio_returns.skew()
            kurtosis = portfolio_returns.kurtosis()
            
            # 计算信息比率（假设基准为等权组合）
            tracking_error = (portfolio_returns - market_returns).std() * np.sqrt(252)
            information_ratio = (portfolio_returns.mean() - market_returns.mean()) / tracking_error * np.sqrt(252) if tracking_error != 0 else 0
            
            result = {
                'success': True,
                'symbols': symbols,
                'weights': weights.tolist(),
                'volatility': float(volatility),
                'sharpe_ratio': float(sharpe_ratio),
                'var_95': float(var_95),
                'max_drawdown': float(max_drawdown),
                'beta': float(beta),
                'skewness': float(skewness),
                'kurtosis': float(kurtosis),
                'information_ratio': float(information_ratio),
                'tracking_error': float(tracking_error),
                'correlation_matrix': correlation_matrix.to_dict(),
                'analysis_date': datetime.now().isoformat(),
                'period_days': days,
                'risk_free_rate': 0.02,
                'data_points': len(prices)
            }
            
            self.logger.info(f"分析完成: 波动率={volatility:.2%}, Sharpe={sharpe_ratio:.2f}, 数据点={len(prices)}")
            return result
            
        except Exception as e:
            self.logger.error(f"分析出错: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'symbols': symbols,
                'analysis_date': datetime.now().isoformat()
            }
    
    def monte_carlo_simulation(self, symbols, initial_investment=10000, simulations=10000, days=30):
        """蒙特卡洛模拟"""
        try:
            self.logger.info(f"开始蒙特卡洛模拟: {simulations}次, {days}天")
            
            # 获取历史数据计算参数
            historical_data = self.simulate_market_data(symbols, 500)  # 使用更多历史数据
            returns = self._calculate_returns(historical_data)
            
            if len(returns) < 50:
                raise ValueError("历史数据不足进行蒙特卡洛模拟")
            
            # 计算统计参数
            mean_returns = returns.mean().values
            cov_matrix = returns.cov().values
            
            # 生成随机收益率
            np.random.seed(42)
            simulated_returns = np.random.multivariate_normal(
                mean_returns, 
                cov_matrix, 
                (simulations, days)
            )
            
            # 计算最终价值
            final_values = []
            for sim in range(simulations):
                portfolio_value = initial_investment
                for day in range(days):
                    daily_return = np.mean(simulated_returns[sim, day])  # 等权组合
                    portfolio_value *= (1 + daily_return)
                final_values.append(portfolio_value)
            
            final_values = np.array(final_values)
            
            # 计算风险指标
            mean_value = np.mean(final_values)
            std_value = np.std(final_values)
            var_95 = np.percentile(final_values, 5)
            cvar_95 = final_values[final_values <= var_95].mean()
            
            # 计算置信区间
            confidence_95 = np.percentile(final_values, [2.5, 97.5])
            
            result = {
                'success': True,
                'initial_investment': initial_investment,
                'mean_final_value': float(mean_value),
                'std_final_value': float(std_value),
                'var_95': float(var_95),
                'cvar_95': float(cvar_95),
                'confidence_95': confidence_95.tolist(),
                'probability_loss': float(np.mean(final_values < initial_investment)),
                'probability_gain_10': float(np.mean(final_values > initial_investment * 1.1)),
                'probability_gain_20': float(np.mean(final_values > initial_investment * 1.2)),
                'expected_return': float((mean_value - initial_investment) / initial_investment),
                'best_case': float(np.max(final_values)),
                'worst_case': float(np.min(final_values)),
                'simulations': simulations,
                'simulation_days': days,
                'simulation_date': datetime.now().isoformat()
            }
            
            self.logger.info(f"蒙特卡洛模拟完成: 预期收益={result['expected_return']:.2%}")
            return result
            
        except Exception as e:
            self.logger.error(f"蒙特卡洛模拟出错: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'simulation_date': datetime.now().isoformat()
            }
    
    def get_risk_score(self, symbols, weights=None):
        """计算风险评分（0-10）"""
        try:
            analysis = self.analyze_portfolio(symbols, weights)
            
            if not analysis['success']:
                return {'success': False, 'error': analysis['error']}
            
            # 计算风险评分
            volatility = analysis['volatility']
            max_drawdown = abs(analysis['max_drawdown'])
            var_95 = abs(analysis['var_95'])
            
            # 归一化评分
            vol_score = min(volatility * 100, 10)
            drawdown_score = min(max_drawdown * 100, 10)
            var_score = min(abs(var_95) * 400, 10)
            
            # 考虑偏度和峰度
            skewness = abs(analysis['skewness'])
            kurtosis = analysis['kurtosis']
            
            skew_score = min(skewness * 2, 5)
            kurtosis_score = min(max(0, kurtosis - 3) * 0.5, 5)
            
            # 加权总分
            total_score = (
                vol_score * 0.3 + 
                drawdown_score * 0.25 + 
                var_score * 0.25 +
                skew_score * 0.1 +
                kurtosis_score * 0.1
            )
            
            # 风险等级
            if total_score < 3:
                risk_level = "低风险"
                color = "#10B981"  # 绿色
            elif total_score < 6:
                risk_level = "中风险"
                color = "#F59E0B"  # 黄色
            else:
                risk_level = "高风险"
                color = "#EF4444"  # 红色
            
            # 建议
            recommendations = {
                "低风险": [
                    "适合保守型投资者",
                    "可考虑增加少量成长型资产",
                    "当前配置风险控制良好"
                ],
                "中风险": [
                    "适合平衡型投资者",
                    "建议定期再平衡",
                    "保持适当现金储备"
                ],
                "高风险": [
                    "适合激进型投资者",
                    "建议设置止损点",
                    "考虑分散投资降低风险",
                    "增加债券或防御型资产"
                ]
            }
            
            return {
                'success': True,
                'risk_score': round(total_score, 2),
                'risk_level': risk_level,
                'risk_color': color,
                'components': {
                    'volatility_score': round(vol_score, 2),
                    'drawdown_score': round(drawdown_score, 2),
                    'var_score': round(var_score, 2),
                    'skewness_score': round(skew_score, 2),
                    'kurtosis_score': round(kurtosis_score, 2)
                },
                'recommendations': recommendations.get(risk_level, ["配置合理"])
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}