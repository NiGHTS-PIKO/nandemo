import streamlit as st
import time
import base64
import streamlit.components.v1 as stc
import requests
from datetime import datetime
import os

# ==========================
# 🔧 設定と初期化
# ==========================
audio_url = "https://raw.githubusercontent.com/NiGHTS-PIKO/nandemo/main/kitchenTimer/kaeru.wav"
local_path = "kaeru_temp.wav"

# セッションステート初期化
for key, value in {
    "total_seconds": 0,
    "running": False,
    "paused": False,
    "beeping": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================
# 📥 WAVダウンロード関数
# ==========================
def fetch_audio(url, save_as):
    if not os.path.exists(save_as):
        response = requests.get(url)
        with open(save_as, "wb") as f:
            f.write(response.content)

def load_audio_base64(path):
    with open(path, "rb") as f:
        audio_bytes = f.read()
    return base64.b64encode(audio_bytes).decode()

# WAV取得＆Base64化
fetch_audio(audio_url, local_path)
audio_base64 = load_audio_base64(local_path)

# ==========================
# 🔊 カエル再生（HTML埋め込み）
# ==========================
def play_audio_once(b64data):
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/wav;base64,{b64data}" type="audio/wav">
    </audio>
    """
    stc.html(audio_html, height=0)

# ==========================
# 🖼️ UI表示
# ==========================
st.title("🧑‍🍳 よくあるキッチンタイマー（Web版）")
now = datetime.now()
weekday = ["月", "火", "水", "木", "金", "土", "日"][now.weekday()]
st.caption(f"現在時刻: {now.strftime(f'%Y/%m/%d（{weekday}）%H:%M')}")

# タイマー表示
hrs, rem = divmod(st.session_state.total_seconds, 3600)
mins, secs = divmod(rem, 60)
st.header(f"⏳ {hrs:02}:{mins:02}:{secs:02}")

# ==========================
# 🎛️ ボタン操作
# ==========================
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

col1, col2, col3 = st.columns(3)
with col1: st.button("＋1分", on_click=lambda: increment(60))
with col2: st.button("＋10分", on_click=lambda: increment(600))
with col3: st.button("＋1時間", on_click=lambda: increment(3600))

col4, col5, col6 = st.columns(3)
with col4: st.button("スタート／一時停止", on_click=start_or_pause)
with col5: st.button("リセット", on_click=reset)
with col6: st.button("止める", on_click=stop_beep)

# ==========================
# ⏱️ タイマー進行ロジック
# ==========================
if st.session_state.running and not st.session_state.paused:
    st.session_state.total_seconds -= 1
    time.sleep(1)
    if st.session_state.total_seconds == 0:
        st.session_state.running = False
        st.session_state.beeping = True

# ==========================
# 🐸 カエルの鳴き声ループ再生
# ==========================
if st.session_state.beeping:
    for i in range(5):
        if not st.session_state.beeping:
            break
        st.write(f"🐸 カエルの歌 {i+1} 回目")
        play_audio_once(audio_base64)
        time.sleep(11)  # 10秒再生 + 1秒休止
    st.session_state.beeping = False
