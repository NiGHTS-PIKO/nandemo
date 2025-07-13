import streamlit as st
import time

st.title("⏱️ コロン点滅タイマー")

col1, col2, col3 = st.columns(3)
with col1:
    hours = st.number_input("時間", 0, 23, 0)
with col2:
    minutes = st.number_input("分", 0, 59, 0)
with col3:
    seconds = st.number_input("秒", 0, 59, 10)

total = int(hours * 3600 + minutes * 60 + seconds)

if st.button("スタート！"):
    placeholder = st.empty()
    for i in reversed(range(total + 1)):
        h = i // 3600
        m = (i % 3600) // 60
        s = i % 60

        # ⌛ 点滅用コロン
        colon = ":" if i % 2 == 0 else " "

        time_str = f"{h:02d}{colon}{m:02d}{colon}{s:02d}"
        placeholder.markdown(f"## 残り {time_str}")

        time.sleep(1)

    placeholder.markdown("## ✅ タイマー終了！")
