import streamlit as st
import time
import base64
import streamlit.components.v1 as stc
import requests
from datetime import datetime
import os

# ===================================
# 設定
# ===================================
audio_url = "https://raw.githubusercontent.com/NiGHTS-PIKO/nandemo/main/kitchenTimer/kaeru.wav"
local_path = "kaeru_temp.wav"

# セッション初期化
st.session_state.setdefault("total_seconds", 0)
st.session_state.setdefault("running", False)
st.session_state.setdefault("paused", False)
st.session_state.setdefault("beeping", False)
st.session_state.setdefault("beep_index", 0)

# カエル音声をダウンロード（初回のみ）
def fetch_audio(url, save_as):
    if not os.path.exists(save_as):
        r = requests.get(url)
        with open(save_as, "wb") as f:
            f.write(r.content)

def load_audio_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

fetch_audio(audio_url, local_path)
audio_base64 = load_audio_base64(local_path)

def play_audio():
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
    </audio>
    """
    stc.html(audio_html, height=0)

# ===================================
# UI
# ===================================
st.title("🧑‍🍳 よくあるキッチンタイマー（Web版）")
now = datetime.now()
weekday = ["月", "火", "水", "木", "金", "土", "日"][now.weekday()]
st.caption(f"現在時刻: {now.strftime(f'%Y/%m/%d（{weekday}）%H:%M')}")

hrs, rem = divmod(st.session_state.total_seconds, 3600)
mins, secs = divmod(rem, 60)
st.header(f"⏳ {hrs:02}:{mins:02}:{secs:02}")

# ===================================
# ボタン操作
# ===================================
def stop_beep():
    st.session_state.beeping = False
    st.session_state.beep_index = 0

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

# ===================================
# タイマー進行（擬似ループ）
# ===================================
if st.session_state.running and not st.session_state.paused:
    time.sleep(1)
    st.session_state.total_seconds -= 1
    if st.session_state.total_seconds <= 0:
        st.session_state.running = False
        st.session_state.beeping = True
        st.session_state.beep_index = 0
    st.experimental_rerun()

# ===================================
# カエルの鳴き声（11秒周期・最大5回）
# ===================================
if st.session_state.beeping and st.session_state.beep_index < 5:
    play_audio()
    st.write(f"🐸 カエルの歌 {st.session_state.beep_index + 1} 回目")
    st.session_state.beep_index += 1
    time.sleep(11)
    st.experimental_rerun()
elif st.session_state.beeping:
    stop_beep()
