# simple_working_api.py
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

app = FastAPI(
    title="FinRisk API - 工作版",
    description="金融风险分析API服务",
    version="1.0",
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

class ExportRequest(BaseModel):
    symbol: str
    days: int = 30
    format: str = "csv"

# 股票数据
STOCKS = {
    "AAPL": {"name": "Apple Inc.", "sector": "Technology", "price": 175.0},
    "MSFT": {"name": "Microsoft Corp.", "sector": "Technology", "price": 330.0},
    "GOOGL": {"name": "Alphabet Inc.", "sector": "Technology", "price": 135.0},
    "AMZN": {"name": "Amazon.com Inc.", "sector": "Consumer Cyclical", "price": 145.0},
    "TSLA": {"name": "Tesla Inc.", "sector": "Automotive", "price": 180.0},
    "JPM": {"name": "JPMorgan Chase & Co.", "sector": "Financial Services", "price": 170.0},
    "JNJ": {"name": "Johnson & Johnson", "sector": "Healthcare", "price": 155.0},
    "WMT": {"name": "Walmart Inc.", "sector": "Consumer Defensive", "price": 165.0},
    "NVDA": {"name": "NVIDIA Corp.", "sector": "Technology", "price": 480.0},
    "XOM": {"name": "Exxon Mobil Corp.", "sector": "Energy", "price": 105.0},
    "BRK.B": {"name": "Berkshire Hathaway", "sector": "Financial Services", "price": 360.0},
    "V": {"name": "Visa Inc.", "sector": "Financial Services", "price": 250.0},
}

def generate_data(symbol: str, days: int):
    """生成模拟数据"""
    np.random.seed(abs(hash(symbol)) % 10000)
    
    dates = pd.date_range(end=datetime.now(), periods=days, freq='B')
    base_price = STOCKS.get(symbol, {}).get("price", 100.0)
    
    # 生成收益率
    returns = np.random.normal(0.0005, 0.02, len(dates))
    
    # 计算价格
    prices = base_price * np.exp(np.cumsum(returns))
    
    return {
        "symbol": symbol,
        "name": STOCKS.get(symbol, {}).get("name", symbol),
        "sector": STOCKS.get(symbol, {}).get("sector", "Unknown"),
        "dates": [d.strftime("%Y-%m-%d") for d in dates],
        "prices": [float(p) for p in prices],
        "returns": [float(r) for r in returns],
        "volumes": [int(1000000 * (1 + np.random.rand())) for _ in range(len(dates))]
    }

@app.get("/")
async def root():
    return {"message": "FinRisk API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/stocks")
async def get_stocks():
    stocks = []
    for symbol, info in STOCKS.items():
        stocks.append({
            "symbol": symbol,
            "name": info["name"],
            "sector": info["sector"],
            "current_price": info["price"]
        })
    return {"stocks": stocks, "count": len(stocks)}

@app.get("/dashboard")
async def get_dashboard():
    """仪表板数据"""
    market_data = []
    for symbol in ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]:
        data = generate_data(symbol, 30)
        returns = np.array(data["returns"])
        
        market_data.append({
            "symbol": symbol,
            "name": STOCKS[symbol]["name"],
            "current_price": data["prices"][-1],
            "daily_change": returns[-1] * 100,
            "volatility": np.std(returns) * np.sqrt(252) * 100,
            "volume": data["volumes"][-1]
        })
    
    return {
        "market_overview": market_data,
        "risk_indicators": {
            "market_volatility": 18.5,
            "vix_index": 16.2,
            "put_call_ratio": 0.85,
            "advancers": 1245,
            "decliners": 876
        },
        "timestamp": datetime.now().isoformat()
    }

@app.post("/analyze")
async def analyze_stock(request: StockRequest):
    """分析单只股票"""
    try:
        if request.symbol not in STOCKS:
            raise HTTPException(422, f"不支持的股票: {request.symbol}")
        
        data = generate_data(request.symbol, request.days)
        prices = np.array(data["prices"])
        returns = np.array(data["returns"])
        
        # 计算指标
        volatility = np.std(returns) * np.sqrt(252)
        sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
        
        cumulative = np.cumprod(1 + returns)
        running_max = np.maximum.accumulate(cumulative)
        max_dd = np.max((running_max - cumulative) / running_max) if len(cumulative) > 0 else 0
        
        return {
            "symbol": request.symbol,
            "name": data["name"],
            "sector": data["sector"],
            "analysis_period": request.days,
            "risk_metrics": {
                "volatility": float(volatility),
                "sharpe_ratio": float(sharpe),
                "max_drawdown": float(max_dd),
                "var_95": float(np.percentile(returns, 5)),
                "cvar_95": float(np.mean(returns[returns <= np.percentile(returns, 5)]) if len(returns[returns <= np.percentile(returns, 5)]) > 0 else 0),
                "mean_return": float(np.mean(returns))
            },
            "price_summary": {
                "initial_price": float(prices[0]) if len(prices) > 0 else 0,
                "final_price": float(prices[-1]) if len(prices) > 0 else 0,
                "min_price": float(np.min(prices)) if len(prices) > 0 else 0,
                "max_price": float(np.max(prices)) if len(prices) > 0 else 0
            },
            "history": {
                "dates": data["dates"],
                "prices": data["prices"],
                "returns": data["returns"]
            }
        }
    except Exception as e:
        raise HTTPException(500, f"分析失败: {str(e)}")

@app.post("/portfolio/analyze")
async def analyze_portfolio(request: PortfolioRequest):
    """分析投资组合"""
    try:
        if len(request.symbols) != len(request.weights):
            raise HTTPException(422, "股票和权重数量不匹配")
        
        total_weight = sum(request.weights)
        if abs(total_weight - 1.0) > 0.001:
            raise HTTPException(422, f"权重总和必须为1.0，当前为{total_weight:.3f}")
        
        # 生成各股票数据
        stock_data = []
        for symbol in request.symbols:
            if symbol not in STOCKS:
                raise HTTPException(422, f"不支持的股票: {symbol}")
            data = generate_data(symbol, request.days)
            stock_data.append({
                "symbol": symbol,
                "returns": np.array(data["returns"])
            })
        
        # 计算组合
        portfolio_returns = np.zeros(request.days)
        for i, stock in enumerate(stock_data):
            portfolio_returns += stock["returns"] * request.weights[i]
        
        portfolio_vol = np.std(portfolio_returns) * np.sqrt(252)
        portfolio_sharpe = np.mean(portfolio_returns) / np.std(portfolio_returns) * np.sqrt(252) if np.std(portfolio_returns) > 0 else 0
        
        # 分析各股票
        stock_analysis = []
        for i, stock in enumerate(stock_data):
            stock_vol = np.std(stock["returns"]) * np.sqrt(252)
            stock_analysis.append({
                "symbol": stock["symbol"],
                "weight": float(request.weights[i]),
                "volatility": float(stock_vol),
                "expected_return": float(np.mean(stock["returns"]) * 252),
                "contribution": float(request.weights[i] * stock_vol)
            })
        
        return {
            "portfolio_summary": {
                "symbols": request.symbols,
                "weights": [float(w) for w in request.weights],
                "expected_return": float(np.mean(portfolio_returns) * 252),
                "volatility": float(portfolio_vol),
                "sharpe_ratio": float(portfolio_sharpe)
            },
            "stock_analysis": stock_analysis,
            "analysis_period": request.days
        }
    except Exception as e:
        raise HTTPException(500, f"组合分析失败: {str(e)}")

@app.post("/report/generate")
async def generate_report(request: StockRequest):
    """生成报告"""
    try:
        # 获取分析数据
        analysis = await analyze_stock(request)
        
        return {
            "report_id": f"REPORT_{request.symbol}_{datetime.now().strftime('%Y%m%d')}",
            "generated_at": datetime.now().isoformat(),
            "stock": request.symbol,
            "analysis": analysis,
            "summary": {
                "risk_level": "低风险" if analysis["risk_metrics"]["volatility"] < 0.2 else "中等风险" if analysis["risk_metrics"]["volatility"] < 0.3 else "高风险",
                "recommendation": "推荐投资" if analysis["risk_metrics"]["sharpe_ratio"] > 1.0 else "谨慎投资",
                "key_points": [
                    f"波动率: {analysis['risk_metrics']['volatility']:.2%}",
                    f"夏普比率: {analysis['risk_metrics']['sharpe_ratio']:.2f}",
                    f"最大回撤: {analysis['risk_metrics']['max_drawdown']:.2%}"
                ]
            }
        }
    except Exception as e:
        raise HTTPException(500, f"报告生成失败: {str(e)}")

@app.post("/export")
async def export_data(request: ExportRequest):
    """导出数据"""
    try:
        data = generate_data(request.symbol, request.days)
        
        if request.format.lower() == "csv":
            df = pd.DataFrame({
                "Date": data["dates"],
                "Price": data["prices"],
                "Return": data["returns"],
                "Volume": data["volumes"]
            })
            
            csv_content = df.to_csv(index=False)
            return {
                "filename": f"{request.symbol}_data.csv",
                "content": csv_content,
                "format": "csv",
                "size": len(csv_content)
            }
        
        elif request.format.lower() == "json":
            return {
                "filename": f"{request.symbol}_data.json",
                "content": data,
                "format": "json",
                "size": len(str(data))
            }
        
        else:
            raise HTTPException(422, "只支持csv或json格式")
            
    except Exception as e:
        raise HTTPException(500, f"导出失败: {str(e)}")

if __name__ == "__main__":
    print("Starting FinRisk API...")
    print(f"Available stocks: {', '.join(STOCKS.keys())}")
    print("Docs: http://localhost:8000/docs")
    print("Health: http://localhost:8000/health")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
