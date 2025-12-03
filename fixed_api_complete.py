# fixed_api_complete.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import uvicorn
import json
from scipy import stats
import plotly.graph_objects as go

app = FastAPI(
    title="FinRisk API v2.0",
    description="金融风险分析API服务",
    version="2.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class StockRequest(BaseModel):
    symbol: str
    days: int = 30

class PortfolioRequest(BaseModel):
    symbols: List[str]
    weights: List[float]
    days: int = 30

# 支持的股票列表
SUPPORTED_STOCKS = {
    "AAPL": {"name": "Apple Inc.", "sector": "Technology"},
    "MSFT": {"name": "Microsoft Corp.", "sector": "Technology"},
    "GOOGL": {"name": "Alphabet Inc.", "sector": "Technology"},
    "GOOG": {"name": "Alphabet Inc.", "sector": "Technology"},
    "AMZN": {"name": "Amazon.com Inc.", "sector": "Consumer Cyclical"},
    "TSLA": {"name": "Tesla Inc.", "sector": "Automotive"},
    "JPM": {"name": "JPMorgan Chase & Co.", "sector": "Financial Services"},
    "JNJ": {"name": "Johnson & Johnson", "sector": "Healthcare"},
    "WMT": {"name": "Walmart Inc.", "sector": "Consumer Defensive"},
    "NVDA": {"name": "NVIDIA Corp.", "sector": "Technology"},
    "XOM": {"name": "Exxon Mobil Corp.", "sector": "Energy"},
    "BRK.B": {"name": "Berkshire Hathaway", "sector": "Financial Services"},
    "BRK-B": {"name": "Berkshire Hathaway", "sector": "Financial Services"},
    "V": {"name": "Visa Inc.", "sector": "Financial Services"},
}

def generate_stock_data(symbol: str, days: int = 30):
    """生成模拟股票数据"""
    np.random.seed(abs(hash(symbol)) % 10000)
    
    # 生成日期
    dates = pd.date_range(end=datetime.now(), periods=days, freq='B')
    
    # 基础价格（基于股票代码）
    base_price = 50 + (abs(hash(symbol)) % 1000)
    
    # 生成收益率
    daily_returns = np.random.normal(0.0005, 0.02, days)
    
    # 计算价格
    prices = base_price * np.exp(np.cumsum(daily_returns))
    
    return {
        "symbol": symbol,
        "name": SUPPORTED_STOCKS.get(symbol, {}).get("name", symbol),
        "sector": SUPPORTED_STOCKS.get(symbol, {}).get("sector", "Unknown"),
        "prices": [float(p) for p in prices],
        "dates": [d.strftime("%Y-%m-%d") for d in dates],
        "returns": [float(r) for r in daily_returns],
        "volume": [int(1000000 * (1 + np.random.rand())) for _ in range(days)]
    }

@app.get("/")
def root():
    return {
        "message": "FinRisk API v2.0",
        "endpoints": {
            "/health": "健康检查",
            "/docs": "API文档",
            "/stocks": "可用股票列表",
            "/analyze": "分析单只股票",
            "/portfolio": "分析投资组合"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/stocks")
def get_stocks():
    """获取支持的股票列表"""
    stocks = list(SUPPORTED_STOCKS.keys())
    stock_details = []
    for symbol in stocks:
        stock_details.append({
            "symbol": symbol,
            "name": SUPPORTED_STOCKS[symbol]["name"],
            "sector": SUPPORTED_STOCKS[symbol]["sector"]
        })
    
    return {
        "stocks": stocks,
        "details": stock_details,
        "count": len(stocks)
    }

@app.post("/analyze")
def analyze_stock(request: StockRequest):
    """分析单只股票"""
    # 检查股票是否支持
    if request.symbol not in SUPPORTED_STOCKS:
        raise HTTPException(
            status_code=400, 
            detail=f"股票代码 '{request.symbol}' 不支持。支持的股票: {', '.join(SUPPORTED_STOCKS.keys())}"
        )
    
    # 检查天数
    if request.days < 1 or request.days > 365:
        raise HTTPException(
            status_code=400,
            detail="分析天数必须在1到365之间"
        )
    
    try:
        # 生成数据
        data = generate_stock_data(request.symbol, request.days)
        returns = np.array(data["returns"])
        prices = np.array(data["prices"])
        
        # 计算基本统计
        if len(returns) == 0:
            raise HTTPException(status_code=500, detail="无法生成收益率数据")
        
        # 计算风险指标
        volatility = np.std(returns) * np.sqrt(252)
        mean_return = np.mean(returns)
        sharpe_ratio = mean_return / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
        
        # 计算最大回撤
        cumulative_returns = np.cumprod(1 + returns)
        peak = np.maximum.accumulate(cumulative_returns)
        drawdown = (peak - cumulative_returns) / peak
        max_drawdown = np.max(drawdown) if len(drawdown) > 0 else 0
        
        # 计算VaR和CVaR
        var_95 = np.percentile(returns, 5)
        cvar_95 = np.mean(returns[returns <= var_95]) if len(returns[returns <= var_95]) > 0 else var_95
        
        # 计算相关性（模拟）
        correlation_matrix = np.eye(len(SUPPORTED_STOCKS))
        
        return {
            "symbol": request.symbol,
            "name": SUPPORTED_STOCKS[request.symbol]["name"],
            "sector": SUPPORTED_STOCKS[request.symbol]["sector"],
            "analysis_period": request.days,
            "data_points": len(prices),
            "risk_metrics": {
                "volatility": float(volatility),
                "sharpe_ratio": float(sharpe_ratio),
                "max_drawdown": float(max_drawdown),
                "var_95": float(var_95),
                "cvar_95": float(cvar_95),
                "mean_return": float(mean_return),
                "total_return": float(cumulative_returns[-1] - 1 if len(cumulative_returns) > 0 else 0)
            },
            "price_summary": {
                "initial_price": float(prices[0]) if len(prices) > 0 else 0,
                "final_price": float(prices[-1]) if len(prices) > 0 else 0,
                "min_price": float(np.min(prices)) if len(prices) > 0 else 0,
                "max_price": float(np.max(prices)) if len(prices) > 0 else 0
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")

@app.post("/portfolio")
def analyze_portfolio(request: PortfolioRequest):
    """分析投资组合"""
    # 验证输入
    if len(request.symbols) != len(request.weights):
        raise HTTPException(
            status_code=400, 
            detail="股票数量必须与权重数量相同"
        )
    
    if abs(sum(request.weights) - 1.0) > 0.001:
        raise HTTPException(
            status_code=400,
            detail="权重总和必须为1.0"
        )
    
    # 检查所有股票是否支持
    invalid_stocks = [s for s in request.symbols if s not in SUPPORTED_STOCKS]
    if invalid_stocks:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的股票代码: {', '.join(invalid_stocks)}"
        )
    
    try:
        # 为每只股票生成数据
        stock_data = []
        for symbol in request.symbols:
            data = generate_stock_data(symbol, request.days)
            stock_data.append({
                "symbol": symbol,
                "returns": np.array(data["returns"]),
                "prices": np.array(data["prices"])
            })
        
        # 计算组合收益率
        portfolio_returns = np.zeros(request.days)
        for i, data in enumerate(stock_data):
            portfolio_returns += data["returns"] * request.weights[i]
        
        # 计算组合风险指标
        portfolio_volatility = np.std(portfolio_returns) * np.sqrt(252)
        portfolio_mean_return = np.mean(portfolio_returns)
        portfolio_sharpe = portfolio_mean_return / np.std(portfolio_returns) * np.sqrt(252) if np.std(portfolio_returns) > 0 else 0
        
        # 计算相关性矩阵
        n_stocks = len(request.symbols)
        correlation_matrix = np.eye(n_stocks)
        for i in range(n_stocks):
            for j in range(i+1, n_stocks):
                corr = np.corrcoef(stock_data[i]["returns"], stock_data[j]["returns"])[0,1]
                correlation_matrix[i,j] = corr
                correlation_matrix[j,i] = corr
        
        # 计算每只股票的贡献
        stock_contributions = []
        for i, data in enumerate(stock_data):
            stock_vol = np.std(data["returns"]) * np.sqrt(252)
            stock_sharpe = np.mean(data["returns"]) / np.std(data["returns"]) * np.sqrt(252) if np.std(data["returns"]) > 0 else 0
            
            stock_contributions.append({
                "symbol": data["symbol"],
                "weight": float(request.weights[i]),
                "volatility": float(stock_vol),
                "sharpe_ratio": float(stock_sharpe),
                "contribution_to_risk": float(request.weights[i] * stock_vol)
            })
        
        return {
            "portfolio_summary": {
                "symbols": request.symbols,
                "weights": [float(w) for w in request.weights],
                "expected_return": float(portfolio_mean_return * 252),
                "volatility": float(portfolio_volatility),
                "sharpe_ratio": float(portfolio_sharpe),
                "diversification_benefit": float(1 - (portfolio_volatility / sum([w * np.std(d["returns"]) * np.sqrt(252) for w, d in zip(request.weights, stock_data)])))
            },
            "stock_analysis": stock_contributions,
            "correlation_matrix": correlation_matrix.tolist(),
            "analysis_period": request.days
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"投资组合分析失败: {str(e)}")

if __name__ == "__main__":
    print("Starting FinRisk API v2.0 (Fixed Version)...")
    print(f"Available stocks: {', '.join(SUPPORTED_STOCKS.keys())}")
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
