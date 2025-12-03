@echo off
chcp 65001 >nul
cls

echo ========================================
echo    FinRisk-AI-Agents 安装程序
echo ========================================
echo.

echo [1/4] 检查Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   错误: 未找到Python
    echo   请从 https://python.org 下载安装Python 3.8+
    pause
    exit /b 1
)

python -c "import sys; print(f'Python {sys.version}')"

echo.
echo [2/4] 安装依赖...
pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo   警告: 某些依赖安装失败
    echo   尝试继续安装...
)

echo.
echo [3/4] 验证安装...
python -c "
try:
    import fastapi, streamlit, pandas, numpy
    print('   核心依赖验证通过')
except ImportError as e:
    print(f'   错误: {e}')
"

echo.
echo [4/4] 创建快捷方式...
echo @echo off > start.bat
echo python -m uvicorn finrisk_ai.api:app --host 0.0.0.0 --port 8000 >> start.bat

echo.
echo ========================================
echo    安装完成！
echo.
echo    运行以下命令启动：
echo    1. API服务: python -m uvicorn finrisk_ai.api:app
echo    2. Web界面: python -m streamlit run app.py
echo    3. 或双击 start_final.bat 一键启动
echo ========================================
echo.

pause