@echo off
chcp 65001 >nul
cls
echo.
echo 
echo          FinRisk-AI-Agents ????           
echo 
echo.

set PYTHON=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe

echo [??] ?????...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im streamlit.exe >nul 2>&1
timeout /t 3 >nul

echo.
echo [1/2] ????Web??...
echo     ??: http://localhost:8501
start "FinRisk Web" cmd /k "cd /d %~dp0 && %PYTHON% -m streamlit run STANDALONE_APP.py --server.port 8501 --global.disableWatchdogWarning true --server.headless false"
timeout /t 5 >nul

echo.
echo [2/2] ??API??...
echo     ??: http://localhost:8000/docs
start "FinRisk API" cmd /k "cd /d %~dp0 && %PYTHON% simple_fastapi.py"
timeout /t 3 >nul

echo.
echo 
echo              ??????                    
echo 
echo                                               
echo   ?? Web??: http://localhost:8501          
echo   ? API??: http://localhost:8000/docs     
echo                                               
echo   ????????                           
echo   ???????????...                 
echo                                               
echo 
echo.

pause >nul
echo.
echo ??????????????????
echo      ??? cleanup.bat
