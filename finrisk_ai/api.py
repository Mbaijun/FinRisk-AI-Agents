# finrisk_ai/api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from finrisk_ai.risk_analyzer import RiskAnalyzer

# 创建FastAPI应用
app = FastAPI(
    title="FinRisk-AI-Agents API",
    description="金融风险AI分析系统API",
    version="1.0.0",
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

# 初始化分析器
analyzer = RiskAnalyzer(offline_mode=True)

# 数据模型
class PortfolioRequest(BaseModel):
    symbols: List[str]
    weights: Optional[List[float]] = None
    days: Optional[int] = 252

class MonteCarloRequest(BaseModel):
    symbols: List[str]
    initial_investment: Optional[float] = 10000
    simulations: Optional[int] = 10000
    days: Optional[int] = 30

# API端点
@app.get("/")
async def root():
    return {
        "service": "FinRisk-AI-Agents API",
        "version": "1.0.0",
        "status": "running",
        "mode": "offline_simulation",
        "endpoints": {
            "健康检查": "/health",
            "投资组合分析": "/analyze/portfolio",
            "风险评分": "/analyze/risk-score",
            "蒙特卡洛模拟": "/simulate/monte-carlo"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "FinRisk-AI-Agents"}

@app.post("/analyze/portfolio")
async def analyze_portfolio(request: PortfolioRequest):
    try:
        result = analyzer.analyze_portfolio(
            symbols=request.symbols,
            weights=request.weights,
            days=request.days
        )
        
        if not result.get('success', False):
            raise HTTPException(status_code=400, detail=result.get('error', '分析失败'))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/risk-score")
async def get_risk_score(request: PortfolioRequest):
    try:
        result = analyzer.get_risk_score(
            symbols=request.symbols,
            weights=request.weights
        )
        
        if not result.get('success', False):
            raise HTTPException(status_code=400, detail=result.get('error', '计算失败'))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/simulate/monte-carlo")
async def monte_carlo_simulation(request: MonteCarloRequest):
    try:
        result = analyzer.monte_carlo_simulation(
            symbols=request.symbols,
            initial_investment=request.initial_investment,
            simulations=request.simulations,
            days=request.days
        )
        
        if not result.get('success', False):
            raise HTTPException(status_code=400, detail=result.get('error', '模拟失败'))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/symbols/popular")
async def get_popular_symbols():
    """获取常用股票列表"""
    symbols = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
        "META", "NVDA", "JPM", "JNJ", "V",
        "WMT", "PG", "MA", "UNH", "HD",
        "BAC", "XOM", "CVX", "KO", "PEP"
    ]
    return {
        "symbols": symbols,
        "count": len(symbols),
        "categories": {
            "科技": ["AAPL", "MSFT", "GOOGL", "META", "NVDA"],
            "消费": ["AMZN", "TSLA", "WMT", "KO", "PEP"],
            "金融": ["JPM", "V", "MA", "BAC"],
            "医疗": ["JNJ", "UNH"],
            "能源": ["XOM", "CVX"],
            "工业": ["HD", "PG"]
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "finrisk_ai.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )