# start_finrisk_final.ps1
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    FinRisk AI Agents - Final Version" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Stop existing processes
Write-Host "[1] Stopping existing processes..." -ForegroundColor Green
Get-Process python* -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 3

# Set Python path
$pythonPath = "C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe"
if (-not (Test-Path $pythonPath)) {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    exit 1
}

Write-Host "[2] Starting API service..." -ForegroundColor Green
$apiProcess = Start-Process -FilePath $pythonPath `
    -ArgumentList "simple_working_api.py" `
    -NoNewWindow `
    -PassThru

Write-Host "   API Process ID: $($apiProcess.Id)" -ForegroundColor Gray
Start-Sleep -Seconds 10

# Test API
Write-Host "[3] Testing API..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 5
    Write-Host "   ✅ API Status: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ API connection failed" -ForegroundColor Red
    exit 1
}

Write-Host "[4] Starting Web interface..." -ForegroundColor Green
$webProcess = Start-Process -FilePath $pythonPath `
    -ArgumentList "-m streamlit run web_app_final_fixed.py --server.port 8501 --server.headless true" `
    -NoNewWindow `
    -PassThru

Write-Host "   Web Process ID: $($webProcess.Id)" -ForegroundColor Gray
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    🎉 SYSTEM READY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Web Interface: http://localhost:8501" -ForegroundColor White
Write-Host "📖 API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "🩺 Health Check: http://localhost:8000/health" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Features:" -ForegroundColor Cyan
Write-Host "   • Dashboard - Market overview" -ForegroundColor Gray
Write-Host "   • Single Stock Analysis - Detailed risk metrics" -ForegroundColor Gray
Write-Host "   • Portfolio Analysis - Multi-stock optimization" -ForegroundColor Gray
Write-Host "   • Data Reports - Generation and export (in sidebar)" -ForegroundColor Gray
Write-Host ""
Write-Host "📈 Available Stocks (12):" -ForegroundColor Cyan
Write-Host "   AAPL, MSFT, GOOGL, AMZN, TSLA, JPM, JNJ, WMT, NVDA, XOM, BRK.B, V" -ForegroundColor Gray
Write-Host ""

# Open browser
Write-Host "Opening browser..." -ForegroundColor Yellow
Start-Process "http://localhost:8501"

Write-Host ""
Write-Host "⚠️  IMPORTANT: Keep this window open!" -ForegroundColor Yellow
Write-Host "    Press Ctrl+C to stop all services" -ForegroundColor Yellow

# Keep running
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host ""
    Write-Host "Stopping services..." -ForegroundColor Yellow
    Get-Process python* -ErrorAction SilentlyContinue | Stop-Process -Force
}
