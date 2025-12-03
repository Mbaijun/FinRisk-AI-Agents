# 修复complete_api.py
$content = Get-Content complete_api.py -Raw

# 确保有正确的启动代码
if ($content -notmatch "if __name__ == .__main__.:") {
    Write-Host "添加if __name__ == '__main__':块" -ForegroundColor Yellow
    $content = $content + "`n`nif __name__ == '__main__':`n    print('Starting FinRisk API v2.0...')`n    print('Available stocks: AAPL, MSFT, GOOGL, AMZN, TSLA, JPM, JNJ, WMT, NVDA, XOM, BRK.B, V')`n    print('API Documentation: http://localhost:8000/docs')`n    print('Health Check: http://localhost:8000/health')`n    print('=' * 50)`n    uvicorn.run(app, host='0.0.0.0', port=8000, reload=False)`n"
} elseif ($content -match "uvicorn\.run\(.*reload=True.*\)") {
    Write-Host "修复reload参数" -ForegroundColor Yellow
    $content = $content -replace "reload=True", "reload=False"
}

# 保存修复后的文件
$content | Out-File complete_api_fixed.py -Encoding UTF8
Write-Host "✅ 已创建修复文件: complete_api_fixed.py" -ForegroundColor Green

# 显示修复后的结尾
Write-Host "`n修复后的文件结尾:" -ForegroundColor Cyan
Get-Content complete_api_fixed.py -Tail 10
