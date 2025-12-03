# simplest_app.py - 最简单的Streamlit应用
import streamlit as st

st.title("🎯 FinRisk 测试页面")
st.write("如果看到这个页面，说明一切正常")

if st.button("点击测试"):
    st.success("✅ 测试成功！")
    st.balloons()
    st.write("恭喜！系统工作正常")
