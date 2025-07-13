import streamlit as st
import time
import ntplib
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# 🔁 自動更新（128ms）
st_autorefresh(interval=128, limit=None, key="autorefresh")

# 🗓️ 日本語曜日マップ
weekday_map = {
    "Mon": "月", "Tue": "火", "Wed": "水",
    "Thu": "木", "Fri": "金", "Sat": "土", "Sun": "日"
}

# 🧠 初期化：NTP取得と履歴設定
if "start_time" not in st.session_state:
    st.session_state.sync_history = []
    try:
        c = ntplib.NTPClient()
        response = c.request("time.apple.com", version=3)
        corrected_time = response.tx_time + (response.delay / 2)
        jst_time = datetime.utcfromtimestamp(corrected_time) + timedelta(hours=9)

        st.session_state.start_time = jst_time
        st.session_state.last_sync = time.time()

        weekday_ja = weekday_map[jst_time.strftime("%a")]
        timestamp = jst_time.strftime(f"%Y年%m月%d日（{weekday_ja}） %H:%M:%S")
        rtt_ms = round(response.delay * 1000)
        entry = f"{timestamp} ±{rtt_ms}ms"
        st.session_state.sync_history.insert(0, entry)
    except Exception:
        st.error("NTP初期取得失敗。接続環境をご確認ください。")
        st.stop()

# ⏳ 自走時刻の算出
elapsed = time.time() - st.session_state.last_sync
current_time = st.session_state.start_time + timedelta(seconds=int(elapsed))

# 🔄 NTP再取得（1分ごと）
if int(elapsed) >= 60:
    try:
        c = ntplib.NTPClient()
        response = c.request("time.apple.com", version=3)
        corrected_time = response.tx_time + (response.delay / 2)
        new_jst = datetime.utcfromtimestamp(corrected_time) + timedelta(hours=9)

        st.session_state.start_time = new_jst
        st.session_state.last_sync = time.time()

        weekday_ja = weekday_map[new_jst.strftime("%a")]
        timestamp = new_jst.strftime(f"%Y年%m月%d日（{weekday_ja}） %H:%M:%S")
        rtt_ms = round(response.delay * 1000)
        entry = f"{timestamp} ±{rtt_ms}ms"
        st.session_state.sync_history.insert(0, entry)
        st.session_state.sync_history = st.session_state.sync_history[:5]
    except:
        st.warning("NTP再取得失敗：自走を継続します")

# 🕰️ 現在時刻の表示（2行＋中央＋大文字）
weekday_ja = weekday_map[current_time.strftime("%a")]
date_line = current_time.strftime(f"%Y年%m月%d日（{weekday_ja}）")
time_line = current_time.strftime("%H:%M:%S")

st.markdown("## 🕰️ 現在の日本標準時")
st.markdown(f"<h1 style='text-align:center;'>{date_line}</h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align:center;'>{time_line}</h1>", unsafe_allow_html=True)

# 📜 同期履歴（1行表記）
st.markdown("### 🧭 NTP同期履歴（最新 → 過去）")
for i, entry in enumerate(st.session_state.sync_history, 1):
    st.markdown(f"- {i}. {entry}")
