import streamlit as st
from streamlit.web import cli as stcli
import sys

# 如果是直接运行，设置Streamlit配置
if __name__ == "__main__":
    sys.argv = [
        "streamlit", "run", __file__,
        "--server.port", "8502",
        "--server.address", "localhost",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    sys.exit(stcli.main())                                                                                                       import streamlit as st
import requests

st.set_page_config(page_title="FinRisk Dashboard", layout="wide")
st.title("FinRisk AI Agents Dashboard")

with st.sidebar:
api_url = st.text_input("API URL", "http://localhost:8000")
st.caption("Version 0.1.0")

st.header("Risk Analysis")
col1, col2 = st.columns(2)

with col1:
symbols = st.text_area("Stock Symbols", "AAPL\nMSFT\nGOOGL", height=100)

with col2:
weights = st.text_area("Weights", "0.33\n0.33\n0.34", height=100)

if st.button("Analyze", type="primary"):
try:
symbols_list = [s.strip() for s in symbols.split("\n") if s.strip()]
weights_list = [float(w.strip()) for w in weights.split("\n") if w.strip()]

text

澶嶅埗

涓嬭浇
    response = requests.post(
        f"{api_url}/analyze",
        json={"symbols": symbols_list, "weights": weights_list}
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            st.success("Analysis completed")
            col1, col2, col3 = st.columns(3)
            col1.metric("Volatility", f"{result['volatility']:.4f}")
            col2.metric("VaR(95%)", f"{result['var_95']:.4f}")
            col3.metric("Sharpe Ratio", f"{result['sharpe']:.2f}")
        else:
            st.error(f"Error: {result.get('error')}")
except Exception as e:
    st.error(f"Request failed: {e}")
st.caption("2023 FinRisk AI Agents")

