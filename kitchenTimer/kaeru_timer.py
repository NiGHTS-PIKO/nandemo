import streamlit as st
import time
import base64
import streamlit.components.v1 as stc
from datetime import datetime

# 初期化
if "total_seconds" not in st.session_state:
    st.session_state.total_seconds = 0
if "running" not in st.session_state:
    st.session_state.running = False
if "paused" not in st.session_state:
    st.session_state.paused = False
if "beeping" not in st.session_state:
    st.session_state.beeping = False

def load_audio_base64(path):
    with open(path, "rb") as f:
        audio_bytes = f.read()
    return base64.b64encode(audio_bytes).decode()

def play_audio_once(audio_base64):
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
    </audio>
    """
    stc.html(audio_html, height=0)

# UI表示
st.title("🧑‍🍳 よくあるキッチンタイマー（Web版）")
now = datetime.now()
weekday = ["月", "火", "水", "木", "金", "土", "日"][now.weekday()]
st.caption(f"現在時刻: {now.strftime(f'%Y/%m/%d（{weekday}）%H:%M')}")

# タイマー表示
hrs, rem = divmod(st.session_state.total_seconds, 3600)
mins, secs = divmod(rem, 60)
st.header(f"⏳ {hrs:02}:{mins:02}:{secs:02}")

# 音声読み込み（WAVファイルのパスを指定）
audio_base64 = load_audio_base64("kaeru.wav")

# ボタン操作
def stop_beep():
    st.session_state.beeping = False

def increment(sec):
    st.session_state.total_seconds += sec
    stop_beep()

def reset():
    st.session_state.total_seconds = 0
    st.session_state.running = False
    st.session_state.paused = False
    stop_beep()

def start_or_pause():
    if not st.session_state.running:
        st.session_state.running = True
        st.session_state.paused = False
    else:
        st.session_state.paused = not st.session_state.paused
    stop_beep()

# 時間加算ボタン（例）
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("＋1分", on_click=lambda: increment(60)): pass
with col2:
    if st.button("＋10分", on_click=lambda: increment(600)): pass
with col3:
    if st.button("＋1時間", on_click=lambda: increment(3600)): pass

col4, col5, col6 = st.columns(3)
with col4:
    if st.button("スタート／一時停止", on_click=start_or_pause): pass
with col5:
    if st.button("リセット", on_click=reset): pass
with col6:
    if st.button("止める", on_click=stop_beep): pass

# タイマー動作
if st.session_state.running and not st.session_state.paused:
    st.session_state.total_seconds -= 1
    time.sleep(1)
    if st.session_state.total_seconds == 0:
        st.session_state.running = False
        st.session_state.beeping = True

# カエル再生ループ（最大5回）
if st.session_state.beeping:
    for i in range(5):
        if not st.session_state.beeping:
            break
        st.write(f"🐸 カエルの歌 {i+1} 回目")
        play_audio_once(audio_base64)
        time.sleep(11)  # 10秒再生＋1秒休止
    st.session_state.beeping = False
