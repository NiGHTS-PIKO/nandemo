import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh

# 🔁 描画更新（100ms）
st_autorefresh(interval=100, limit=None, key="tick")

st.title("⏱️ カエルフェスタタイマー")

# 🧠 状態初期化
default_keys = {
    "hours": 0, "minutes": 0, "seconds": 0,
    "remaining": 0, "running": False, "paused": False,
    "last_update": None, "played_frogfest": False
}
for key, value in default_keys.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 🕹️ 入力欄
col1, col2, col3 = st.columns(3)
with col1:
    st.session_state.hours = st.number_input("時間", 0, 23, st.session_state.hours)
with col2:
    st.session_state.minutes = st.number_input("分", 0, 59, st.session_state.minutes)
with col3:
    st.session_state.seconds = st.number_input("秒", 0, 59, st.session_state.seconds)

# ⏱️ 初期時間
initial_total = int(
    st.session_state.hours * 3600 +
    st.session_state.minutes * 60 +
    st.session_state.seconds
)

# 🎮 ボタン群
colA, colB, colC, colD = st.columns(4)
with colA:
    if st.button("スタート"):
        if not st.session_state.running and not st.session_state.paused:
            st.session_state.remaining = initial_total  # ✅ 最初だけリセット
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
            st.session_state[key] = 0 if key != "last_update" else None
        st.session_state.played_frogfest = False

# ⏳ カウント処理
if st.session_state.running and st.session_state.remaining > 0:
    now = time.time()
    elapsed = now - st.session_state.last_update
    if elapsed >= 1.0:
        st.session_state.remaining = max(0, st.session_state.remaining - int(elapsed))
        st.session_state.last_update = now

# 💓 点滅ドット（1秒周期）
dot = "." if int(time.time()) % 2 == 0 else " "

# 🕒 時間表示構築
h = st.session_state.remaining // 3600
m = (st.session_state.remaining % 3600) // 60
s = st.session_state.remaining % 60
time_str = f"{h:02d}:{m:02d}:{s:02d}{dot}"

# 📺 表示フェーズ
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
    # 🐸 ケロケロフェス：ドットと同期して10匹点滅
    blink_on = int(time.time()) % 2 == 0
    frogs = "🐸 " * 10 if blink_on else "　" * 10
    st.markdown(f"## {frogs}<br>🎵 ケロケロフェス終了！", unsafe_allow_html=True)
