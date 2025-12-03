@echo off
chcp 65001 >nul
cls
echo.
echo ========================================
echo     FinRisk-AI-Agents 启动器
echo ========================================
echo.

REM 设置Python路径
set PYTHON=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe

REM 检查Python是否存在
if not exist "%PYTHON%" (
    echo [错误] 未找到Python
    echo 请检查路径: %PYTHON%
    pause
    exit /b 1
)

echo [信息] 使用Python: %PYTHON%
"%PYTHON%" --version

echo.
echo [步骤1] 检查依赖...
"%PYTHON%" -c "import streamlit, pandas, numpy" 2>nul
if errorlevel 1 (
    echo     正在安装必要依赖...
    "%PYTHON%" -m pip install streamlit pandas numpy plotly > nul 2>&1
    echo     依赖安装完成
) else (
    echo     依赖已安装
)

echo.
echo [步骤2] 启动FinRisk独立版...
echo     访问: http://localhost:8501
echo.
echo     按Ctrl+C停止服务
echo.

REM 启动应用
"%PYTHON%" -m streamlit run STANDALONE_APP.py --server.port 8501 --server.headless false

echo.
echo 服务已停止
pause