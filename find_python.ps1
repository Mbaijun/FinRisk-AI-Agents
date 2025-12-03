$foundPython = $false

Write-Host "搜索Python..." -ForegroundColor Yellow

# 检查常见位置
$locations = @(
    "C:\Python311\python.exe",
    "C:\Python39\python.exe", 
    "C:\Python38\python.exe",
    "C:\Python37\python.exe",
    "$env:USERPROFILE\AppData\Local\Programs\Python\Python311\python.exe",
    "$env:USERPROFILE\AppData\Local\Programs\Python\Python39\python.exe",
    "$env:USERPROFILE\AppData\Local\Programs\Python\Python38\python.exe",
    "$env:USERPROFILE\AppData\Local\Programs\Python\Python37\python.exe",
    "$env:ProgramFiles\Python311\python.exe",
    "$env:ProgramFiles\Python39\python.exe"
)

foreach ($loc in $locations) {
    if (Test-Path $loc) {
        Write-Host "✓ 找到Python: $loc" -ForegroundColor Green
        & $loc --version
        $foundPython = $true
        break
    }
}

if (-not $foundPython) {
    Write-Host "✗ 未在常见位置找到Python" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先安装Python 3.8或更高版本:" -ForegroundColor Yellow
    Write-Host "下载地址: https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host "安装时务必勾选: 'Add Python to PATH'" -ForegroundColor Red
}

Read-Host "按回车继续"
