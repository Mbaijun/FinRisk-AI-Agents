# launch_system.bat
@echo off
chcp 65001 > nul
echo ========================================
echo     FinRisk AI Agents - 完整系统启动
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

echo [3] 启动API服务 (v3.0)...
start "FinRisk API v3.0" cmd /k "%PYTHON_PATH% complete_fixed_api.py"
echo    等待API启动...
timeout /t 10 /nobreak > nul

echo [4] 测试API连接...
powershell -Command "try { `$result = Invoke-RestMethod -Uri 'http://localhost:8000/health' -TimeoutSec 5; Write-Host 'API状态: ' -NoNewline; Write-Host '`$(`$result.status)' -ForegroundColor Green } catch { Write-Host 'API连接失败' -ForegroundColor Red; exit 1 }"
echo.

echo [5] 启动Web界面...
start "FinRisk Web" cmd /k "%PYTHON_PATH% -m streamlit run web_app_fixed.py --server.port 8501"
echo    等待Web界面启动...
timeout /t 8 /nobreak > nul

echo.
echo ========================================
echo     ✅ 系统启动完成！
echo ========================================
echo.
echo 🌐 Web界面: http://localhost:8501
echo 📖 API文档: http://localhost:8000/docs
echo 🩺 健康检查: http://localhost:8000/health
echo.
echo 📝 支持的股票 (12只):
echo    AAPL, MSFT, GOOGL, AMZN, TSLA, JPM
echo    JNJ, WMT, NVDA, XOM, BRK.B, V
echo.
echo 🚀 功能列表:
echo   • 仪表板 - 市场概览和风险指标
echo   • 单股票分析 - 详细风险分析
echo   • 投资组合分析 - 多股票组合优化
echo   • 数据报告 - 完整报告生成和导出
echo.
echo 按任意键打开Web界面...
pause > nul

start http://localhost:8501
start http://localhost:8000/docs

echo.
echo 按任意键退出此窗口...
pause > nul
