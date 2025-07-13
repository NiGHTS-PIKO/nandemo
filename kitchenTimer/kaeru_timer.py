import streamlit as st
import subprocess
import base64
import streamlit.components.v1 as stc
import requests
import os

# 🔧 Javaファイルのパス（ローカルでクローンしてる前提）
JAVA_SRC_PATH = "kitchenTimer/TimerService.java"
JAVA_CLASS_NAME = "TimerService"

# 🔊 GitHub上の音声ファイル（WAV）
WAV_URL = "https://raw.githubusercontent.com/NiGHTS-PIKO/nandemo/main/kitchenTimer/kaeru.wav"
LOCAL_WAV_PATH = "kaeru_temp.wav"

# ✅ 初期化
st.session_state.setdefault("java_timer_started", False)
st.session_state.setdefault("java_timer_finished", False)

# 🛠 Javaのコンパイル
def compile_java():
    if not os.path.exists(f"kitchenTimer/{JAVA_CLASS_NAME}.class"):
        subprocess.run(["javac", JAVA_SRC_PATH])

# 🎮 Javaの実行（秒数を渡して呼び出し）
def run_java_timer(seconds):
    compile_java()
    result = subprocess.run(["java", JAVA_CLASS_NAME, str(seconds)], capture_output=True, text=True)
    if "TIME_UP" in result.stdout:
        st.session_state.java_timer_finished = True

# 🎵 WAVファイルの取得とbase64化
def fetch_wav():
    if not os.path.exists(LOCAL_WAV_PATH):
        r = requests.get(WAV_URL)
        with open(LOCAL_WAV_PATH, "wb") as f:
            f.write(r.content)

def load_audio_base64():
    with open(LOCAL_WAV_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode()

# 🔊 カエル再生（HTML埋め込み）
def play_kaeru():
    b64 = load_audio_base64()
    html = f"""
    <audio autoplay>
        <source src="data:audio/wav;base64,{b64}" type="audio/wav">
    </audio>
    """
    stc.html(html, height=0)

# 🖼️ UI表示
st.title("🐸 Java連携キッチンタイマー")

minutes = st.slider("タイマー時間（分）", 1, 30, 3)

if st.button("スタート"):
    st.session_state.java_timer_started = True
    st.session_state.java_timer_finished = False
    fetch_wav()
    run_java_timer(minutes * 60)

# 🎬 結果検知＆鳴き声再生
if st.session_state.java_timer_started:
    if st.session_state.java_timer_finished:
        st.success("⏰ 時間です！カエルが鳴きます！")
        play_kaeru()
    else:
        st.info("⏳ Javaタイマー実行中...")
