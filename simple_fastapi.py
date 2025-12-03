from fastapi import FastAPI
import uvicorn

app = FastAPI(title="FinRisk API", version="1.0")

@app.get("/")
def root():
    return {
        "service": "FinRisk-AI-Agents API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "test": "/test"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "FinRisk"}

@app.get("/test")
def test():
    return {"message": "API is working", "test": "success"}

if __name__ == "__main__":
    print("=" * 50)
    print("FinRisk API 服务启动")
    print("访问: http://localhost:8000/docs")
    print("按 Ctrl+C 停止")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
