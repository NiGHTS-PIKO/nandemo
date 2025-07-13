import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh

# 🔁 UI更新頻度（0.1秒ごとに自動描画リフレッシュ）
st_autorefresh(interval=100, limit=None, key="tick")

st.title("⏱️ 鼓動ドット付きタイマー")

# 🧮 入力セクション（時間・分・秒）
col1, col2, col3 = st.columns(3)
with col1:
    hours = st.number_input("時間", 0, 23, 0)
with col2:
    minutes = st.number_input("分", 0, 59, 0)
with col3:
    seconds = st.number_input("秒", 0, 59, 10)

# 🔢 初期時間を秒単位で計算
initial_total = int(hours * 3600 + minutes * 60 + seconds)

# 🧠 セッションステート管理
if "remaining" not in st.session_state:
    st.session_state.remaining = initial_total
if "running" not in st.session_state:
    st.session_state.running = False
if "paused" not in st.session_state:
    st.session_state.paused = False
if "last_update" not in st.session_state:
    st.session_state.last_update = None

# 🎮 操作ボタン群
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

# ⏱️ 時間経過に応じたカウント更新（1秒単位）
if st.session_state.running and st.session_state.remaining > 0:
    now = time.time()
    elapsed = now - st.session_state.last_update
    if elapsed >= 1.0:
        st.session_state.remaining = max(0, st.session_state.remaining - int(elapsed))
        st.session_state.last_update = now

# 💓 ドット点滅演出（1秒ごと）
dot = "." if int(time.time()) % 2 == 0 else " "

# 🖼️ 時間表示整形：ドットは秒の右側に配置
h = st.session_state.remaining // 3600
m = (st.session_state.remaining % 3600) // 60
s = st.session_state.remaining % 60
time_str = f"{h:02d}:{m:02d}:{s:02d}{dot}"

# 📺 状態に応じた表示
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
