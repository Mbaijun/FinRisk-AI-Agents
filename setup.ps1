Write-Host "Starting project creation..." -ForegroundColor Green

"agents","api","ui","config","data","models","tests","docs","logs" | ForEach-Object {
    New-Item -ItemType Directory -Force -Path $_ | Out-Null
    Write-Host "Created: $_" -ForegroundColor Gray
}

@'
# FinRisk-AI-Agents

## Quick Start
```bash
pip install -r requirements.txt
python run.py
'@ | Set-Content README.md -Encoding UTF8

@'
fastapi==0.104.1
uvicorn==0.24.0
streamlit==1.28.0
pydantic==2.5.0
pandas==2.1.3
numpy==1.24.3
yfinance==0.2.28
python-dotenv==1.0.0
loguru==0.7.2
requests==2.31.0
aiohttp==3.9.1
scipy==1.11.4
scikit-learn==1.3.2
plotly==5.17.0
pytest==7.4.3
'@ | Set-Content requirements.txt -Encoding UTF8

@'
OPENAI_API_KEY=your_key_here
DEBUG=True
API_PORT=8000
STREAMLIT_PORT=8501
'@ | Set-Content .env.example -Encoding UTF8

@'
version = "0.1.0"
author = "Mbaijun"
'@ | Set-Content init.py -Encoding UTF8

Set-Content agents_init_.py "# Agents" -Encoding UTF8

@'
import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Dict

class RiskAnalyzer:
def init(self, risk_free_rate: float = 0.02):
self.risk_free_rate = risk_free_rate

text

复制

下载
def analyze_portfolio(self, symbols: List[str], weights: List[float]) -> Dict:
    try:
        data = yf.download(symbols, period="1y")["Adj Close"]
        returns = data.pct_change().dropna()
        portfolio_returns = (returns * weights).sum(axis=1)
        
        volatility = portfolio_returns.std() * np.sqrt(252)
        var_95 = -np.percentile(portfolio_returns, 5)
        sharpe = (portfolio_returns.mean() * 252 - self.risk_free_rate) / volatility if volatility > 0 else 0
        
        return {
            "success": True,
            "volatility": float(volatility),
            "var_95": float(var_95),
            "sharpe": float(sharpe)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
'@ | Set-Content agents\risk_analyzer.py -Encoding UTF8

Set-Content api_init_.py "# API" -Encoding UTF8

@'
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
return {"message": "FinRisk API is running"}

@app.get("/health")
def health():
return {"status": "healthy"}

@app.post("/analyze")
def analyze(request: PortfolioRequest):
return analyzer.analyze_portfolio(request.symbols, request.weights)

if name == "main":
uvicorn.run(app, host="0.0.0.0", port=8000)
'@ | Set-Content api\fastapi_app.py -Encoding UTF8

Set-Content ui_init_.py "# UI" -Encoding UTF8

@'
import streamlit as st
import requests

st.set_page_config(page_title="FinRisk Dashboard", layout="wide")
st.title("FinRisk AI Agents Dashboard")

with st.sidebar:
api_url = st.text_input("API URL", "http://localhost:8000")
st.caption("Version 0.1.0")

st.header("Risk Analysis")
col1, col2 = st.columns(2)

with col1:
symbols = st.text_area("Stock Symbols", "AAPL\nMSFT\nGOOGL", height=100)

with col2:
weights = st.text_area("Weights", "0.33\n0.33\n0.34", height=100)

if st.button("Analyze", type="primary"):
try:
symbols_list = [s.strip() for s in symbols.split("\n") if s.strip()]
weights_list = [float(w.strip()) for w in weights.split("\n") if w.strip()]

text

复制

下载
    response = requests.post(
        f"{api_url}/analyze",
        json={"symbols": symbols_list, "weights": weights_list}
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            st.success("Analysis completed")
            col1, col2, col3 = st.columns(3)
            col1.metric("Volatility", f"{result['volatility']:.4f}")
            col2.metric("VaR(95%)", f"{result['var_95']:.4f}")
            col3.metric("Sharpe Ratio", f"{result['sharpe']:.2f}")
        else:
            st.error(f"Error: {result.get('error')}")
except Exception as e:
    st.error(f"Request failed: {e}")
st.caption("2023 FinRisk AI Agents")
'@ | Set-Content ui\dashboard.py -Encoding UTF8

Set-Content config_init_.py "# Config" -Encoding UTF8

@'
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
API_PORT = int(os.getenv("API_PORT", "8000"))
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))

settings = Settings()
'@ | Set-Content config\settings.py -Encoding UTF8

Set-Content tests_init_.py "# Tests" -Encoding UTF8

@'
from agents.risk_analyzer import RiskAnalyzer

def test_analyzer():
analyzer = RiskAnalyzer()
assert analyzer is not None
print("Test passed")

if name == "main":
test_analyzer()
'@ | Set-Content tests\test_basic.py -Encoding UTF8

@'
import sys
import subprocess
import threading
import time

def print_banner():
print("=" * 50)
print("FinRisk-AI-Agents Launcher")
print("=" * 50)

def install_deps():
print("Installing dependencies...")
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def start_api():
print("Starting API: http://localhost:8000")
subprocess.run([sys.executable, "-m", "api.fastapi_app"])

def start_ui():
print("Starting UI: http://localhost:8501")
subprocess.run([sys.executable, "-m", "streamlit", "run", "ui/dashboard.py", "--server.port", "8501"])

def main():
print_banner()
print("1. Install dependencies")
print("2. Start API")
print("3. Start UI")
print("4. Start all services")
print("0. Exit")

text

复制

下载
choice = input("Choice: ").strip()

if choice == "1":
    install_deps()
elif choice == "2":
    start_api()
elif choice == "3":
    start_ui()
elif choice == "4":
    install_deps()
    print("Starting all services...")
    api_thread = threading.Thread(target=start_api, daemon=True)
    ui_thread = threading.Thread(target=start_ui, daemon=True)
    api_thread.start()
    ui_thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping services...")
elif choice == "0":
    print("Goodbye!")
    sys.exit(0)
if name == "main":
main()
'@ | Set-Content run.py -Encoding UTF8

Write-Host "`nProject created successfully!" -ForegroundColor Green
Write-Host "Next steps:"
Write-Host "1. copy .env.example .env"
Write-Host "2. python run.py"