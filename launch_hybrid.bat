@echo off
chcp 65001 >nul
echo ========================================
echo   FinRisk AI Agents 混合模式启动器
echo ========================================
echo.

cd /d "C:\Users\Administrator\FinRisk-AI-Agents"

echo 🤖 启动混合智能模式...
echo 💡 特性: 实时API + 本地模拟 + 智能缓存
echo 🌐 访问: http://localhost:7860
echo.

set PYTHONPATH=%cd%;%PYTHONPATH%
python src\app_hybrid.py

pause
