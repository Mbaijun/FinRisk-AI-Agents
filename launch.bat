@echo off
chcp 65001 > nul
echo ========================================
echo     FinRisk AI Agents - ????
echo ========================================
echo.

echo [1] Stopping existing processes...
taskkill /F /IM python.exe /T > nul 2>&1
timeout /t 3 /nobreak > nul

echo [2] Setting up environment...
set PYTHON_PATH=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe
set API_PORT=8000
set WEB_PORT=8501

if not exist "%PYTHON_PATH%" (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo [3] Starting API service...
start "FinRisk API" cmd /k "%PYTHON_PATH% simple_working_api.py"
echo    Waiting for API startup...
timeout /t 10 /nobreak > nul

echo [4] Testing API connection...
powershell -Command "try { Invoke-RestMethod -Uri 'http://localhost:8000/health' -TimeoutSec 5 > $null; echo [OK] API is healthy } catch { echo [ERROR] API connection failed; exit 1 }"
echo.

echo [5] Starting Web interface...
start "FinRisk Web" cmd /k "%PYTHON_PATH% -m streamlit run web_app_encoded.py --server.port %WEB_PORT%"
echo    Waiting for Web interface...
timeout /t 8 /nobreak > nul

echo.
echo ========================================
echo     [SUCCESS] System started!
echo ========================================
echo.
echo Web Interface: http://localhost:%WEB_PORT%
echo API Docs: http://localhost:%API_PORT%/docs
echo Health Check: http://localhost:%API_PORT%/health
echo.
echo Features:
echo   * Dashboard - Market overview
echo   * Single Stock Analysis - Risk metrics
echo   * Portfolio Analysis - Multi-stock portfolio
echo   * Data Reports - Generate and export reports
echo.
echo Press any key to open Web interface...
pause > nul

start http://localhost:%WEB_PORT%
start http://localhost:%API_PORT%/docs

echo.
echo Note: Do not close the two command windows!
echo Press any key to exit this window...
pause > nul
