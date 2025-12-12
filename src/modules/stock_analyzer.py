# ============================================================================
# 股票分析模块
# ============================================================================

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from typing import Dict, List, Optional, Tuple

class StockAnalyzer:
    """股票分析器"""
    
    @staticmethod
    def get_stock_data(ticker: str, period: str = "1mo") -> Optional[Dict]:
        """获取股票数据"""
        try:
            stock = yf.Ticker(ticker)
            
            # 获取历史数据
            hist = stock.history(period=period)
            if hist.empty:
                return None
            
            # 获取基本信息
            info = stock.info
            
            return {
                'history': hist,
                'info': info,
                'ticker': ticker,
                'success': True
            }
        except Exception as e:
            print(f"获取股票数据失败 {ticker}: {e}")
            return {
                'ticker': ticker,
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def calculate_risk_metrics(data: Dict) -> Dict:
        """计算风险指标"""
        if not data.get('success', False):
            return data
        
        hist = data['history']
        info = data['info']
        
        result = {
            'ticker': data['ticker'],
            'success': True,
            'analysis_time': datetime.now().isoformat()
        }
        
        try:
            # 基础信息
            if not hist.empty:
                result['current_price'] = float(hist['Close'].iloc[-1])
                result['previous_close'] = float(hist['Close'].iloc[-2]) if len(hist) > 1 else result['current_price']
                result['daily_change_pct'] = ((result['current_price'] / result['previous_close']) - 1) * 100
                result['volume'] = int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0
            
            # 公司信息
            result['company_name'] = info.get('longName', data['ticker'])
            result['market_cap'] = info.get('marketCap', 0)
            result['sector'] = info.get('sector', '未知')
            result['industry'] = info.get('industry', '未知')
            
            # 计算技术指标
            if len(hist) >= 10:
                closes = hist['Close'].values
                
                # 移动平均线
                if len(closes) >= 20:
                    result['ma_20'] = float(np.mean(closes[-20:]))
                    result['ma_50'] = float(np.mean(closes[-min(50, len(closes)):]))
                
                # 回报率
                returns = hist['Close'].pct_change().dropna()
                if len(returns) > 1:
                    # 年化波动率
                    volatility = returns.std() * np.sqrt(252)
                    result['volatility_annual'] = float(volatility)
                    
                    # 夏普比率 (简化)
                    risk_free_rate = 0.03  # 假设无风险利率3%
                    excess_returns = returns - risk_free_rate/252
                    sharpe = np.sqrt(252) * excess_returns.mean() / excess_returns.std() if excess_returns.std() > 0 else 0
                    result['sharpe_ratio'] = float(sharpe)
                    
                    # 最大回撤
                    cum_returns = (1 + returns).cumprod()
                    running_max = cum_returns.expanding().max()
                    drawdown = (cum_returns - running_max) / running_max
                    result['max_drawdown'] = float(drawdown.min())
                    
                    # 计算风险评分 (0-10)
                    risk_score = min(10, max(0, 
                        volatility * 5 +  # 波动率
                        abs(result.get('beta', 1) - 1) * 2 +  # 贝塔风险
                        max(0, -result.get('max_drawdown', 0)) * 3  # 回撤风险
                    ))
                    result['risk_score'] = float(risk_score)
                    
                    # 风险等级
                    if risk_score >= 7:
                        result['risk_level'] = "高风险"
                        result['recommendation'] = "谨慎投资，建议设置止损"
                    elif risk_score >= 4:
                        result['risk_level'] = "中风险"
                        result['recommendation'] = "适度配置，分散投资"
                    else:
                        result['risk_level'] = "低风险"
                        result['recommendation'] = "适合稳健型投资者"
            
            # 添加从 info 获取的其他指标
            result['beta'] = info.get('beta', 1.0)
            result['pe_ratio'] = info.get('trailingPE', 0)
            result['forward_pe'] = info.get('forwardPE', 0)
            result['dividend_yield'] = info.get('dividendYield', 0)
            result['profit_margins'] = info.get('profitMargins', 0)
            
        except Exception as e:
            result['success'] = False
            result['error'] = f"指标计算失败: {str(e)}"
        
        return result
    
    @staticmethod
    def format_analysis_result(result: Dict) -> str:
        """格式化分析结果为可读文本"""
        if not result.get('success', False):
            return f"❌ 分析失败: {result.get('error', '未知错误')}"
        
        output = f"# 📊 {result['ticker']} - {result.get('company_name', '')}\n\n"
        
        # 价格信息
        if 'current_price' in result:
            output += f"## 💰 价格信息\n"
            output += f"- **当前价格**: \n"
            if 'daily_change_pct' in result:
                change_icon = "📈" if result['daily_change_pct'] > 0 else "📉"
                output += f"- **今日涨跌**: {change_icon} {result['daily_change_pct']:+.2f}%\n"
            if 'previous_close' in result:
                output += f"- **昨收**: \n"
            output += "\n"
        
        # 公司信息
        output += f"## 🏢 公司信息\n"
        output += f"- **行业**: {result.get('sector', '未知')} / {result.get('industry', '未知')}\n"
        if result.get('market_cap', 0) > 0:
            market_cap_b = result['market_cap'] / 1e9
            output += f"- **市值**: B\n"
        output += "\n"
        
        # 估值指标
        output += f"## 📈 估值指标\n"
        if result.get('pe_ratio'):
            output += f"- **市盈率 (P/E)**: {result['pe_ratio']:.2f}\n"
        if result.get('forward_pe'):
            output += f"- **前瞻市盈率**: {result['forward_pe']:.2f}\n"
        if result.get('dividend_yield'):
            output += f"- **股息率**: {result['dividend_yield']*100:.2f}%\n"
        output += "\n"
        
        # 风险指标
        output += f"## ⚠️ 风险分析\n"
        
        if 'risk_score' in result:
            risk_score = result['risk_score']
            risk_bar = "" * int(risk_score) + "░" * (10 - int(risk_score))
            color = "🔴" if risk_score >= 7 else "🟡" if risk_score >= 4 else "🟢"
            
            output += f"- **风险评分**: {color} {risk_score:.1f}/10\n"
            output += f"  {risk_bar}\n"
            output += f"- **风险等级**: {result.get('risk_level', '未知')}\n"
        
        if 'volatility_annual' in result:
            output += f"- **年化波动率**: {result['volatility_annual']*100:.2f}%\n"
        
        if 'beta' in result:
            beta = result['beta']
            beta_desc = "高风险" if beta > 1.2 else "低风险" if beta < 0.8 else "市场同步"
            output += f"- **贝塔系数**: {beta:.2f} ({beta_desc})\n"
        
        if 'max_drawdown' in result:
            output += f"- **最大回撤**: {result['max_drawdown']*100:.2f}%\n"
        
        if 'sharpe_ratio' in result:
            sharpe = result['sharpe_ratio']
            sharpe_eval = "优秀" if sharpe > 1 else "一般" if sharpe > 0 else "较差"
            output += f"- **夏普比率**: {sharpe:.2f} ({sharpe_eval})\n"
        
        output += "\n"
        
        # 投资建议
        if 'recommendation' in result:
            output += f"## 🎯 投资建议\n"
            output += f"{result['recommendation']}\n\n"
        
        output += f"---\n"
        output += f"*分析时间: {result.get('analysis_time', datetime.now().isoformat())}*\n"
        
        return output
    
    @staticmethod
    def analyze_stock(ticker: str, period: str = "1mo") -> str:
        """分析股票的完整流程"""
        data = StockAnalyzer.get_stock_data(ticker, period)
        if data and data.get('success'):
            result = StockAnalyzer.calculate_risk_metrics(data)
            return StockAnalyzer.format_analysis_result(result)
        else:
            return f"❌ 无法获取股票数据: {ticker}\n请检查股票代码是否正确，或尝试其他代码如 AAPL、MSFT。"

# ============================================================================
