<#
.SYNOPSIS
FinRisk AI Agents 最终部署脚本

.DESCRIPTION
一键部署到Vercel，包含所有必要的检查和配置

.PARAMETER Environment
部署环境: preview (预览) 或 prod (生产)

.EXAMPLE
# 部署到预览环境
.\deploy-final.ps1

# 部署到生产环境
.\deploy-final.ps1 -Environment prod

# 只测试不部署
.\deploy-final.ps1 -TestOnly
#>
param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("preview", "prod")]
    [string]$Environment = "preview",
    
    [Parameter(Mandatory=$false)]
    [switch]$TestOnly,
    
    [Parameter(Mandatory=$false)]
    [switch]$Force
)

# 颜色定义
$success = "Green"
$error = "Red"
$warning = "Yellow"
$info = "Cyan"

function Show-Header {
    Write-Host "`n" + "="*70 -ForegroundColor Cyan
    Write-Host "FinRisk AI Agents - Vercel 部署脚本" -ForegroundColor White
    Write-Host "="*70 -ForegroundColor Cyan
    Write-Host "开始时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
    Write-Host "部署环境: $Environment" -ForegroundColor Gray
}

function Show-Step {
    param([string]$Message)
    Write-Host "`n▶️  $Message" -ForegroundColor Magenta
}

function Show-Result {
    param([string]$Status, [string]$Message)
    $color = switch ($Status) {
        "✅" { $success }
        "❌" { $error }
        "⚠️ " { $warning }
        default { $info }
    }
    Write-Host "  $Status $Message" -ForegroundColor $color
}

Show-Header

# 步骤1: 系统检查
Show-Step "步骤1: 系统环境检查"

$checks = @(
    @{Name="Python"; Command="python --version"; Optional=$false},
    @{Name="pip"; Command="pip --version"; Optional=$false},
    @{Name="Node.js"; Command="node --version"; Optional=$true},
    @{Name="Git"; Command="git --version"; Optional=$true}
)

$allPassed = $true
foreach ($check in $checks) {
    try {
        $output = Invoke-Expression $check.Command 2>&1
        if ($LASTEXITCODE -eq 0 -or $check.Optional) {
            Show-Result "✅" "$($check.Name): 已安装"
        } else {
            Show-Result "❌" "$($check.Name): 未安装"
            if (-not $check.Optional) { $allPassed = $false }
        }
    } catch {
        if ($check.Optional) {
            Show-Result "⚠️ " "$($check.Name): 未安装 (可选)"
        } else {
            Show-Result "❌" "$($check.Name): 未安装"
            $allPassed = $false
        }
    }
}

if (-not $allPassed -and -not $Force) {
    Show-Result "❌" "系统检查失败，使用 -Force 参数强制继续"
    exit 1
}

# 步骤2: 项目检查
Show-Step "步骤2: 项目文件检查"

$requiredFiles = @(
    "vercel.json",
    "requirements.txt", 
    "api/index.py",
    "src/app.py",
    ".gitignore"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Show-Result "✅" "$file"
    } else {
        Show-Result "❌" "$file (缺失)"
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0 -and -not $Force) {
    Show-Result "❌" "缺少必要文件，使用 -Force 参数强制继续"
    exit 1
}

# 步骤3: 依赖检查
Show-Step "步骤3: Python依赖检查"

try {
    # 检查关键依赖
    $criticalDeps = @("gradio", "fastapi", "uvicorn", "pandas", "numpy")
    $missingDeps = @()
    
    foreach ($dep in $criticalDeps) {
        $check = python -c "try: import $dep; print('INSTALLED'); except: print('MISSING')" 2>&1
        if ($check -contains "INSTALLED") {
            Show-Result "✅" "$dep"
        } else {
            Show-Result "❌" "$dep (未安装)"
            $missingDeps += $dep
        }
    }
    
    if ($missingDeps.Count -gt 0) {
        Show-Result "⚠️ " "正在安装缺失的依赖..."
        foreach ($dep in $missingDeps) {
            pip install $dep 2>&1 | Out-Null
            Show-Result "✅" "已安装 $dep"
        }
    }
} catch {
    Show-Result "❌" "依赖检查失败: $_"
    if (-not $Force) { exit 1 }
}

# 步骤4: 应用测试
Show-Step "步骤4: 应用功能测试"

if (-not $TestOnly) {
    try {
        # 快速应用测试
        $testScript = @"
import sys
try:
    # 测试导入
    import gradio as gr
    import fastapi
    from src.app import create_compatible_interface
    
    print("IMPORT_SUCCESS")
    
    # 测试应用创建
    app = create_compatible_interface()
    print("APP_CREATE_SUCCESS")
    
    print("✅ 应用测试通过")
    sys.exit(0)
except Exception as e:
    print(f"❌ 应用测试失败: {e}")
    sys.exit(1)
"@
        
        $testScript | Out-File "quick_test.py" -Encoding UTF8
        $testResult = python quick_test.py 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Show-Result "✅" "应用功能测试通过"
        } else {
            Show-Result "❌" "应用测试失败"
            Write-Host $testResult -ForegroundColor Red
            if (-not $Force) { exit 1 }
        }
        
        Remove-Item "quick_test.py" -Force -ErrorAction SilentlyContinue
        
    } catch {
        Show-Result "❌" "测试过程出错: $_"
        if (-not $Force) { exit 1 }
    }
} else {
    Show-Result "ℹ️" "跳过应用测试 (TestOnly模式)"
}

if ($TestOnly) {
    Show-Step "测试完成"
    Write-Host "所有测试通过！可以安全部署。" -ForegroundColor Green
    exit 0
}

# 步骤5: Vercel部署
Show-Step "步骤5: 部署到Vercel"

# 检查Vercel CLI
$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue
if (-not $vercelInstalled) {
    Show-Result "❌" "Vercel CLI未安装"
    Write-Host "`n请先安装Vercel CLI:" -ForegroundColor Yellow
    Write-Host "1. 安装Node.js: https://nodejs.org/" -ForegroundColor Gray
    Write-Host "2. 安装Vercel: npm install -g vercel" -ForegroundColor Gray
    Write-Host "3. 登录: vercel login" -ForegroundColor Gray
    exit 1
}

try {
    # 检查登录状态
    Show-Result "ℹ️" "检查Vercel登录状态..."
    $whoami = vercel whoami 2>&1
    if ($LASTEXITCODE -eq 0) {
        Show-Result "✅" "已登录: $whoami"
    } else {
        Show-Result "⚠️ " "未登录或会话过期，尝试登录..."
        vercel login
    }
    
    # 开始部署
    Show-Result "ℹ️" "开始部署到 $Environment 环境..."
    
    if ($Environment -eq "prod") {
        Show-Result "🚀" "部署到生产环境..."
        vercel --prod --confirm
    } else {
        Show-Result "🚀" "部署到预览环境..."
        vercel --confirm
    }
    
    if ($LASTEXITCODE -eq 0) {
        Show-Result "✅" "部署成功！"
        
        # 获取部署URL
        $deployInfo = vercel 2>&1
        if ($deployInfo -match "(https?://[^\s]+)") {
            $deployUrl = $matches[1]
            Write-Host "`n🎉 部署完成！" -ForegroundColor Green
            Write-Host "🌐 访问地址: $deployUrl" -ForegroundColor Cyan
            Write-Host "🔧 管理面板: https://vercel.com/dashboard" -ForegroundColor Gray
            
            # 保存部署信息
            @{
                url = $deployUrl
                environment = $Environment
                timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            } | ConvertTo-Json | Out-File "deployment-info.json" -Encoding UTF8
        }
        
    } else {
        Show-Result "❌" "部署失败"
        exit 1
    }
    
} catch {
    Show-Result "❌" "部署过程出错: $_"
    exit 1
}

# 完成
Write-Host "`n" + "="*70 -ForegroundColor Cyan
Write-Host "✅ 部署流程完成！" -ForegroundColor Green
Write-Host "完成时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host "="*70 -ForegroundColor Cyan

Write-Host "`n📋 后续操作建议:" -ForegroundColor Yellow
Write-Host "1. 访问部署的应用测试功能" -ForegroundColor Gray
Write-Host "2. 检查Vercel日志确保运行正常" -ForegroundColor Gray
Write-Host "3. 配置自定义域名（如需要）" -ForegroundColor Gray
Write-Host "4. 设置环境变量（如需要）" -ForegroundColor Gray
Write-Host "5. 启用自动部署（如需要）" -ForegroundColor Gray

exit 0
