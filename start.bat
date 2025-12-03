@echo off
chcp 65001 > nul
echo ========================================
echo FinRisk-AI-Agents 启动器
echo ========================================

:: 检查Python
python --version
if errorlevel 1 (
    echo Python未找到
    pause
    exit /b 1
)

echo.
echo 启动FinRisk-AI-Agents...
echo.

:: 启动API服务
echo [1/2] 启动API服务 (端口: 8000)...
start "FinRisk API" python api\fastapi_app.py

:: 等待API启动
timeout /t 3 /nobreak > nul

:: 启动Web界面
echo [2/2] 启动Web界面 (端口: 8501)...
start "FinRisk Web" python -m streamlit run ui\dashboard.py --server.port 8501

echo.
echo ========================================
echo 服务已启动！
echo.
echo 访问地址：
echo   Web界面: http://localhost:8501
echo   API文档: http://localhost:8000/docs
echo.
echo 按任意键停止服务...
pause > nul

:: 停止服务
taskkill /f /im python.exe 2>nul
taskkill /f /im streamlit.exe 2>nul

echo 服务已停止
pause