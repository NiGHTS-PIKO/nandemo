import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh

# 🔁 自動描画：0.1秒ごとに更新
st_autorefresh(interval=100, limit=None, key="tick")

st.title("⏱️ フルリセット対応タイマー")

# 🧠 状態初期化（default: 00:00:00）
if "hours" not in st.session_state:
    st.session_state.hours = 0
if "minutes" not in st.session_state:
    st.session_state.minutes = 0
if "seconds" not in st.session_state:
    st.session_state.seconds = 0
if "remaining" not in st.session_state:
    st.session_state.remaining = 0
if "running" not in st.session_state:
    st.session_state.running = False
if "paused" not in st.session_state:
    st.session_state.paused = False
if "last_update" not in st.session_state:
    st.session_state.last_update = None

# 🕹️ 時間設定欄（セッションステートに直結）
col1, col2, col3 = st.columns(3)
with col1:
    st.session_state.hours = st.number_input("時間", 0, 23, st.session_state.hours)
with col2:
    st.session_state.minutes = st.number_input("分", 0, 59, st.session_state.minutes)
with col3:
    st.session_state.seconds = st.number_input("秒", 0, 59, st.session_state.seconds)

initial_total = int(st.session_state.hours * 3600 +
                    st.session_state.minutes * 60 +
                    st.session_state.seconds)

# 🎮 操作ボタン群
colA, colB, colC, colD = st.columns(4)
with colA:
    if st.button("スタート"):
        st.session_state.remaining = initial_total
        st.session_state.running = True
        st.session_state.paused = False
        st.session_state.last_update = time.time()
with colB:
    if st.button("一時停止"):
        st.session_state.running = False
        st.session_state.paused = True
with colC:
    if st.button("セット/リセット"):
        st.session_state.remaining = initial_total
        st.session_state.running = False
        st.session_state.paused = False
        st.session_state.last_update = None
with colD:
    if st.button("🧹オールリセット"):
        st.session_state.hours = 0
        st.session_state.minutes = 0
        st.session_state.seconds = 0
        st.session_state.remaining = 0
        st.session_state.running = False
        st.session_state.paused = False
        st.session_state.last_update = None

# ⏱️ 残り時間更新（1秒単位）
if st.session_state.running and st.session_state.remaining > 0:
    now = time.time()
    elapsed = now - st.session_state.last_update
    if elapsed >= 1.0:
        st.session_state.remaining = max(0, st.session_state.remaining - int(elapsed))
        st.session_state.last_update = now

# 💓 ドット点滅（1秒ごと）
dot = "." if int(time.time()) % 2 == 0 else " "

# 🖼️ 表示文字列
h = st.session_state.remaining // 3600
m = (st.session_state.remaining % 3600) // 60
s = st.session_state.remaining % 60
time_str = f"{h:02d}:{m:02d}:{s:02d}{dot}"

# 📺 タイマー表示
if st.session_state.remaining > 0:
    if st.session_state.running:
        st.markdown(f"## ▶️ {time_str}")
    elif st.session_state.paused:
        st.markdown(f"## ⏸️ {time_str}")
    else:
        st.markdown(f"## ⏹️ {time_str}")
else:
    st.markdown("## ✅ タイマー終了！")
    st.session_state.running = False
    st.session_state.paused = False
