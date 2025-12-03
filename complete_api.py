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
import plotly.io as pio

app = FastAPI(
    title="FinRisk API v2.0",
    description="完整的金融风险分析API服务",
    version="2.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== 数据模型 ==========
class StockRequest(BaseModel):
    stock_code: str
    analysis_days: int
    simulation_count: Optional[int] = 10000

class PortfolioRequest(BaseModel):
    stocks: List[str]
    weights: List[float]
    analysis_days: int

class RiskMetrics(BaseModel):
    stock_code: str
    analysis_days: int
    timestamp: str
    basic_metrics: Dict[str, float]
    var_metrics: Dict[str, float]
    performance_metrics: Dict[str, float]
    distribution_stats: Dict[str, float]
    simulated_data: Dict[str, List[float]]

class PortfolioMetrics(BaseModel):
    portfolio: List[str]
    weights: List[float]
    metrics: Dict[str, float]
    correlation_matrix: List[List[float]]

# ========== 全局数据 ==========
STOCK_INFO = {
    "AAPL": {"name": "Apple Inc.", "sector": "Technology", "volatility": 0.25, "return": 0.08},
    "MSFT": {"name": "Microsoft Corporation", "sector": "Technology", "volatility": 0.20, "return": 0.07},
    "GOOGL": {"name": "Alphabet Inc.", "sector": "Communication", "volatility": 0.22, "return": 0.06},
    "AMZN": {"name": "Amazon.com Inc.", "sector": "Consumer Cyclical", "volatility": 0.30, "return": 0.10},
    "TSLA": {"name": "Tesla Inc.", "sector": "Automotive", "volatility": 0.50, "return": 0.15},
    "JPM": {"name": "JPMorgan Chase & Co.", "sector": "Financial", "volatility": 0.18, "return": 0.05},
    "JNJ": {"name": "Johnson & Johnson", "sector": "Healthcare", "volatility": 0.15, "return": 0.04},
    "WMT": {"name": "Walmart Inc.", "sector": "Consumer Defensive", "volatility": 0.16, "return": 0.04},
    "NVDA": {"name": "NVIDIA Corporation", "sector": "Technology", "volatility": 0.35, "return": 0.12},
    "XOM": {"name": "Exxon Mobil Corporation", "sector": "Energy", "volatility": 0.20, "return": 0.06},
    "BRK.B": {"name": "Berkshire Hathaway", "sector": "Financial", "volatility": 0.17, "return": 0.05},
    "V": {"name": "Visa Inc.", "sector": "Financial", "volatility": 0.19, "return": 0.06},
}

# ========== 工具函数 ==========
def generate_stock_returns(stock_code: str, days: int) -> np.ndarray:
    """生成股票收益率序列"""
    if stock_code not in STOCK_INFO:
        # 默认值
        daily_vol = 0.25 / np.sqrt(252)
        daily_return = 0.05 / 252
    else:
        info = STOCK_INFO[stock_code]
        daily_vol = info["volatility"] / np.sqrt(252)
        daily_return = info["return"] / 252
    
    # 生成收益率（添加随机游走）
    np.random.seed(hash(stock_code) % 10000)
    returns = np.random.randn(days) * daily_vol + daily_return
    
    # 添加一些自相关性
    for i in range(1, len(returns)):
        returns[i] = 0.1 * returns[i-1] + 0.9 * returns[i]
    
    return returns

def calculate_metrics(returns: np.ndarray) -> Dict[str, Any]:
    """计算所有风险指标"""
    # 基本统计
    daily_mean = np.mean(returns)
    daily_std = np.std(returns)
    annual_return = daily_mean * 252 * 100
    annual_volatility = daily_std * np.sqrt(252) * 100
    
    # 夏普比率（无风险利率2%）
    risk_free_rate = 0.02
    sharpe_ratio = (annual_return/100 - risk_free_rate) / (annual_volatility/100) if annual_volatility > 0 else 0
    
    # 索提诺比率（只考虑下行风险）
    downside_returns = returns[returns < 0]
    downside_std = np.std(downside_returns) if len(downside_returns) > 0 else 0
    sortino_ratio = (annual_return/100 - risk_free_rate) / (downside_std * np.sqrt(252)) if downside_std > 0 else 0
    
    # VaR计算
    var_95 = np.percentile(returns, 5) * 100
    var_99 = np.percentile(returns, 1) * 100
    
    # CVaR
    cvar_95 = np.mean(returns[returns <= np.percentile(returns, 5)]) * 100
    cvar_99 = np.mean(returns[returns <= np.percentile(returns, 1)]) * 100
    
    # 最大回撤
    cumulative = (1 + returns).cumprod()
    running_max = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = np.min(drawdown) * 100
    max_drawdown_duration = np.argmax(drawdown) - np.argmin(drawdown[:np.argmax(drawdown)]) if np.argmax(drawdown) > 0 else 0
    
    # 偏度和峰度
    skewness = stats.skew(returns)
    kurtosis = stats.kurtosis(returns)
    
    # 正态性检验
    if len(returns) > 3:
        _, normality_p = stats.normaltest(returns)
    else:
        normality_p = 1.0
    
    # 收益分布分位数
    percentiles = np.percentile(returns * 100, [1, 5, 10, 25, 50, 75, 90, 95, 99])
    
    return {
        "basic": {
            "annual_return": round(annual_return, 2),
            "annual_volatility": round(annual_volatility, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "sortino_ratio": round(sortino_ratio, 2),
            "daily_mean": round(daily_mean * 100, 3),
            "daily_std": round(daily_std * 100, 3),
        },
        "var": {
            "var_95": round(var_95, 2),
            "var_99": round(var_99, 2),
            "cvar_95": round(abs(cvar_95), 2),
            "cvar_99": round(abs(cvar_99), 2),
            "expected_shortfall": round(abs(cvar_95), 2),
        },
        "drawdown": {
            "max_drawdown": round(abs(max_drawdown), 2),
            "max_drawdown_duration": int(max_drawdown_duration),
            "recovery_period": int(max_drawdown_duration * 1.5),
        },
        "distribution": {
            "skewness": round(skewness, 3),
            "kurtosis": round(kurtosis, 3),
            "normality_p": round(normality_p, 4),
            "min": round(np.min(returns) * 100, 2),
            "max": round(np.max(returns) * 100, 2),
            "percentiles": {f"p{p}": round(val, 2) for p, val in zip([1,5,10,25,50,75,90,95,99], percentiles)}
        }
    }

# ========== API端点 ==========
@app.get("/")
async def root():
    return {
        "service": "FinRisk API v2.0",
        "version": "2.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            {"path": "/", "method": "GET", "description": "API信息"},
            {"path": "/health", "method": "GET", "description": "健康检查"},
            {"path": "/stocks", "method": "GET", "description": "获取股票列表"},
            {"path": "/analyze", "method": "POST", "description": "单股票风险分析"},
            {"path": "/analyze/portfolio", "method": "POST", "description": "投资组合分析"},
            {"path": "/simulate/{stock}/{days}", "method": "GET", "description": "快速模拟"},
            {"path": "/compare", "method": "POST", "description": "多股票比较"}
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "FinRisk API",
        "version": "2.0",
        "timestamp": datetime.now().isoformat(),
        "uptime": "running",
        "memory_usage": "normal"
    }

@app.get("/stocks")
async def get_stocks():
    """获取所有支持的股票信息"""
    stocks = []
    for code, info in STOCK_INFO.items():
        stocks.append({
            "code": code,
            "name": info["name"],
            "sector": info["sector"],
            "expected_return": info["return"],
            "expected_volatility": info["volatility"]
        })
    
    return {
        "stocks": stocks,
        "count": len(stocks),
        "sectors": list(set([info["sector"] for info in STOCK_INFO.values()]))
    }

@app.get("/stock/{stock_code}")
async def get_stock_info(stock_code: str):
    """获取单个股票信息"""
    if stock_code not in STOCK_INFO:
        raise HTTPException(status_code=404, detail=f"股票代码 {stock_code} 不存在")
    
    info = STOCK_INFO[stock_code]
    return {
        "code": stock_code,
        "name": info["name"],
        "sector": info["sector"],
        "expected_annual_return": info["return"],
        "expected_annual_volatility": info["volatility"],
        "description": f"{info['name']} ({stock_code}) - {info['sector']} sector"
    }

@app.post("/analyze", response_model=RiskMetrics)
async def analyze_single_stock(request: StockRequest):
    """单股票风险分析"""
    
    # 参数验证
    if request.analysis_days <= 0:
        raise HTTPException(status_code=400, detail="分析天数必须大于0")
    
    if request.simulation_count <= 0:
        raise HTTPException(status_code=400, detail="模拟次数必须大于0")
    
    # 生成收益率数据
    returns = generate_stock_returns(request.stock_code, request.analysis_days)
    
    # 计算所有指标
    metrics = calculate_metrics(returns)
    
    # 生成模拟数据用于前端显示
    np.random.seed(42)
    simulated_returns = np.random.randn(min(5000, request.simulation_count)) * np.std(returns)
    
    # 生成价格路径
    price_paths = []
    for _ in range(5):  # 5条价格路径
        path = 100 * (1 + np.cumsum(np.random.randn(request.analysis_days) * np.std(returns) + np.mean(returns)))
        price_paths.append(path.tolist())
    
    return RiskMetrics(
        stock_code=request.stock_code,
        analysis_days=request.analysis_days,
        timestamp=datetime.now().isoformat(),
        basic_metrics=metrics["basic"],
        var_metrics=metrics["var"],
        performance_metrics=metrics["drawdown"],
        distribution_stats=metrics["distribution"],
        simulated_data={
            "daily_returns": (returns * 100).tolist(),
            "cumulative_returns": ((1 + returns).cumprod() * 100).tolist(),
            "drawdown_series": (np.minimum.accumulate((1 + returns).cumprod() / np.maximum.accumulate((1 + returns).cumprod()) - 1) * 100).tolist(),
            "simulated_distribution": simulated_returns.tolist(),
            "price_paths": price_paths
        }
    )

@app.post("/analyze/portfolio")
async def analyze_portfolio(request: PortfolioRequest):
    """投资组合风险分析"""
    
    # 参数验证
    if len(request.stocks) != len(request.weights):
        raise HTTPException(status_code=400, detail="股票数量必须与权重数量相同")
    
    if abs(sum(request.weights) - 1.0) > 0.01:
        raise HTTPException(status_code=400, detail="权重总和必须为1")
    
    if request.analysis_days <= 0:
        raise HTTPException(status_code=400, detail="分析天数必须大于0")
    
    # 生成各股票收益率
    stock_returns = []
    for stock in request.stocks:
        returns = generate_stock_returns(stock, request.analysis_days)
        stock_returns.append(returns)
    
    stock_returns = np.array(stock_returns)
    weights = np.array(request.weights)
    
    # 计算组合收益率
    portfolio_returns = weights @ stock_returns
    
    # 计算组合指标
    metrics = calculate_metrics(portfolio_returns)
    
    # 计算相关性矩阵
    correlation_matrix = np.corrcoef(stock_returns).tolist()
    
    # 计算组合波动率
    cov_matrix = np.cov(stock_returns)
    portfolio_variance = weights @ cov_matrix @ weights
    portfolio_volatility = np.sqrt(portfolio_variance) * np.sqrt(252) * 100
    
    return {
        "portfolio": request.stocks,
        "weights": request.weights,
        "metrics": {
            **metrics["basic"],
            "portfolio_volatility": round(portfolio_volatility, 2),
            "diversification_benefit": round((1 - portfolio_volatility / np.mean([STOCK_INFO[s]["volatility"]*100 for s in request.stocks])) * 100, 1)
        },
        "correlation_matrix": correlation_matrix,
        "component_volatilities": {stock: round(STOCK_INFO.get(stock, {"volatility": 0.25})["volatility"]*100, 1) for stock in request.stocks},
        "timestamp": datetime.now().isoformat()
    }

@app.get("/simulate/{stock_code}/{days}")
async def quick_simulate(stock_code: str, days: int = 252):
    """快速模拟（用于测试）"""
    if days <= 0 or days > 5000:
        raise HTTPException(status_code=400, detail="天数必须在1-5000之间")
    
    request = StockRequest(stock_code=stock_code, analysis_days=days)
    return await analyze_single_stock(request)

@app.get("/dashboard")
async def get_dashboard_data():
    """获取仪表板数据"""
    # 生成一些示例数据
    np.random.seed(42)
    
    top_performers = []
    for code in ["NVDA", "TSLA", "AMZN", "AAPL", "MSFT"]:
        returns = generate_stock_returns(code, 252)
        metrics = calculate_metrics(returns)
        top_performers.append({
            "stock": code,
            "return": metrics["basic"]["annual_return"],
            "volatility": metrics["basic"]["annual_volatility"],
            "sharpe": metrics["basic"]["sharpe_ratio"]
        })
    
    # 按夏普比率排序
    top_performers.sort(key=lambda x: x["sharpe"], reverse=True)
    
    return {
        "market_summary": {
            "total_stocks": len(STOCK_INFO),
            "avg_volatility": round(np.mean([info["volatility"] for info in STOCK_INFO.values()]) * 100, 1),
            "avg_return": round(np.mean([info["return"] for info in STOCK_INFO.values()]) * 100, 1),
            "update_time": datetime.now().isoformat()
        },
        "top_performers": top_performers[:5],
        "sector_breakdown": {
            "Technology": len([s for s, info in STOCK_INFO.items() if info["sector"] == "Technology"]),
            "Financial": len([s for s, info in STOCK_INFO.items() if info["sector"] == "Financial"]),
            "Healthcare": len([s for s, info in STOCK_INFO.items() if info["sector"] == "Healthcare"]),
            "Consumer": len([s for s, info in STOCK_INFO.items() if info["sector"] in ["Consumer Cyclical", "Consumer Defensive"]]),
            "Other": len([s for s, info in STOCK_INFO.items() if info["sector"] not in ["Technology", "Financial", "Healthcare", "Consumer Cyclical", "Consumer Defensive"]])
        }
    }

if __name__ == "__main__":
    print(" Starting FinRisk API v2.0...")
    print(f" Available stocks: {', '.join(STOCK_INFO.keys())}")
    print(" API Documentation: http://localhost:8000/docs")
    print(" Health Check: http://localhost:8000/health")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


