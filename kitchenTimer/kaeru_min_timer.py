import streamlit as st
import time

st.title("⏱️ カウントダウンタイマー（操作可能）")

# 🔧 時間指定
col1, col2, col3 = st.columns(3)
with col1:
    hours = st.number_input("時間", min_value=0, max_value=23, value=0)
with col2:
    minutes = st.number_input("分", min_value=0, max_value=59, value=0)
with col3:
    seconds = st.number_input("秒", min_value=0, max_value=59, value=10)

total = int(hours * 3600 + minutes * 60 + seconds)

# 🧠 セッションステートの初期化
if "remaining" not in st.session_state:
    st.session_state.remaining = total
if "running" not in st.session_state:
    st.session_state.running = False

# 🎮 操作ボタン
start = st.button("スタート")
pause = st.button("一時停止")
reset = st.button("クリア")

# 🕹️ 操作処理
if start:
    st.session_state.running = True
elif pause:
    st.session_state.running = False
elif reset:
    st.session_state.running = False
    st.session_state.remaining = total

# 🔁 タイマー表示
placeholder = st.empty()

if st.session_state.running and st.session_state.remaining > 0:
    for i in range(st.session_state.remaining, -1, -1):
        h = i // 3600
        m = (i % 3600) // 60
        s = i % 60
        placeholder.markdown(f"## 残り {h:02d}:{m:02d}:{s:02d}")
        st.session_state.remaining = i
        time.sleep(1)
        if not st.session_state.running:
            break
    if st.session_state.remaining == 0:
        st.success("✅ タイマー終了！")
