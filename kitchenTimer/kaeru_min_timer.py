import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh
import numpy as np
import sounddevice as sd

# 🔁 自動描画更新（100ms）
st_autorefresh(interval=100, limit=None, key="tick")

st.title("⏱️ 鳴きカエル付きタイマー")

# 🧠 初期ステート
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
if "played_song" not in st.session_state:
    st.session_state.played_song = False

# 🎵 カエルの歌（NumPy波形）生成関数
def kaeru_song():
    fs = 44100
    notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00]  # C D E F G A
    melody = notes + notes[::-1]
    note_duration = 0.4
    volume = 0.4
    song = np.array([])
    for freq in melody:
        t = np.linspace(0, note_duration, int(fs * note_duration), endpoint=False)
        wave = volume * np.sin(2 * np.pi * freq * t)
        song = np.concatenate((song, wave))
    sd.play(song, samplerate=fs)

# 🎮 時間設定（セッションと同期）
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
        st.session_state.played_song = False
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
        st.session_state.played_song = False
with colD:
    if st.button("🧹オールリセット"):
        st.session_state.hours = 0
        st.session_state.minutes = 0
        st.session_state.seconds = 0
        st.session_state.remaining = 0
        st.session_state.running = False
        st.session_state.paused = False
        st.session_state.last_update = None
        st.session_state.played_song = False

# ⏱️ 時間更新ロジック
if st.session_state.running and st.session_state.remaining > 0:
    now = time.time()
    elapsed = now - st.session_state.last_update
    if elapsed >= 1.0:
        st.session_state.remaining = max(0, st.session_state.remaining - int(elapsed))
        st.session_state.last_update = now

# 💓 点滅ドット（1秒ごと）
dot = "." if int(time.time()) % 2 == 0 else " "

# 🖼️ 表示文字列
h = st.session_state.remaining // 3600
m = (st.session_state.remaining % 3600) // 60
s = st.session_state.remaining % 60
time_str = f"{h:02d}:{m:02d}:{s:02d}{dot}"

# 📺 表示とカエルの歌呼び出し
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

    # 🐸 カエルの歌（0秒で鳴らす）
    if not st.session_state.played_song:
        kaeru_song()
        st.session_state.played_song = True
