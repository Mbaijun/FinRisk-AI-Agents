# launch_finrisk.bat - Windows?????
@echo off
echo ========================================
echo     FinRisk AI Agents ???
echo ========================================
echo.

echo [1] ??????...
taskkill /F /IM python.exe /T > nul 2>&1
timeout /t 3 /nobreak > nul

echo [2] ??Python??...
set PYTHON_PATH=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe

if not exist "%PYTHON_PATH%" (
    echo ??: Python???!
    pause
    exit /b 1
)

echo [3] ??API??...
start "FinRisk API" cmd /k "%PYTHON_PATH% complete_api_fixed.py"

echo [4] ??API???...
timeout /t 8 /nobreak > nul

echo [5] ??Web??...
start "FinRisk Web" cmd /k "%PYTHON_PATH% -m streamlit run complete_app.py --server.port 8501"

echo [6] ??Web????...
timeout /t 5 /nobreak > nul

echo.
echo ========================================
echo     ? ?????
echo ========================================
echo.
echo ?? Web??: http://localhost:8501
echo ?? API??: http://localhost:8000/docs
echo ?? ????: http://localhost:8000/health
echo.
echo ?? ??:
echo   1. ?????????????
echo   2. ??????????????
echo.
echo ??????Web??...
pause > nul

start http://localhost:8501
start http://localhost:8000/docs

echo.
echo ??????...
pause > nul
