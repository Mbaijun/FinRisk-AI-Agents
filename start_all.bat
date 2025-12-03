# start_all.bat - 一键启动所有服务
@echo off
chcp 65001 > nul
echo ========================================
echo     FinRisk AI Agents - 完整启动
echo ========================================
echo.

echo [1] 停止现有进程...
taskkill /F /IM python.exe /T > nul 2>&1
timeout /t 3 /nobreak > nul

echo [2] 设置Python路径...
set PYTHON_PATH=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe

if not exist "%PYTHON_PATH%" (
    echo 错误: Python未找到!
    pause
    exit /b 1
)

echo [3] 启动API服务...
start "FinRisk API" cmd /k "%PYTHON_PATH% fixed_api_complete.py"
echo    等待API启动...
timeout /t 10 /nobreak > nul

echo [4] 测试API连接...
powershell -Command "try { $result = Invoke-RestMethod -Uri 'http://localhost:8000/health' -TimeoutSec 5; Write-Host 'API状态: ' -NoNewline; Write-Host '$($result.status)' -ForegroundColor Green } catch { Write-Host 'API连接失败' -ForegroundColor Red }"
echo.

echo [5] 启动Web界面...
start "FinRisk Web" cmd /k "%PYTHON_PATH% -m streamlit run complete_app.py --server.port 8501"
echo    等待Web界面启动...
timeout /t 5 /nobreak > nul

echo.
echo ========================================
echo     ✅ 启动完成！
echo ========================================
echo.
echo 🌐 Web界面: http://localhost:8501
echo 📖 API文档: http://localhost:8000/docs
echo 🩺 健康检查: http://localhost:8000/health
echo.
echo 📝 支持的股票:
echo    AAPL, MSFT, GOOGL, GOOG, AMZN, TSLA, JPM
echo    JNJ, WMT, NVDA, XOM, BRK.B, BRK-B, V
echo.
echo 按任意键打开Web界面和API文档...
pause > nul

start http://localhost:8501
start http://localhost:8000/docs

echo.
echo 按任意键退出此窗口...
pause > nul
