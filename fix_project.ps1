# fix_project.ps1 - 修复PowerShell执行问题
Write-Host "修复FinRisk-AI-Agents项目" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Cyan

# 检查当前目录
Write-Host "当前目录: $PWD" -ForegroundColor Yellow

# 检查requirements.txt是否存在
if (Test-Path "requirements.txt") {
    Write-Host "找到requirements.txt文件" -ForegroundColor Green
    
    # 安装依赖
    Write-Host "正在安装依赖..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "依赖安装成功！" -ForegroundColor Green
    } else {
        Write-Host "依赖安装失败，尝试逐个安装..." -ForegroundColor Yellow
        python -m pip install fastapi uvicorn streamlit pandas numpy plotly requests
    }
} else {
    Write-Host "未找到requirements.txt，创建中..." -ForegroundColor Yellow
    
    # 创建requirements.txt
    @"
fastapi==0.104.1
uvicorn==0.24.0
streamlit==1.28.1
pandas==2.1.3
numpy==1.24.4
plotly==5.18.0
requests==2.31.0
"@ | Out-File -FilePath requirements.txt
    
    Write-Host "已创建requirements.txt" -ForegroundColor Green
    Write-Host "正在安装依赖..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt
}

# 测试安装
Write-Host "`n测试安装..." -ForegroundColor Yellow
python -c "
try:
    import fastapi, streamlit, pandas, numpy
    print('✓ 核心库安装成功')
except ImportError as e:
    print(f'✗ 导入失败: {e}')
"

Write-Host "`n修复完成！" -ForegroundColor Green
Write-Host "运行以下命令启动：" -ForegroundColor Cyan
Write-Host "1. .\start_final.bat" -ForegroundColor Cyan
Write-Host "2. 或手动启动: python -m uvicorn finrisk_ai.api:app" -ForegroundColor Cyan