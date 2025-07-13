import streamlit as st
import time

st.title("⏱️ 最低限のカウントダウンタイマー")

if st.button("スタート！"):
    placeholder = st.empty()
    for i in reversed(range(11)):
        placeholder.markdown(f"## 残り {i} 秒")
        time.sleep(1)
    placeholder.markdown("## ✅ タイマー終了！")
