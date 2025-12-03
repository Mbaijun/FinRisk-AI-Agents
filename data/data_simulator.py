"""
数据模拟器 - 完全离线运行
当网络不可用时提供模拟数据
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from datetime import datetime, timedelta

class DataSimulator:
    """数据模拟器，生成模拟的股票数据"""
    
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        
        # 常见股票的基本信息（用于模拟）
        self.stock_info = {
            'AAPL': {'name': 'Apple Inc.', 'sector': 'Technology', 'base_volatility': 0.25},
            'MSFT': {'name': 'Microsoft', 'sector': 'Technology', 'base_volatility': 0.22},
            'GOOGL': {'name': 'Alphabet', 'sector': 'Technology', 'base_volatility': 0.28},
            'AMZN': {'name': 'Amazon', 'sector': 'Consumer', 'base_volatility': 0.30},
            'TSLA': {'name': 'Tesla', 'sector': 'Automotive', 'base_volatility': 0.40},
            'JPM': {'name': 'JPMorgan', 'sector': 'Financial', 'base_volatility': 0.20},
            'V': {'name': 'Visa', 'sector': 'Financial', 'base_volatility': 0.18},
            'WMT': {'name': 'Walmart', 'sector': 'Consumer', 'base_volatility': 0.15},
            'JNJ': {'name': 'Johnson & Johnson', 'sector': 'Healthcare', 'base_volatility': 0.16},
            'XOM': {'name': 'Exxon Mobil', 'sector': 'Energy', 'base_volatility': 0.24}
        }
    
    def generate_stock_data(self, symbol: str, days: int = 100) -> pd.Series:
        """生成模拟的股票价格数据"""
        info = self.stock_info.get(symbol, {
            'name': f'Stock {symbol}',
            'sector': 'General',
            'base_volatility': 0.25
        })
        
        # 生成日期范围
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days + 10)  # 多加几天确保有足够数据
        dates = pd.date_range(start=start_date, end=end_date, freq='B')  # 工作日
        dates = dates[-days:]  # 取最后days天
        
        # 基础价格（模拟）
        if symbol == 'AAPL':
            base_price = 180.0
        elif symbol == 'MSFT':
            base_price = 350.0
        elif symbol == 'GOOGL':
            base_price = 140.0
        elif symbol == 'AMZN':
            base_price = 150.0
        elif symbol == 'TSLA':
            base_price = 240.0
        else:
            base_price = 100.0
        
        # 生成价格序列
        volatility = info['base_volatility'] / np.sqrt(252)  # 日波动率
        
        # 随机游走生成价格
        returns = np.random.normal(0.0005, volatility, days)
        price_series = base_price * np.exp(np.cumsum(returns))
        
        # 添加一些趋势和季节性
        trend = np.linspace(0, 0.05 * base_price, days)  # 轻微上涨趋势
        seasonal = 2.0 * np.sin(np.linspace(0, 4*np.pi, days))
        
        price_series = price_series + trend + seasonal
        
        return pd.Series(price_series, index=dates, name=symbol)
    
    def generate_portfolio_data(self, symbols: List[str], days: int = 100) -> pd.DataFrame:
        """生成投资组合的模拟数据"""
        data_frames = []
        
        for symbol in symbols:
            price_series = self.generate_stock_data(symbol, days)
            data_frames.append(price_series)
        
        # 合并所有数据
        portfolio_data = pd.concat(data_frames, axis=1)
        
        # 确保所有日期对齐（可能会有缺失日期）
        portfolio_data = portfolio_data.dropna()
        
        return portfolio_data
    
    def get_stock_info(self, symbol: str) -> Dict:
        """获取股票信息"""
        return self.stock_info.get(symbol, {
            'name': f'Stock {symbol}',
            'sector': 'General',
            'base_volatility': 0.25
        })
