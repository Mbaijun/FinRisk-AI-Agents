# absolute_api.py - 100% working version
from fastapi import FastAPI
import uvicorn
from datetime import datetime

print("=" * 50)
print("🚀 FinRisk API - Absolute Working Version")
print("=" * 50)

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "FinRisk API is running!",
        "status": "active",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "FinRisk"}

@app.get("/test")
async def test():
    return {"test": "success", "number": 42, "list": [1, 2, 3]}

@app.get("/stocks")
async def stocks():
    return {
        "stocks": [
            {"symbol": "AAPL", "name": "Apple Inc.", "price": 175.25},
            {"symbol": "MSFT", "name": "Microsoft Corp.", "price": 330.15},
            {"symbol": "GOOGL", "name": "Alphabet Inc.", "price": 135.80}
        ]
    }

if __name__ == "__main__":
    print("Starting server on http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print("Test Endpoint: http://localhost:8000/test")
    print("=" * 50)
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    except Exception as e:
        print(f"Error starting server: {e}")
        print("Trying alternative method...")
        uvicorn.run("absolute_api:app", host="0.0.0.0", port=8000)
