import streamlit as st
import time

st.title("⏱️ コロン点滅・一時停止・リセット対応タイマー")

# 🕹️ 入力欄
col1, col2, col3 = st.columns(3)
with col1:
    hours = st.number_input("時間", 0, 23, 0)
with col2:
    minutes = st.number_input("分", 0, 59, 0)
with col3:
    seconds = st.number_input("秒", 0, 59, 10)

initial_total = int(hours * 3600 + minutes * 60 + seconds)

# 🧠 セッション管理
if "remaining" not in st.session_state:
    st.session_state.remaining = initial_total
if "running" not in st.session_state:
    st.session_state.running = False
if "paused" not in st.session_state:
    st.session_state.paused = False
if "last_update" not in st.session_state:
    st.session_state.last_update = None

# 🔘 操作ボタン
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

# 🧮 時間更新（スタート時のみ）
if st.session_state.running and st.session_state.remaining > 0:
    now = time.time()
    elapsed = int(now - st.session_state.last_update)
    if elapsed > 0:
        st.session_state.remaining = max(0, st.session_state.remaining - elapsed)
        st.session_state.last_update = now

# 🎇 表示（コロン点滅常時）
h = st.session_state.remaining // 3600
m = (st.session_state.remaining % 3600) // 60
s = st.session_state.remaining % 60
colon = ":" if int(time.time()) % 2 == 0 else " "

time_str = f"{h:02d}{colon}{m:02d}{colon}{s:02d}"
placeholder = st.empty()

if st.session_state.remaining > 0:
    if st.session_state.running:
        placeholder.markdown(f"## ▶️ {time_str}")
    elif st.session_state.paused:
        placeholder.markdown(f"## ⏸️ {time_str}")
    else:
        placeholder.markdown(f"## ⏹️ {time_str}")  # 停止中（リセット済み）
else:
    placeholder.markdown("## ✅ タイマー終了！")
    st.session_state.running = False
    st.session_state.paused = False
