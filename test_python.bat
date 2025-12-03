@echo off
echo Testing Python installation...
echo.

echo 1. Checking if python is in PATH...
where python
echo.

echo 2. Trying python --version...
python --version
echo.

echo 3. Trying py launcher...
py --version
echo.

echo 4. Running a simple Python script...
echo print("Hello from Python") > test_python.py
python test_python.py
echo.

echo 5. Checking Python installation directories...
dir /b C:\Python* 2>nul
dir /b "%USERPROFILE%\AppData\Local\Programs\Python" 2>nul
echo.

pause
