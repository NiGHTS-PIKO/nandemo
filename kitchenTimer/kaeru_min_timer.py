import streamlit as st
import time

st.title("⏱️ フル指定型カウントダウンタイマー")

# 🧮 時間・分・秒を入力
col1, col2, col3 = st.columns(3)
with col1:
    hours = st.number_input("時間", min_value=0, max_value=23, value=0, step=1)
with col2:
    minutes = st.number_input("分", min_value=0, max_value=59, value=0, step=1)
with col3:
    seconds = st.number_input("秒", min_value=0, max_value=59, value=10, step=1)

# 📦 合計秒数を計算
total_seconds = int(hours * 3600 + minutes * 60 + seconds)

# 🕹️ タイマー開始ボタン
if st.button("スタート！"):
    placeholder = st.empty()
    for i in reversed(range(total_seconds + 1)):
        h = i // 3600
        m = (i % 3600) // 60
        s = i % 60
        placeholder.markdown(f"## 残り {h:02d}:{m:02d}:{s:02d}")
        time.sleep(1)
    placeholder.markdown("## ✅ タイマー終了！")
