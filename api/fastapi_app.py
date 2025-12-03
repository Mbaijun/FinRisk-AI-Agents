from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
from agents.risk_analyzer import RiskAnalyzer

app = FastAPI(title="FinRisk API", version="0.1.0")
analyzer = RiskAnalyzer()

class PortfolioRequest(BaseModel):
    symbols: List[str]
    weights: List[float]

@app.get("/")
def root():
    return {"message": "FinRisk API is running", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/analyze")
def analyze(request: PortfolioRequest):
    print(f"API收到请求: {request.symbols}")
    result = analyzer.analyze_portfolio(request.symbols, request.weights)
    print(f"API返回结果: {result}")
    return result

if __name__ == "__main__":
    print("Starting FinRisk API on http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
