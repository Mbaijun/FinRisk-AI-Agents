# complete_fixed_api.py
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
import plotly.express as px
from io import StringIO, BytesIO
import base64

app = FastAPI(
    title="FinRisk API v3.0",
    description="完整的金融风险分析API服务",
    version="3.0",
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
    format: str = "csv"  # csv, json, excel

# 支持的股票列表
STOCK_DATA = {
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

def generate_stock_history(symbol: str, days: int):
    """生成股票历史数据"""
    np.random.seed(abs(hash(symbol)) % 10000)
    
    # 生成日期
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days*1.5)  # 考虑非交易日
    dates = pd.date_range(start=start_date, end=end_date, freq='B')[-days:]
    
    # 基础价格
    base_info = STOCK_DATA.get(symbol, {"price": 100.0})
    base_price = base_info["price"]
    
    # 生成收益率序列
    if symbol in ["AAPL", "MSFT", "GOOGL"]:
        volatility = 0.018
    elif symbol in ["TSLA", "NVDA"]:
        volatility = 0.025
    else:
        volatility = 0.015
    
    daily_returns = np.random.normal(0.0008, volatility, len(dates))
    
    # 计算价格
    prices = base_price * np.exp(np.cumsum(daily_returns))
    
    # 生成成交量
    volumes = np.random.lognormal(14, 0.8, len(dates)).astype(int)
    
    return {
        "dates": [d.strftime("%Y-%m-%d") for d in dates],
        "prices": [float(p) for p in prices],
        "returns": [float(r) for r in daily_returns],
        "volumes": [int(v) for v in volumes]
    }

@app.get("/")
async def root():
    return {
        "message": "FinRisk API v3.0",
        "version": "3.0",
        "endpoints": {
            "/health": "健康检查",
            "/docs": "API文档",
            "/dashboard": "仪表板数据",
            "/stocks": "可用股票列表",
            "/analyze": "单股票分析",
            "/portfolio/analyze": "投资组合分析",
            "/report/generate": "生成数据报告",
            "/export": "导出数据"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/stocks")
async def get_stocks():
    """获取所有股票信息"""
    stocks = []
    for symbol, info in STOCK_DATA.items():
        stocks.append({
            "symbol": symbol,
            "name": info["name"],
            "sector": info["sector"],
            "current_price": info["price"]
        })
    
    return {
        "stocks": stocks,
        "count": len(stocks),
        "sectors": list(set([info["sector"] for info in STOCK_DATA.values()]))
    }

@app.get("/dashboard")
async def get_dashboard():
    """获取仪表板数据"""
    try:
        # 市场概况数据
        market_data = []
        for symbol in ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]:
            history = generate_stock_history(symbol, 30)
            returns = np.array(history["returns"])
            
            market_data.append({
                "symbol": symbol,
                "name": STOCK_DATA[symbol]["name"],
                "current_price": history["prices"][-1],
                "daily_change": returns[-1] * 100,
                "volatility": np.std(returns) * np.sqrt(252) * 100,
                "volume": history["volumes"][-1]
            })
        
        # 风险指标
        risk_indicators = {
            "market_volatility": 18.5,
            "vix_index": 16.2,
            "put_call_ratio": 0.85,
            "advancers": 1245,
            "decliners": 876,
            "unchanged": 234
        }
        
        # 热门行业
        sectors = {}
        for info in STOCK_DATA.values():
            sector = info["sector"]
            sectors[sector] = sectors.get(sector, 0) + 1
        
        return {
            "market_overview": market_data,
            "risk_indicators": risk_indicators,
            "sector_distribution": sectors,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"仪表板数据生成失败: {str(e)}")

@app.post("/analyze")
async def analyze_stock(request: StockRequest):
    """分析单只股票"""
    try:
        # 验证输入
        if request.days < 1 or request.days > 365:
            raise HTTPException(status_code=422, detail="分析天数必须在1到365之间")
        
        if request.symbol not in STOCK_DATA:
            raise HTTPException(status_code=422, detail=f"不支持的股票代码: {request.symbol}")
        
        # 生成数据
        history = generate_stock_history(request.symbol, request.days)
        prices = np.array(history["prices"])
        returns = np.array(history["returns"])
        
        if len(returns) == 0:
            raise HTTPException(status_code=500, detail="无法生成收益率数据")
        
        # 计算风险指标
        volatility = np.std(returns) * np.sqrt(252)  # 年化波动率
        mean_return = np.mean(returns)
        sharpe_ratio = mean_return / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
        
        # 计算最大回撤
        cumulative = np.cumprod(1 + returns)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (running_max - cumulative) / running_max
        max_drawdown = np.max(drawdown) if len(drawdown) > 0 else 0
        
        # 计算VaR和CVaR
        var_95 = np.percentile(returns, 5)
        cvar_95 = np.mean(returns[returns <= var_95]) if len(returns[returns <= var_95]) > 0 else var_95
        
        # 计算统计信息
        skewness = stats.skew(returns)
        kurtosis = stats.kurtosis(returns)
        
        return {
            "symbol": request.symbol,
            "name": STOCK_DATA[request.symbol]["name"],
            "sector": STOCK_DATA[request.symbol]["sector"],
            "analysis_period": request.days,
            "data_points": len(prices),
            "risk_metrics": {
                "volatility": float(volatility),
                "sharpe_ratio": float(sharpe_ratio),
                "max_drawdown": float(max_drawdown),
                "var_95": float(var_95),
                "cvar_95": float(cvar_95),
                "mean_return": float(mean_return),
                "total_return": float(cumulative[-1] - 1 if len(cumulative) > 0 else 0),
                "skewness": float(skewness),
                "kurtosis": float(kurtosis)
            },
            "price_summary": {
                "initial_price": float(prices[0]) if len(prices) > 0 else 0,
                "final_price": float(prices[-1]) if len(prices) > 0 else 0,
                "min_price": float(np.min(prices)) if len(prices) > 0 else 0,
                "max_price": float(np.max(prices)) if len(prices) > 0 else 0,
                "average_price": float(np.mean(prices)) if len(prices) > 0 else 0
            },
            "history": history
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"股票分析失败: {str(e)}")

@app.post("/portfolio/analyze")
async def analyze_portfolio(request: PortfolioRequest):
    """分析投资组合"""
    try:
        # 验证输入
        if len(request.symbols) != len(request.weights):
            raise HTTPException(status_code=422, detail="股票数量必须与权重数量相同")
        
        total_weight = sum(request.weights)
        if abs(total_weight - 1.0) > 0.001:
            raise HTTPException(status_code=422, detail=f"权重总和必须为1.0，当前为{total_weight:.3f}")
        
        invalid_stocks = [s for s in request.symbols if s not in STOCK_DATA]
        if invalid_stocks:
            raise HTTPException(status_code=422, detail=f"不支持的股票代码: {', '.join(invalid_stocks)}")
        
        if request.days < 1 or request.days > 365:
            raise HTTPException(status_code=422, detail="分析天数必须在1到365之间")
        
        # 生成各股票数据
        stock_histories = []
        for symbol in request.symbols:
            history = generate_stock_history(symbol, request.days)
            stock_histories.append({
                "symbol": symbol,
                "history": history,
                "returns": np.array(history["returns"])
            })
        
        # 计算组合收益率
        portfolio_returns = np.zeros(request.days)
        for i, stock in enumerate(stock_histories):
            portfolio_returns += stock["returns"] * request.weights[i]
        
        # 计算组合风险指标
        portfolio_volatility = np.std(portfolio_returns) * np.sqrt(252)
        portfolio_mean_return = np.mean(portfolio_returns)
        portfolio_sharpe = portfolio_mean_return / np.std(portfolio_returns) * np.sqrt(252) if np.std(portfolio_returns) > 0 else 0
        
        # 计算相关性矩阵
        n_stocks = len(request.symbols)
        correlation_matrix = np.eye(n_stocks)
        for i in range(n_stocks):
            for j in range(i+1, n_stocks):
                corr = np.corrcoef(stock_histories[i]["returns"], stock_histories[j]["returns"])[0,1]
                correlation_matrix[i,j] = corr
                correlation_matrix[j,i] = corr
        
        # 计算各股票贡献
        stock_analysis = []
        for i, stock in enumerate(stock_histories):
            stock_vol = np.std(stock["returns"]) * np.sqrt(252)
            stock_sharpe = np.mean(stock["returns"]) / np.std(stock["returns"]) * np.sqrt(252) if np.std(stock["returns"]) > 0 else 0
            
            stock_analysis.append({
                "symbol": stock["symbol"],
                "name": STOCK_DATA[stock["symbol"]]["name"],
                "weight": float(request.weights[i]),
                "volatility": float(stock_vol),
                "sharpe_ratio": float(stock_sharpe),
                "expected_return": float(np.mean(stock["returns"]) * 252),
                "contribution_to_risk": float(request.weights[i] * stock_vol)
            })
        
        # 计算分散化效益
        weighted_vol = sum([w * np.std(s["returns"]) * np.sqrt(252) for w, s in zip(request.weights, stock_histories)])
        diversification_benefit = 1 - (portfolio_volatility / weighted_vol) if weighted_vol > 0 else 0
        
        return {
            "portfolio_summary": {
                "symbols": request.symbols,
                "weights": [float(w) for w in request.weights],
                "expected_return": float(portfolio_mean_return * 252),
                "volatility": float(portfolio_volatility),
                "sharpe_ratio": float(portfolio_sharpe),
                "diversification_benefit": float(diversification_benefit),
                "max_drawdown": float(np.max((np.maximum.accumulate(1+portfolio_returns) - (1+portfolio_returns)) / np.maximum.accumulate(1+portfolio_returns)) if len(portfolio_returns) > 0 else 0)
            },
            "stock_analysis": stock_analysis,
            "correlation_matrix": correlation_matrix.tolist(),
            "analysis_period": request.days
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"投资组合分析失败: {str(e)}")

@app.post("/report/generate")
async def generate_report(request: StockRequest):
    """生成数据报告"""
    try:
        # 先获取分析数据
        analysis_data = await analyze_stock(request)
        
        # 生成报告内容
        report = {
            "report_id": f"REPORT_{request.symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "generated_at": datetime.now().isoformat(),
            "stock_analysis": analysis_data,
            "summary": {
                "risk_level": "中等" if analysis_data["risk_metrics"]["volatility"] < 0.25 else "较高",
                "investment_suggestion": "适合长期投资" if analysis_data["risk_metrics"]["sharpe_ratio"] > 1.0 else "建议谨慎投资",
                "key_risks": ["市场波动风险", "行业政策风险", "汇率风险"] if analysis_data["stock_analysis"]["sector"] == "Technology" else ["市场波动风险"]
            },
            "charts": {
                "price_chart": f"data:image/png;base64,{generate_chart_base64(request.symbol, request.days)}",
                "distribution_chart": f"data:image/png;base64,{generate_distribution_base64(analysis_data['history']['returns'])}"
            }
        }
        
        return report
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"报告生成失败: {str(e)}")

@app.post("/export")
async def export_data(request: ExportRequest):
    """导出数据"""
    try:
        # 获取数据
        history = generate_stock_history(request.symbol, request.days)
        
        # 创建DataFrame
        df = pd.DataFrame({
            "Date": history["dates"],
            "Price": history["prices"],
            "Daily_Return": history["returns"],
            "Volume": history["volumes"]
        })
        
        if request.format.lower() == "csv":
            csv_string = df.to_csv(index=False)
            return {
                "filename": f"{request.symbol}_{request.days}d_{datetime.now().strftime('%Y%m%d')}.csv",
                "content": csv_string,
                "format": "csv",
                "size": len(csv_string)
            }
            
        elif request.format.lower() == "json":
            json_data = df.to_dict(orient="records")
            return {
                "filename": f"{request.symbol}_{request.days}d_{datetime.now().strftime('%Y%m%d')}.json",
                "content": json_data,
                "format": "json",
                "size": len(str(json_data))
            }
            
        else:
            raise HTTPException(status_code=422, detail="不支持的数据格式，请使用csv或json")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"数据导出失败: {str(e)}")

def generate_chart_base64(symbol: str, days: int):
    """生成图表并转换为base64"""
    try:
        history = generate_stock_history(symbol, days)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=history["dates"],
            y=history["prices"],
            mode='lines',
            name=symbol,
            line=dict(color='blue', width=2)
        ))
        
        fig.update_layout(
            title=f"{symbol} Price Chart ({days} days)",
            xaxis_title="Date",
            yaxis_title="Price",
            height=400,
            width=600
        )
        
        # 转换为base64
        img_bytes = fig.to_image(format="png")
        return base64.b64encode(img_bytes).decode('utf-8')
        
    except:
        return ""

def generate_distribution_base64(returns):
    """生成收益率分布图"""
    try:
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=returns,
            nbinsx=30,
            name="Returns Distribution",
            marker_color='green'
        ))
        
        fig.update_layout(
            title="Returns Distribution",
            xaxis_title="Daily Return",
            yaxis_title="Frequency",
            height=300,
            width=400
        )
        
        img_bytes = fig.to_image(format="png")
        return base64.b64encode(img_bytes).decode('utf-8')
        
    except:
        return ""

if __name__ == "__main__":
    print("Starting FinRisk API v3.0...")
    print(f"Available stocks: {', '.join(STOCK_DATA.keys())}")
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
