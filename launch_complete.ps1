# launch_complete.ps1 - FinRisk AI Agents 完整版启动脚本
$ErrorActionPreference = "Continue"

# 设置控制台标题
$host.ui.RawUI.WindowTitle = "FinRisk AI Agents - 完整版"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  FinRisk AI Agents - 完整金融风险分析系统" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# 检查文件是否存在
if (-not (Test-Path "complete_api.py")) {
    Write-Host "❌ 错误: 找不到 complete_api.py" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "complete_app.py")) {
    Write-Host "❌ 错误: 找不到 complete_app.py" -ForegroundColor Red
    exit 1
}

Write-Host "✅ 找到所有必要文件" -ForegroundColor Green

# 检查Python
Write-Host "`n[1/3] 检查Python环境..." -ForegroundColor Green
try {
    $pythonVersion = python --version
    Write-Host "✅ Python版本: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到Python，请先安装Python 3.8+" -ForegroundColor Red
    pause
    exit 1
}

# 检查依赖
Write-Host "`n[2/3] 检查依赖包..." -ForegroundColor Green
try {
    # 检查主要依赖是否已安装
    $checkDeps = @("fastapi", "streamlit", "pandas", "numpy", "plotly")
    foreach ($dep in $checkDeps) {
        try {
            python -c "import $dep" 2>$null
            Write-Host "  ✅ $dep" -ForegroundColor Green
        } catch {
            Write-Host "  ⚠️  $dep (需要安装)" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "⚠️  依赖检查跳过" -ForegroundColor Yellow
}

Write-Host "`n[3/3] 启动完整系统..." -ForegroundColor Green

# 启动API服务
Write-Host "`n🚀 启动API服务 (端口: 8000)..." -ForegroundColor Cyan
$apiJob = Start-Job -ScriptBlock {
    cd $using:PWD
    python complete_api.py
} -Name "FinRisk-API"

# 等待API启动
Write-Host "⏳ 等待API启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 检查API是否运行
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 3
    Write-Host "✅ API服务运行正常: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  API服务可能启动较慢，继续..." -ForegroundColor Yellow
}

# 启动Web界面
Write-Host "`n🌐 启动Web界面 (端口: 8501)..." -ForegroundColor Cyan
$webJob = Start-Job -ScriptBlock {
    cd $using:PWD
    streamlit run complete_app.py --server.port 8501 --server.headless false
} -Name "FinRisk-Web"

# 等待Web启动
Write-Host "⏳ 等待Web界面启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "✅ 系统启动完成！" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Web界面: http://localhost:8501" -ForegroundColor White
Write-Host "📖 API文档: http://localhost:8000/docs" -ForegroundColor White
Write-Host "🩺 健康检查: http://localhost:8000/health" -ForegroundColor White
Write-Host ""
Write-Host "🔧 进程信息:" -ForegroundColor Yellow
Get-Job | Format-Table Name, State -AutoSize
Write-Host ""
Write-Host "📊 服务状态测试..." -ForegroundColor Cyan

# 测试服务
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 5
    Write-Host "✅ API健康: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ API未响应" -ForegroundColor Red
}

try {
    $stocks = Invoke-RestMethod -Uri "http://localhost:8000/stocks" -TimeoutSec 5
    Write-Host "✅ 可用股票: $($stocks.count) 只" -ForegroundColor Green
} catch {
    Write-Host "❌ 无法获取股票列表" -ForegroundColor Red
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "系统正在运行中..." -ForegroundColor White
Write-Host "要停止系统，请在此窗口按 Ctrl+C" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan

# 保持脚本运行
try {
    while ($true) {
        Write-Host "`n按 Ctrl+C 停止系统..." -ForegroundColor Gray -NoNewline
        Start-Sleep -Seconds 10
    }
} finally {
    Write-Host "`n正在停止服务..." -ForegroundColor Yellow
    Get-Job | Stop-Job -PassThru | Remove-Job -Force
    Write-Host "✅ 服务已停止" -ForegroundColor Green
}
