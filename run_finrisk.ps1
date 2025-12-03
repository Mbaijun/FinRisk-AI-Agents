# run_finrisk.ps1 - Run FinRisk with correct Python
$ErrorActionPreference = "Continue"

Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host "FinRisk AI Agents - Starting with correct Python" -ForegroundColor Yellow
Write-Host "=" * 50 -ForegroundColor Cyan

# Set correct Python path
$pythonExe = "C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "ERROR: Python not found at $pythonExe" -ForegroundColor Red
    exit 1
}

Write-Host "Using Python: $pythonExe" -ForegroundColor Green
& $pythonExe --version

# Check files
if (-not (Test-Path "complete_api.py")) {
    Write-Host "ERROR: complete_api.py not found" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "complete_app.py")) {
    Write-Host "ERROR: complete_app.py not found" -ForegroundColor Red
    exit 1
}

Write-Host "`nStarting API service..." -ForegroundColor Green
Start-Process -FilePath $pythonExe -ArgumentList "complete_api.py" -NoNewWindow -PassThru

Start-Sleep -Seconds 3

# Test API
Write-Host "`nTesting API..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 5
    Write-Host "API Status: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "API not responding yet, continuing..." -ForegroundColor Yellow
}

Write-Host "`nStarting Web interface..." -ForegroundColor Green
Start-Process -FilePath $pythonExe -ArgumentList "-m streamlit run complete_app.py --server.port 8501 --server.headless false" -NoNewWindow -PassThru

Write-Host "`n" + "=" * 50 -ForegroundColor Cyan
Write-Host "✅ System started!" -ForegroundColor Green
Write-Host "🌐 Web Interface: http://localhost:8501" -ForegroundColor White
Write-Host "📖 API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "🩺 Health: http://localhost:8000/health" -ForegroundColor White
Write-Host "=" * 50 -ForegroundColor Cyan

Write-Host "`nPress Enter to exit..." -ForegroundColor Gray
Pause
