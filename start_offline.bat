@echo off
chcp 65001 > nul
echo ========================================
echo FinRisk-AI-Agents 离线版启动器
echo ========================================

:: 设置Python完整路径
set PYTHON_PATH=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe

echo 使用Python: %PYTHON_PATH%
%PYTHON_PATH% --version

echo.
echo 测试离线分析器...
%PYTHON_PATH% -c "
from agents.risk_analyzer import RiskAnalyzer
analyzer = RiskAnalyzer()
result = analyzer.analyze_portfolio(['AAPL','MSFT','GOOGL'],[0.3,0.4,0.3])
print('离线测试:', '成功' if result.get('success') else '失败')
if result.get('success'):
    print('波动率:', result.get('volatility'))
    print('夏普比率:', result.get('sharpe'))
"

echo.
echo 启动离线版FinRisk-AI-Agents...
echo.

:: 启动API服务
echo [1/2] 启动API服务 (端口: 8000)...
start "FinRisk API (离线版)" "%PYTHON_PATH%" api\fastapi_app.py

:: 等待API启动
timeout /t 5 /nobreak > nul

:: 启动Web界面
echo [2/2] 启动Web界面 (端口: 8501)...
start "FinRisk Web (离线版)" "%PYTHON_PATH%" -m streamlit run ui\dashboard.py --server.port 8501 --server.address localhost --server.enableCORS false --server.enableXsrfProtection false

echo.
echo ========================================
echo 离线版服务已启动！
echo.
echo 访问地址：
echo   Web界面: http://localhost:8501
echo   API文档: http://localhost:8000/docs
echo   API测试: http://localhost:8000/health
echo.
echo 注意：当前为离线模拟模式
echo.       所有数据均为模拟生成，用于演示目的
echo.       实际投资决策请使用真实数据
echo.
echo 按任意键停止服务...
pause > nul

:: 停止服务
taskkill /f /im python.exe 2>nul
taskkill /f /im streamlit.exe 2>nul

echo 服务已停止
pause