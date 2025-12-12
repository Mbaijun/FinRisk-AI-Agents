# 🚀 FinRisk-AI-Agents

**基于多智能体的金融风险分析与决策系统**

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)](https://fastapi.tiangolo.com)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-black)](https://vercel.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📌 项目概述

FinRisk-AI-Agents 是一个现代化的金融风险智能分析平台，通过多个专业 AI Agent 协作完成：
- 📊 **市场风险分析**（VaR、CVaR、压力测试）
- 🧠 **智能风险预警**（异常检测、模式识别）
- 🤖 **自动化报告生成**（PDF、HTML、Markdown）
- 🔄 **实时数据监控**（股票、债券、加密货币）
- 📈 **投资组合优化**（风险收益平衡）

## 🏗️ 系统架构
用户请求 → API网关 → 智能体协调器 → 专业Agent池 → 风险引擎 → 报告生成
↑ ↓ ↓ ↓ ↓ ↓
前端界面 数据缓存层 模型仓库 金融市场数据 可视化模块 推送服务

text

复制

下载

## 🚦 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/Mbaijun/FinRisk-AI-Agents.git
cd FinRisk-AI-Agents
2. 安装依赖
bash

复制

下载
pip install -r requirements.txt
3. 配置环境变量
创建 .env 文件：

env

复制

下载
OPENAI_API_KEY=sk-your-key-here
ALPHA_VANTAGE_KEY=your_alpha_vantage_key
DATABASE_URL=sqlite:///./risk_data.db
LOG_LEVEL=INFO
4. 启动系统
bash

复制

下载
# Windows (使用提供的脚本)
launch_ultimate.bat

# 或直接运行
python run.py

# 开发模式
uvicorn api.main:app --reload --port 8000
5. 访问服务
API 文档：http://localhost:8000/docs

监控面板：http://localhost:8000/dashboard

📁 项目结构
text

复制

下载
FinRisk-AI-Agents/
├── agents/              # AI智能体模块
│   ├── market_analyst.py    # 市场分析师
│   ├── risk_assessor.py     # 风险评估师
│   ├── portfolio_manager.py # 组合经理
│   └── orchestrator.py      # 智能体协调器
├── core/                 # 核心引擎
│   ├── system.py           # 主系统
│   ├── risk_engine.py      # 风险计算引擎
│   └── data_manager.py     # 数据管理器
├── api/                  # FastAPI接口
│   ├── endpoints.py        # API端点
│   ├── schemas.py          # 数据模型
│   └── main.py            # API主入口
├── models/               # 风险模型
│   ├── var_model.py        # VaR模型
│   ├── stress_test.py      # 压力测试
│   └── scenario_analysis.py # 情景分析
├── data/                 # 数据层
│   ├── fetchers/           # 数据获取器
│   ├── processors/         # 数据处理器
│   └── cache/              # 缓存数据
├── utils/                # 工具函数
│   ├── logger.py           # 日志配置
│   ├── validator.py        # 数据验证
│   └── formatter.py        # 格式转换
├── tests/                # 测试套件
├── docs/                 # 文档
├── launch_hybrid.bat     # 混合部署脚本
├── launch_ultimate.bat   # 完整部署脚本
├── requirements.txt      # Python依赖
├── run.py               # 主程序入口
├── vercel.json          # Vercel部署配置
└── README.md            # 本文件
🌐 Vercel 部署
一键部署
https://vercel.com/button

手动部署步骤
将项目推送到 GitHub

在 Vercel 导入项目

配置环境变量（同 .env）

部署分支（通常为 main）

访问生成的域名即可使用

🔧 API 使用示例
python

复制

下载
import requests

# 1. 获取股票风险指标
response = requests.post(
    "https://your-vercel-app.vercel.app/api/risk/analyze",
    json={
        "symbol": "AAPL",
        "period": "1y",
        "metrics": ["var", "cvar", "volatility"]
    }
)

# 2. 运行压力测试
response = requests.post(
    "https://your-vercel-app.vercel.app/api/stress-test",
    json={
        "portfolio": ["AAPL", "GOOGL", "TSLA"],
        "scenario": "market_crash_2020",
        "confidence_level": 0.99
    }
)
📊 智能体功能说明
智能体	职责	核心技术
Market Analyst	市场趋势分析、异常检测	LSTM、Prophet、统计模型
Risk Assessor	风险指标计算、预警	VaR、CVaR、Monte Carlo
Portfolio Manager	组合优化、再平衡	Markowitz、Black-Litterman
Report Generator	自动化报告生成	Jinja2、Plotly、PDFKit
🧪 测试
运行完整测试套件：

bash

复制

下载
# 单元测试
pytest tests/unit/

# 集成测试
pytest tests/integration/

# 系统测试
python test_system.py
🤝 贡献指南
Fork 项目

创建功能分支 (git checkout -b feature/AmazingFeature)

提交更改 (git commit -m 'Add AmazingFeature')

推送到分支 (git push origin feature/AmazingFeature)

开启 Pull Request

📄 许可证
本项目基于 MIT 许可证 - 查看 LICENSE 文件了解详情。

📞 支持与联系
📧 邮箱：项目维护者邮箱

🐛 问题反馈

💬 讨论区：GitHub Discussions

🚧 开发状态
当前版本: v0.1.0 (Alpha)
最后更新: 2024年1月
下一个里程碑: v0.2.0 - 增加实时交易风险监控

⚠️ 注意: 项目处于活跃开发阶段，API 可能发生变化。