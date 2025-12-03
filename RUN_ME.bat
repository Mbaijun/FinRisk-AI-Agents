@echo off
chcp 65001 >nul
cls
echo.
echo ███████╗██╗███╗   ██╗██████╗ ██╗██████╗ ██╗  ██╗
echo ██╔════╝██║████╗  ██║██╔══██╗██║██╔══██╗██║ ██╔╝
echo █████╗  ██║██╔██╗ ██║██████╔╝██║██████╔╝█████╔╝
echo ██╔══╝  ██║██║╚██╗██║██╔══██╗██║██╔══██╗██╔═██╗
echo ██║     ██║██║ ╚████║██║  ██║██║██║  ██║██║  ██╗
echo ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
echo.
echo             FinRisk-AI-Agents 启动器
echo.

set PYTHON=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe

if not exist "%PYTHON%" (
    echo [错误] Python未找到
    echo 请确保Python已安装在此路径
    pause
    exit /b 1
)

echo [信息] 使用: %PYTHON%
%PYTHON% --version

echo.
echo [1/2] 启动独立Web应用...
start "FinRisk Web" cmd /k "cd /d %~dp0 && %PYTHON% -m streamlit run STANDALONE_APP.py --server.port 8501"
timeout /t 3 >nul

echo [2/2] 启动API服务(可选)...
start "FinRisk API" cmd /k "cd /d %~dp0 && %PYTHON% -m uvicorn finrisk_ai.api:app --host 0.0.0.0 --port 8000" 2>nul
timeout /t 2 >nul

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                        启动完成！                         ║
echo ╠══════════════════════════════════════════════════════════╣
echo ║                                                          ║
echo ║  ✅ 主应用: http://localhost:8501                       ║
echo ║  ⚡ API服务: http://localhost:8000/docs (如果启动)       ║
echo ║                                                          ║
echo ║  按任意键停止服务...                                     ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

pause >nul

echo.
echo [清理] 停止所有服务...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im streamlit.exe >nul 2>&1
echo [完成] 服务已停止