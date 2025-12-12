# 馃殌 FinRisk-AI-Agents

**鍩轰簬澶氭櫤鑳戒綋鐨勯噾铻嶉闄╁垎鏋愪笌鍐崇瓥绯荤粺**

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)](https://fastapi.tiangolo.com)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-black)](https://vercel.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 馃搶 椤圭洰姒傝堪

FinRisk-AI-Agents 鏄竴涓幇浠ｅ寲鐨勯噾铻嶉闄╂櫤鑳藉垎鏋愬钩鍙帮紝閫氳繃澶氫釜涓撲笟 AI Agent 鍗忎綔瀹屾垚锛?
- 馃搳 **甯傚満椋庨櫓鍒嗘瀽**锛圴aR銆丆VaR銆佸帇鍔涙祴璇曪級
- 馃 **鏅鸿兘椋庨櫓棰勮**锛堝紓甯告娴嬨€佹ā寮忚瘑鍒級
- 馃 **鑷姩鍖栨姤鍛婄敓鎴?*锛圥DF銆丠TML銆丮arkdown锛?
- 馃攧 **瀹炴椂鏁版嵁鐩戞帶**锛堣偂绁ㄣ€佸€哄埜銆佸姞瀵嗚揣甯侊級
- 馃搱 **鎶曡祫缁勫悎浼樺寲**锛堥闄╂敹鐩婂钩琛★級

## 馃彈锔?绯荤粺鏋舵瀯
鐢ㄦ埛璇锋眰 鈫?API缃戝叧 鈫?鏅鸿兘浣撳崗璋冨櫒 鈫?涓撲笟Agent姹?鈫?椋庨櫓寮曟搸 鈫?鎶ュ憡鐢熸垚
鈫?鈫?鈫?鈫?鈫?鈫?
鍓嶇鐣岄潰 鏁版嵁缂撳瓨灞?妯″瀷浠撳簱 閲戣瀺甯傚満鏁版嵁 鍙鍖栨ā鍧?鎺ㄩ€佹湇鍔?

text

澶嶅埗

涓嬭浇

## 馃殾 蹇€熷紑濮?

### 1. 鍏嬮殕椤圭洰
```bash
git clone https://github.com/Mbaijun/FinRisk-AI-Agents.git
cd FinRisk-AI-Agents
2. 瀹夎渚濊禆
bash

澶嶅埗

涓嬭浇
pip install -r requirements.txt
3. 閰嶇疆鐜鍙橀噺
鍒涘缓 .env 鏂囦欢锛?

env

澶嶅埗

涓嬭浇
OPENAI_API_KEY=sk-your-key-here
ALPHA_VANTAGE_KEY=your_alpha_vantage_key
DATABASE_URL=sqlite:///./risk_data.db
LOG_LEVEL=INFO
4. 鍚姩绯荤粺
bash

澶嶅埗

涓嬭浇
# Windows (浣跨敤鎻愪緵鐨勮剼鏈?
launch_ultimate.bat

# 鎴栫洿鎺ヨ繍琛?
python run.py

# 寮€鍙戞ā寮?
uvicorn api.main:app --reload --port 8000
5. 璁块棶鏈嶅姟
API 鏂囨。锛歨ttp://localhost:8000/docs

鐩戞帶闈㈡澘锛歨ttp://localhost:8000/dashboard

馃搧 椤圭洰缁撴瀯
text

澶嶅埗

涓嬭浇
FinRisk-AI-Agents/
鈹溾攢鈹€ agents/              # AI鏅鸿兘浣撴ā鍧?
鈹?  鈹溾攢鈹€ market_analyst.py    # 甯傚満鍒嗘瀽甯?
鈹?  鈹溾攢鈹€ risk_assessor.py     # 椋庨櫓璇勪及甯?
鈹?  鈹溾攢鈹€ portfolio_manager.py # 缁勫悎缁忕悊
鈹?  鈹斺攢鈹€ orchestrator.py      # 鏅鸿兘浣撳崗璋冨櫒
鈹溾攢鈹€ core/                 # 鏍稿績寮曟搸
鈹?  鈹溾攢鈹€ system.py           # 涓荤郴缁?
鈹?  鈹溾攢鈹€ risk_engine.py      # 椋庨櫓璁＄畻寮曟搸
鈹?  鈹斺攢鈹€ data_manager.py     # 鏁版嵁绠＄悊鍣?
鈹溾攢鈹€ api/                  # FastAPI鎺ュ彛
鈹?  鈹溾攢鈹€ endpoints.py        # API绔偣
鈹?  鈹溾攢鈹€ schemas.py          # 鏁版嵁妯″瀷
鈹?  鈹斺攢鈹€ main.py            # API涓诲叆鍙?
鈹溾攢鈹€ models/               # 椋庨櫓妯″瀷
鈹?  鈹溾攢鈹€ var_model.py        # VaR妯″瀷
鈹?  鈹溾攢鈹€ stress_test.py      # 鍘嬪姏娴嬭瘯
鈹?  鈹斺攢鈹€ scenario_analysis.py # 鎯呮櫙鍒嗘瀽
鈹溾攢鈹€ data/                 # 鏁版嵁灞?
鈹?  鈹溾攢鈹€ fetchers/           # 鏁版嵁鑾峰彇鍣?
鈹?  鈹溾攢鈹€ processors/         # 鏁版嵁澶勭悊鍣?
鈹?  鈹斺攢鈹€ cache/              # 缂撳瓨鏁版嵁
鈹溾攢鈹€ utils/                # 宸ュ叿鍑芥暟
鈹?  鈹溾攢鈹€ logger.py           # 鏃ュ織閰嶇疆
鈹?  鈹溾攢鈹€ validator.py        # 鏁版嵁楠岃瘉
鈹?  鈹斺攢鈹€ formatter.py        # 鏍煎紡杞崲
鈹溾攢鈹€ tests/                # 娴嬭瘯濂椾欢
鈹溾攢鈹€ docs/                 # 鏂囨。
鈹溾攢鈹€ launch_hybrid.bat     # 娣峰悎閮ㄧ讲鑴氭湰
鈹溾攢鈹€ launch_ultimate.bat   # 瀹屾暣閮ㄧ讲鑴氭湰
鈹溾攢鈹€ requirements.txt      # Python渚濊禆
鈹溾攢鈹€ run.py               # 涓荤▼搴忓叆鍙?
鈹溾攢鈹€ vercel.json          # Vercel閮ㄧ讲閰嶇疆
鈹斺攢鈹€ README.md            # 鏈枃浠?
馃寪 Vercel 閮ㄧ讲
涓€閿儴缃?
https://vercel.com/button

鎵嬪姩閮ㄧ讲姝ラ
灏嗛」鐩帹閫佸埌 GitHub

鍦?Vercel 瀵煎叆椤圭洰

閰嶇疆鐜鍙橀噺锛堝悓 .env锛?

閮ㄧ讲鍒嗘敮锛堥€氬父涓?main锛?

璁块棶鐢熸垚鐨勫煙鍚嶅嵆鍙娇鐢?

馃敡 API 浣跨敤绀轰緥
python

澶嶅埗

涓嬭浇
import requests

# 1. 鑾峰彇鑲＄エ椋庨櫓鎸囨爣
response = requests.post(
    "https://your-vercel-app.vercel.app/api/risk/analyze",
    json={
        "symbol": "AAPL",
        "period": "1y",
        "metrics": ["var", "cvar", "volatility"]
    }
)

# 2. 杩愯鍘嬪姏娴嬭瘯
response = requests.post(
    "https://your-vercel-app.vercel.app/api/stress-test",
    json={
        "portfolio": ["AAPL", "GOOGL", "TSLA"],
        "scenario": "market_crash_2020",
        "confidence_level": 0.99
    }
)
馃搳 鏅鸿兘浣撳姛鑳借鏄?
鏅鸿兘浣?鑱岃矗	鏍稿績鎶€鏈?
Market Analyst	甯傚満瓒嬪娍鍒嗘瀽銆佸紓甯告娴?LSTM銆丳rophet銆佺粺璁℃ā鍨?
Risk Assessor	椋庨櫓鎸囨爣璁＄畻銆侀璀?VaR銆丆VaR銆丮onte Carlo
Portfolio Manager	缁勫悎浼樺寲銆佸啀骞宠　	Markowitz銆丅lack-Litterman
Report Generator	鑷姩鍖栨姤鍛婄敓鎴?Jinja2銆丳lotly銆丳DFKit
馃И 娴嬭瘯
杩愯瀹屾暣娴嬭瘯濂椾欢锛?

bash

澶嶅埗

涓嬭浇
# 鍗曞厓娴嬭瘯
pytest tests/unit/

# 闆嗘垚娴嬭瘯
pytest tests/integration/

# 绯荤粺娴嬭瘯
python test_system.py
馃 璐＄尞鎸囧崡
Fork 椤圭洰

鍒涘缓鍔熻兘鍒嗘敮 (git checkout -b feature/AmazingFeature)

鎻愪氦鏇存敼 (git commit -m 'Add AmazingFeature')

鎺ㄩ€佸埌鍒嗘敮 (git push origin feature/AmazingFeature)

寮€鍚?Pull Request

馃搫 璁稿彲璇?
鏈」鐩熀浜?MIT 璁稿彲璇?- 鏌ョ湅 LICENSE 鏂囦欢浜嗚В璇︽儏銆?

馃摓 鏀寔涓庤仈绯?
馃摟 閭锛氶」鐩淮鎶よ€呴偖绠?

馃悰 闂鍙嶉

馃挰 璁ㄨ鍖猴細GitHub Discussions

馃毀 寮€鍙戠姸鎬?
褰撳墠鐗堟湰: v0.1.0 (Alpha)
鏈€鍚庢洿鏂? 2024骞?鏈?
涓嬩竴涓噷绋嬬: v0.2.0 - 澧炲姞瀹炴椂浜ゆ槗椋庨櫓鐩戞帶

鈿狅笍 娉ㄦ剰: 椤圭洰澶勪簬娲昏穬寮€鍙戦樁娈碉紝API 鍙兘鍙戠敓鍙樺寲銆
