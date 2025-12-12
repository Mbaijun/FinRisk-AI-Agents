@echo off
chcp 65001 >nul
echo ========================================
echo   FinRisk AI Agents 终极版启动器
echo ========================================
echo.

cd /d "%~dp0"

echo 🚀 启动终极本地版...
echo ✅ 特性: 零依赖 | 100%%本地 | 永不失败
echo 🌐 访问: http://localhost:7860
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请安装Python 3.8+
    pause
    exit /b 1
)

REM 启动应用
python app_ultimate.py

if errorlevel 1 (
    echo.
    echo ❌ 启动失败，请检查错误信息
    pause
)
