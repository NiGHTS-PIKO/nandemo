import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh
import numpy as np

# 🔁 0.1秒間隔で描画更新
st_autorefresh(interval=100, limit=None, key="tick")

st.title("⏱️ カエルフェス終了演出タイマー")

# 🧠 セッション初期化
for key in ["hours", "minutes", "seconds", "remaining", "running", "paused", "last_update"]:
    if key not in st.session_state:
        st.session_state[key] = 0 if key in ["hours", "minutes", "seconds", "remaining"] else False
if "played_frogfest" not in st.session_state:
    st.session_state.played_frogfest = False

# 🕹️ 時間設定
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
        st.session_state.played_frogfest = False
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
        st.session_state.played_frogfest = False
with colD:
    if st.button("🧹オールリセット"):
        for key in ["hours", "minutes", "seconds", "remaining", "running", "paused", "last_update"]:
            st.session_state[key] = 0 if key in ["hours", "minutes", "seconds", "remaining"] else False
        st.session_state.played_frogfest = False

# ⏱️ 秒単位カウント
if st.session_state.running and st.session_state.remaining > 0:
    now = time.time()
    elapsed = now - st.session_state.last_update
    if elapsed >= 1.0:
        st.session_state.remaining = max(0, st.session_state.remaining - int(elapsed))
        st.session_state.last_update = now

# 💓 点滅ドット（1秒周期）
dot = "." if int(time.time()) % 2 == 0 else " "

# 🖼️ 時間表示
h = st.session_state.remaining // 3600
m = (st.session_state.remaining % 3600) // 60
s = st.session_state.remaining % 60
time_str = f"{h:02d}:{m:02d}:{s:02d}{dot}"

# 📺 タイマー表示 or フェス演出
if st.session_state.remaining > 0:
    if st.session_state.running:
        st.markdown(f"## ▶️ {time_str}")
    elif st.session_state.paused:
        st.markdown(f"## ⏸️ {time_str}")
    else:
        st.markdown(f"## ⏹️ {time_str}")
else:
    st.session_state.running = False
    st.session_state.paused = False
    # 🐸 カエル顔点滅（ドットと同期）
    blink_on = int(time.time()) % 2 == 0
    frogs = "🐸 " * 10 if blink_on else "　" * 10
    st.markdown(f"## {frogs}<br>🎵 ケロケロフェス終了！", unsafe_allow_html=True)
