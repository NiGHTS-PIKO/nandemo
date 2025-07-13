import streamlit as st
import time
import ntplib
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# 🔁 自動更新（1秒ごと）
st_autorefresh(interval=1000, limit=None, key="autorefresh")

# 🧠 セッション初期化
if "start_time" not in st.session_state:
    st.session_state.sync_history = []  # 履歴初期化
    try:
        c = ntplib.NTPClient()
        response = c.request("time.apple.com", version=3)
        utc_time = datetime.utcfromtimestamp(response.tx_time)
        jst_time = utc_time + timedelta(hours=9)
        st.session_state.start_time = jst_time
        st.session_state.last_sync = time.time()

        # 📋 履歴へ追加（年月日＋曜日表示）
        formatted = jst_time.strftime("%Y年%m月%d日（%a） %H:%M:%S")
        st.session_state.sync_history.insert(0, formatted)
    except Exception as e:
        st.error("初回NTP取得失敗")
        st.stop()

# ⏳ 経過時間で現在時刻構築
elapsed = time.time() - st.session_state.last_sync
current_time = st.session_state.start_time + timedelta(seconds=int(elapsed))

# 🔄 1分経過でNTP再取得
if int(elapsed) >= 60:
    try:
        c = ntplib.NTPClient()
        response = c.request("time.apple.com", version=3)
        new_utc = datetime.utcfromtimestamp(response.tx_time)
        new_jst = new_utc + timedelta(hours=9)
        st.session_state.start_time = new_jst
        st.session_state.last_sync = time.time()

        formatted = new_jst.strftime("%Y年%m月%d日（%a） %H:%M:%S")
        st.session_state.sync_history.insert(0, formatted)
        st.session_state.sync_history = st.session_state.sync_history[:5]
    except Exception:
        st.warning("NTP再取得失敗：自走継続")

# 🕒 現在時刻の表示（年月日＋曜日）
display_time = current_time.strftime("%Y年%m月%d日（%a） %H:%M:%S")
st.markdown(f"## 🕰️ 現在の日本標準時： {display_time}")

# 📋 履歴表示
st.markdown("### 🧭 NTP同期履歴（最新 → 過去）")
for i, entry in enumerate(st.session_state.sync_history, 1):
    st.markdown(f"- {i}. {entry}")
