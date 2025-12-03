Write-Host "清理FinRisk系统..." -ForegroundColor Green
Write-Host "=" * 50

# 停止进程
Write-Host "停止相关进程..." -ForegroundColor Yellow
$processes = @("python", "python.exe", "streamlit", "streamlit.exe", "uvicorn")
foreach ($proc in $processes) {
    try {
        Get-Process $proc -ErrorAction SilentlyContinue | Stop-Process -Force
        Write-Host "  停止: $proc" -ForegroundColor Cyan
    } catch {
        # 忽略错误
    }
}

Start-Sleep -Seconds 2

# 检查端口
Write-Host "`n检查端口状态..." -ForegroundColor Yellow
$ports = @(8501, 8000, 8502)
foreach ($port in $ports) {
    $connections = netstat -ano | findstr ":$port"
    if ($connections) {
        Write-Host "  ❌ 端口 $port 被占用:" -ForegroundColor Red
        $connections
    } else {
        Write-Host "  ✅ 端口 $port 可用" -ForegroundColor Green
    }
}

Write-Host "`n清理完成！" -ForegroundColor Green
