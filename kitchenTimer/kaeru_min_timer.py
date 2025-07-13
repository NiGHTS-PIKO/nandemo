import streamlit as st
import time

st.title("⏱️ 一時停止時に点滅するタイマー")

# 🧮 時間指定
col1, col2, col3 = st.columns(3)
with col1:
    hours = st.number_input("時間", 0, 23, 0)
with col2:
    minutes = st.number_input("分", 0, 59, 0)
with col3:
    seconds = st.number_input("秒", 0, 59, 10)

initial_total = int(hours * 3600 + minutes * 60 + seconds)

# 🧠 セッション初期化
if "remaining" not in st.session_state:
    st.session_state.remaining = initial_total
if "running" not in st.session_state:
    st.session_state.running = False
if "paused" not in st.session_state:
    st.session_state.paused = False
if "last_tick" not in st.session_state:
    st.session_state.last_tick = None
if "blink" not in st.session_state:
    st.session_state.blink = True

# 🎮 操作ボタン
start = st.button("スタート")
pause = st.button("一時停止")
reset = st.button("クリア")

# 🕹️ ボタン処理
if start:
    st.session_state.running = True
    st.session_state.paused = False
    st.session_state.last_tick = time.time()
elif pause:
    st.session_state.running = False
    st.session_state.paused = True
elif reset:
    st.session_state.running = False
    st.session_state.paused = False
    st.session_state.remaining = initial_total
    st.session_state.last_tick = None
    st.session_state.blink = True

# ⏱️ タイマー更新
if st.session_state.running and st.session_state.remaining > 0:
    now = time.time()
    elapsed = int(now - st.session_state.last_tick)
    if elapsed > 0:
        st.session_state.remaining -= elapsed
        st.session_state.last_tick = now

# 👁️ 表示領域
h = st.session_state.remaining // 3600
m = (st.session_state.remaining % 3600) // 60
s = st.session_state.remaining % 60

placeholder = st.empty()

# 🔦 通常表示
if st.session_state.running:
    placeholder.markdown(f"## 残り {h:02d}:{m:02d}:{s:02d}")

# 🔁 一時停止中 → 点滅させる
elif st.session_state.paused:
    if st.session_state.blink:
        placeholder.markdown(f"## ⏸️ 残り {h:02d}:{m:02d}:{s:02d}")
    else:
        placeholder.markdown(" ")  # 空白表示
    time.sleep(0.5)  # 点滅間隔
    st.session_state.blink = not st.session_state.blink

# 🔚 終了時
if st.session_state.remaining <= 0:
    placeholder.markdown("## ✅ タイマー終了！")
    st.session_state.running = False
    st.session_state.paused = False
