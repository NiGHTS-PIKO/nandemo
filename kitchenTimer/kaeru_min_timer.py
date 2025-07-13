import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh

# 🔁 0.1秒ごとに再描画（UIなめらか）
st_autorefresh(interval=100, limit=None, key="tick")

st.title("⏱️ 正確な鼓動タイマー")

# 🕹️ 時間設定欄
col1, col2, col3 = st.columns(3)
with col1:
    hours = st.number_input("時間", 0, 23, 0)
with col2:
    minutes = st.number_input("分", 0, 59, 0)
with col3:
    seconds = st.number_input("秒", 0, 59, 10)

initial_total = int(hours * 3600 + minutes * 60 + seconds)

# 🧠 ステート初期化
if "remaining" not in st.session_state:
    st.session_state.remaining = initial_total
if "running" not in st.session_state:
    st.session_state.running = False
if "paused" not in st.session_state:
    st.session_state.paused = False
if "last_update" not in st.session_state:
    st.session_state.last_update = None

# 🎮 操作ボタン
colA, colB, colC = st.columns(3)
with colA:
    if st.button("スタート"):
        st.session_state.running = True
        st.session_state.paused = False
        st.session_state.last_update = time.time()
with colB:
    if st.button("一時停止"):
        st.session_state.running = False
        st.session_state.paused = True
with colC:
    if st.button("リセット"):
        st.session_state.running = False
        st.session_state.paused = False
        st.session_state.remaining = initial_total
        st.session_state.last_update = None

# ⏱️ カウント処理（1秒単位で更新）
if st.session_state.running and st.session_state.remaining > 0:
    now = time.time()
    elapsed = now - st.session_state.last_update
    if elapsed >= 1.0:
        st.session_state.remaining = max(0, st.session_state.remaining - int(elapsed))
        st.session_state.last_update = now

# 💓 コロン点滅（1秒間隔）
colon = ":" if int(time.time()) % 2 == 0 else " "

# 🎨 表示構築
h = st.session_state.remaining // 3600
m = (st.session_state.remaining % 3600) // 60
s = st.session_state.remaining % 60
time_str = f"{h:02d}{colon}{m:02d}{colon}{s:02d}"

# 📺 UI表示
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
