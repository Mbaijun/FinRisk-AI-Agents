@echo off
echo Stopping existing processes...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM ngrok.exe 2>nul
timeout /t 2 /nobreak >nul

echo Starting Gradio demo...
start cmd /k "python demo_final_simple.py"

echo Waiting for Gradio to start...
timeout /t 5 /nobreak >nul

echo Starting ngrok tunnel...
start cmd /k "ngrok.exe http 7890"

echo.
echo ========================================
echo 1. Open browser to: http://localhost:7890
echo 2. Check ngrok window for public URL
echo 3. Add header to bypass warning
echo ========================================
pause