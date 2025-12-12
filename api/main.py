"""
Vercel 部署主入口 - 兼容 Vercel Serverless Functions
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from api.endpoints import router as api_router
from utils.logger import setup_logger

# 设置日志
logger = setup_logger("vercel_app")

# 创建 FastAPI 应用
app = FastAPI(
    title="FinRisk AI Agents API",
    description="金融风险 AI 智能体系统",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件（如果存在）
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 包含 API 路由
app.include_router(api_router, prefix="/api")

# 健康检查端点
@app.get("/")
async def root():
    """根端点 - 服务状态检查"""
    return {
        "service": "FinRisk-AI-Agents",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": [
            "/api/risk/analyze",
            "/api/stress-test",
            "/api/portfolio/optimize",
            "/api/market/trends"
        ]
    }

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "timestamp": datetime.now().isoformat()}
    )

# 全局异常处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "path": request.url.path}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "内部服务器错误", "detail": str(exc)}
    )

# Vercel 需要这个变量
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)