<#
.DESCRIPTION
FinRisk AI Agents Vercel部署脚本
#>
param(
    [string]$Environment = "preview"
)

Write-Host "FinRisk AI Agents 部署脚本" -ForegroundColor Cyan
Write-Host "环境: $Environment" -ForegroundColor Yellow

# 运行快速测试
Write-Host "`n运行快速测试..." -ForegroundColor Green
python -c "
import sys
try:
    import gradio, fastapi, pandas, numpy
    print('✅ 核心依赖检查通过')
    
    # 测试主应用导入
    sys.path.insert(0, '.')
    from src.app import create_enhanced_interface
    print('✅ 应用导入成功')
    
    print('🎉 所有测试通过！')
except Exception as e:
    print(f'❌ 测试失败: {e}')
    sys.exit(1)
"

if ($LASTEXITCODE -ne 0) {
    Write-Host "测试失败，请先解决依赖问题" -ForegroundColor Red
    exit 1
}

# 检查文件
Write-Host "`n检查部署文件..." -ForegroundColor Green
$requiredFiles = @("vercel.json", "requirements.txt", "api/index.py", "src/app.py")
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file (缺失)" -ForegroundColor Red
        exit 1
    }
}

# 部署到Vercel
Write-Host "`n开始部署到Vercel..." -ForegroundColor Cyan

if (Get-Command vercel -ErrorAction SilentlyContinue) {
    if ($Environment -eq "prod") {
        Write-Host "部署到生产环境..." -ForegroundColor Yellow
        vercel --prod
    } else {
        Write-Host "部署到预览环境..." -ForegroundColor Yellow
        vercel
    }
} else {
    Write-Host "Vercel CLI未安装" -ForegroundColor Red
    Write-Host "请先安装: npm install -g vercel" -ForegroundColor Yellow
    Write-Host "然后运行: vercel login" -ForegroundColor Yellow
    Write-Host "最后运行: vercel --prod" -ForegroundColor Yellow
}
