@echo off
chcp 65001 >nul
echo ========================================
echo   FinRisk AI Agents 启动器
echo ========================================
echo.

cd /d "C:\Users\Administrator\FinRisk-AI-Agents"

echo 🐍 检查Python...
python --version
if errorlevel 1 (
    echo ❌ Python未找到
    pause
    exit /b 1
)

echo.
echo 📦 检查依赖...
python -c "import gradio, yfinance, pandas; print('✅ 依赖检查通过')"
if errorlevel 1 (
    echo ⚠️ 缺少依赖，正在安装...
    pip install -r requirements.txt
)

echo.
echo 🚀 启动应用...
echo 🌐 访问地址: http://localhost:7860
echo.

set PYTHONPATH=%cd%;%PYTHONPATH%
python src\app_fixed2.py

echo.
if errorlevel 1 (
    echo ❌ 应用启动失败
    echo 请检查错误信息
) else (
    echo ✅ 应用已停止
)

pause
