Write-Host "FinRisk-AI-Agents ????" -ForegroundColor Green
Write-Host "=" * 70

# ?????Python??
$pythonExe = "C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe"
$pythonDir = "C:\Users\Administrator\AppData\Local\Programs\Python\Python311"

if (-not (Test-Path $pythonExe)) {
    Write-Host "??: Python???? $pythonExe" -ForegroundColor Red
    Write-Host "???????Python??" -ForegroundColor Yellow
    exit 1
}

# ????PATH
$env:PATH = "$pythonDir;$pythonDir\Scripts;$env:PATH"

Write-Host "1. ??Python: $pythonExe" -ForegroundColor Yellow
Write-Host "   ??: $(& $pythonExe --version)" -ForegroundColor Cyan

# ???????
Write-Host "`n2. ????..." -ForegroundColor Yellow
$deps = @("fastapi", "uvicorn", "streamlit", "pandas", "numpy", "plotly", "requests")
foreach ($dep in $deps) {
    & $pythonExe -c "try: import $dep; print('? $dep')`nexcept: print('? $dep')"
}

Write-Host "`n3. ??Streamlit??..." -ForegroundColor Yellow
if (Test-Path .streamlit\config.toml) {
    Remove-Item .streamlit\config.toml -Force
}
if (-not (Test-Path .streamlit)) {
    New-Item -ItemType Directory -Force .streamlit
}
@"
[theme]
primaryColor = "#1E3A8A"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
address = "0.0.0.0"
enableCORS = false

[browser]
gatherUsageStats = false
"@ | Out-File .streamlit\config.toml -Encoding ASCII
Write-Host "   Streamlit?????" -ForegroundColor Green

# ???????????
Write-Host "`n4. ???????..." -ForegroundColor Yellow

# ????????
@'
@echo off
chcp 65001 >nul
cls
echo.
echo 
echo                  FinRisk-AI-Agents ???                 
echo 
echo.

set PYTHON=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe

if not exist "%PYTHON%" (
    echo [??] ???Python: %PYTHON%
    pause
    exit /b 1
)

echo [??] ??Python: %PYTHON%
%PYTHON% --version

echo.
echo [??1/3] ????...
%PYTHON% -c "import fastapi, streamlit" 2>nul
if errorlevel 1 (
    echo    ??????...
    %PYTHON% -m pip install fastapi uvicorn streamlit pandas numpy plotly requests > nul 2>&1
    echo    ??????
) else (
    echo    ?????
)

echo.
echo [??2/3] ??API?? (??: 8000)...
start "FinRisk API" cmd /k "cd /d %~dp0 && %PYTHON% -m uvicorn finrisk_ai.api:app --host 0.0.0.0 --port 8000"
timeout /t 5 >nul

echo.
echo [??3/3] ??Web?? (??: 8501)...
start "FinRisk Web" cmd /k "cd /d %~dp0 && %PYTHON% -m streamlit run app.py --server.port 8501"
timeout /t 3 >nul

echo.
echo 
echo                         ?????                         
echo 
echo                                                           
echo   Web??: http://localhost:8501                         
echo   API??: http://localhost:8000/docs                    
echo                                                           
echo   ??????????...                                 
echo                                                           
echo 
echo.

pause >nul

echo.
echo [??] ??????...
taskkill /f /im python.exe >nul 2>&1
echo [??] ?????
