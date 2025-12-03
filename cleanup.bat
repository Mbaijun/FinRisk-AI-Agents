@echo off
chcp 65001 >nul
echo.
echo ??FinRisk??...
echo.
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im streamlit.exe >nul 2>&1
echo ?????????
echo.
pause
