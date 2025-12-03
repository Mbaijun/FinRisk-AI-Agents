# run_finrisk_fixed.ps1
$ErrorActionPreference = "Continue"

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "FinRisk AI Agents - Fixed Startup Script" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Cyan

# 1. 首先清理可能的冲突进程
Write-Host "`n[1/4] 清理现有进程..." -ForegroundColor Cyan
Get-Process python* -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host "停止进程: $($_.Name) PID: $($_.Id)" -ForegroundColor Gray
    Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
}
Start-Sleep -Seconds 2

# 2. 检查端口占用并释放
Write-Host "`n[2/4] 检查端口占用..." -ForegroundColor Cyan

$ports = @(8000, 8501)
foreach ($port in $ports) {
    $netstat = netstat -ano | findstr ":$port " | findstr "LISTENING"
    if ($netstat) {
        $pidMatch = $netstat -match '\s+(\d+)$'
        if ($pidMatch) {
            $pid = $matches[1]
            Write-Host "端口 $port 被进程 $pid 占用，正在停止..." -ForegroundColor Yellow
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 1
        }
    }
}

# 3. 设置Python路径
$pythonExe = "C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe"
if (-not (Test-Path $pythonExe)) {
    Write-Host "错误: Python 未找到: $pythonExe" -ForegroundColor Red
    exit 1
}

Write-Host "`n[3/4] 使用 Python: $pythonExe" -ForegroundColor Green
& $pythonExe --version

# 检查必要文件
$requiredFiles = @("complete_api.py", "complete_app.py")
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "错误: 缺少文件 $file" -ForegroundColor Red
        exit 1
    }
}

# 4. 先启动API服务（在前台运行以便查看错误）
Write-Host "`n[4/4] 启动 API 服务..." -ForegroundColor Green
$apiProcess = Start-Process -FilePath $pythonExe `
    -ArgumentList "complete_api.py" `
    -NoNewWindow `
    -PassThru `
    -RedirectStandardOutput "api_output.log" `
    -RedirectStandardError "api_error.log"

Write-Host "API 进程已启动，PID: $($apiProcess.Id)" -ForegroundColor Gray

# 等待API初始化
Write-Host "等待 API 初始化 (10秒)..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

# 测试API
Write-Host "`n测试 API 连接..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 10
    Write-Host "✅ API 状态: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ API 连接失败: $_" -ForegroundColor Red
    Write-Host "检查日志文件: api_output.log 和 api_error.log" -ForegroundColor Yellow
    Write-Host "API 可能需要手动启动..." -ForegroundColor Yellow
}

# 5. 启动Web界面
Write-Host "`n启动 Web 界面..." -ForegroundColor Green
$webProcess = Start-Process -FilePath $pythonExe `
    -ArgumentList "-m streamlit run complete_app.py --server.port 8501 --server.headless true" `
    -NoNewWindow `
    -PassThru

Write-Host "Web 进程已启动，PID: $($webProcess.Id)" -ForegroundColor Gray
Start-Sleep -Seconds 3

# 显示信息
Write-Host "`n" + "=" * 60 -ForegroundColor Cyan
Write-Host "✅ FinRisk 系统启动完成！" -ForegroundColor Green
Write-Host "📊 Web 界面: http://localhost:8501" -ForegroundColor White
Write-Host "📖 API 文档: http://localhost:8000/docs" -ForegroundColor White
Write-Host "🩺 健康检查: http://localhost:8000/health" -ForegroundColor White
Write-Host "📁 日志文件: api_output.log, api_error.log" -ForegroundColor Gray
Write-Host "=" * 60 -ForegroundColor Cyan

Write-Host "`n重要: 不要关闭此窗口！" -ForegroundColor Yellow
Write-Host "按 Ctrl+C 停止所有服务" -ForegroundColor Yellow

# 保持窗口打开
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host "`n正在停止服务..." -ForegroundColor Yellow
    Get-Process python* -ErrorAction SilentlyContinue | Stop-Process -Force
}
