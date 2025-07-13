import streamlit as st
import subprocess
import base64
import streamlit.components.v1 as stc
import requests
import os

# 🔧 JavaとWAVファイルの設定
JAVA_CLASS_PATH = "kitchenTimer"     # .class があるフォルダ（ディレクトリ名のみ）
JAVA_CLASS_NAME = "TimerService"     # クラス名（.class ファイル名と一致）

WAV_URL = "https://raw.githubusercontent.com/NiGHTS-PIKO/nandemo/main/kitchenTimer/kaeru.wav"
WAV_LOCAL_PATH = "kaeru_temp.wav"

# 🔊 WAVを準備
def fetch_wav():
    if not os.path.exists(WAV_LOCAL_PATH):
        r = requests.get(WAV_URL)
        with open(WAV_LOCAL_PATH, "wb") as f:
            f.write(r.content)

def load_audio_base64():
    with open(WAV_LOCAL_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode()

def play_kaeru():
    b64 = load_audio_base64()
    html = f"""
    <audio autoplay>
        <source src="data:audio/wav;base64,{b64}" type="audio/wav">
    </audio>
    """
    stc.html(html, height=0)

# 🖼️ UI
st.title("🐸 Java連携キッチンタイマー")
st.caption("Javaでタイマー制御し、終了後にカエルが鳴きます！")

minutes = st.slider("タイマー時間（分）", 1, 30, 3)

if "java_timer_started" not in st.session_state:
    st.session_state.java_timer_started = False
    st.session_state.java_timer_finished = False

if st.button("スタート"):
    st.session_state.java_timer_started = True
    st.session_state.java_timer_finished = False
    fetch_wav()

    # Java タイマーを呼び出す（事前に .class が存在している必要あり）
    result = subprocess.run(["java", "-cp", JAVA_CLASS_PATH, JAVA_CLASS_NAME, str(minutes * 60)],
                            capture_output=True, text=True)

    if "TIME_UP" in result.stdout:
        st.session_state.java_timer_finished = True

# 状態表示
if st.session_state.java_timer_started and not st.session_state.java_timer_finished:
    st.info("⏳ Javaタイマー実行中...")

if st.session_state.java_timer_finished:
    st.success("⏰ 時間です！カエルが鳴きます！")
    play_kaeru()
