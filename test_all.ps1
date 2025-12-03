# test_all.ps1
Write-Host "FinRisk-AI-Agents 完整测试" -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor Cyan
Write-Host ""

# 1. 测试Python
Write-Host "1. 测试Python..." -ForegroundColor Yellow
$pythonVersion = python --version
if ($LASTEXITCODE -eq 0) {
    Write-Host "   $pythonVersion" -ForegroundColor Green
    Write-Host "   √ Python正常" -ForegroundColor Green
} else {
    Write-Host "   ✗ Python未安装或配置错误" -ForegroundColor Red
    exit 1
}

Write-Host ""

# 2. 测试依赖
Write-Host "2. 测试依赖..." -ForegroundColor Yellow
try {
    python -c "
import sys
try:
    import fastapi, uvicorn, streamlit, pandas, numpy, plotly, scipy, requests
    print('   所有依赖导入成功')
except ImportError as e:
    print(f'   缺少依赖: {e}')
    sys.exit(1)
"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   √ 依赖检查通过" -ForegroundColor Green
    } else {
        Write-Host "   ✗ 依赖检查失败" -ForegroundColor Red
    }
} catch {
    Write-Host "   ✗ 依赖测试出错" -ForegroundColor Red
}

Write-Host ""

# 3. 测试风险分析器
Write-Host "3. 测试风险分析器..." -ForegroundColor Yellow
try {
    python -c "
import sys
sys.path.append('.')
try:
    from finrisk_ai.risk_analyzer import RiskAnalyzer
    analyzer = RiskAnalyzer()
    print('   风险分析器初始化成功')
    
    # 测试分析
    result = analyzer.analyze_portfolio(['AAPL', 'MSFT', 'GOOGL'])
    if result.get('success'):
        print(f'   分析成功: 波动率={result[\"volatility\"]:.2%}, Sharpe={result[\"sharpe_ratio\"]:.2f}')
    else:
        print(f'   分析失败: {result.get(\"error\", \"未知错误\")}')
        sys.exit(1)
        
except Exception as e:
    print(f'   测试失败: {str(e)}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   √ 风险分析器测试通过" -ForegroundColor Green
    } else {
        Write-Host "   ✗ 风险分析器测试失败" -ForegroundColor Red
    }
} catch {
    Write-Host "   ✗ 风险分析器测试出错" -ForegroundColor Red
}

Write-Host ""

# 4. 创建快速启动脚本
Write-Host "4. 创建启动脚本..." -ForegroundColor Yellow
try {
    # 检查启动脚本
    if (Test-Path "start_final.bat") {
        Write-Host "   √ 启动脚本已存在" -ForegroundColor Green
    } else {
        Write-Host "   ! 启动脚本不存在，请重新创建" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ✗ 检查启动脚本出错" -ForegroundColor Red
}

Write-Host ""

# 5. 显示配置信息
Write-Host "5. 配置信息..." -ForegroundColor Yellow
$pythonPath = where.exe python 2>$null
if ($pythonPath) {
    Write-Host "   Python路径: $pythonPath" -ForegroundColor Cyan
}

Write-Host "   API端口: 8000" -ForegroundColor Cyan
Write-Host "   Web端口: 8501" -ForegroundColor Cyan
Write-Host "   运行模式: 离线模拟" -ForegroundColor Cyan

Write-Host ""
Write-Host ("=" * 50) -ForegroundColor Cyan
Write-Host "测试完成！" -ForegroundColor Green
Write-Host ""

Write-Host "下一步：" -ForegroundColor Yellow
Write-Host "1. 双击运行 start_final.bat 启动服务" -ForegroundColor Cyan
Write-Host "2. 访问 http://localhost:8501 使用Web界面" -ForegroundColor Cyan
Write-Host "3. 访问 http://localhost:8000/docs 查看API文档" -ForegroundColor Cyan
Write-Host ""

$null = Read-Host "按回车键退出"
