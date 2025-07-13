import streamlit as st
import time
import ntplib
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# 🔁 自動更新（1秒ごと）
st_autorefresh(interval=1000, limit=None, key="autorefresh")

# 🧠 初期状態定義
if "start_time" not in st.session_state:
    try:
        c = ntplib.NTPClient()
        response = c.request("time.apple.com", version=3)
        utc_time = datetime.utcfromtimestamp(response.tx_time)
        jst_time = utc_time + timedelta(hours=9)
        st.session_state.start_time = jst_time
        st.session_state.last_sync = time.time()
        st.session_state.sync_history = [jst_time.strftime("%H:%M:%S")]
    except Exception as e:
        st.error("NTP初期取得失敗")
        st.stop()

# ⏳ 経過時間で現在時刻を自走
elapsed = time.time() - st.session_state.last_sync
current_time = st.session_state.start_time + timedelta(seconds=int(elapsed))

# ⏱️ 1分ごとに再同期
if int(elapsed) >= 60:
    try:
        c = ntplib.NTPClient()
        response = c.request("time.apple.com", version=3)
        new_utc = datetime.utcfromtimestamp(response.tx_time)
        new_jst = new_utc + timedelta(hours=9)
        st.session_state.start_time = new_jst
        st.session_state.last_sync = time.time()

        # 🧾 同期履歴更新（先頭追加・最大5件まで）
        timestamp = new_jst.strftime("%H:%M:%S")
        st.session_state.sync_history.insert(0, timestamp)
        st.session_state.sync_history = st.session_state.sync_history[:5]
    except Exception:
        st.warning("再同期失敗：自走継続中")

# 🕒 時刻表示
formatted = current_time.strftime("%H:%M:%S")
st.markdown(f"## ⏱️ 日本標準時（JST）： {formatted}")

# 📋 過去の同期履歴表示
st.markdown("### 🧭 過去のNTP同期時刻（最新 → 古い）")
for i, ts in enumerate(st.session_state.sync_history, 1):
    st.markdown(f"- {i}. {ts}")
