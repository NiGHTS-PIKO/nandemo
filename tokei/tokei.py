import streamlit as st
import time
import ntplib
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# 🔁 秒単位でUI自動更新
st_autorefresh(interval=1000, limit=None, key="autorefresh")

# 🧠 セッション初期化（履歴も含む）
if "start_time" not in st.session_state:
    st.session_state.sync_history = []  # ✅ 初期履歴定義
    try:
        c = ntplib.NTPClient()
        response = c.request("time.apple.com", version=3)
        utc_time = datetime.utcfromtimestamp(response.tx_time)
        jst_time = utc_time + timedelta(hours=9)
        st.session_state.start_time = jst_time
        st.session_state.last_sync = time.time()
        st.session_state.sync_history.insert(0, jst_time.strftime("%H:%M:%S"))
    except Exception as e:
        st.error("初回NTP取得失敗。ネット接続をご確認ください。")
        st.stop()

# ⏳ 経過時間で自走表示
elapsed = time.time() - st.session_state.last_sync
current_time = st.session_state.start_time + timedelta(seconds=int(elapsed))

# 🔄 1分ごとに再同期
if int(elapsed) >= 60:
    try:
        c = ntplib.NTPClient()
        response = c.request("time.apple.com", version=3)
        new_utc = datetime.utcfromtimestamp(response.tx_time)
        new_jst = new_utc + timedelta(hours=9)
        st.session_state.start_time = new_jst
        st.session_state.last_sync = time.time()

        # 🧾 履歴追加（最大5件保持）
        timestamp = new_jst.strftime("%H:%M:%S")
        st.session_state.sync_history.insert(0, timestamp)
        st.session_state.sync_history = st.session_state.sync_history[:5]
    except Exception:
        st.warning("NTP再取得失敗：自走中")

# ⏱️ 表示
formatted = current_time.strftime("%H:%M:%S")
st.markdown(f"## 🕰️ 現在の日本標準時： {formatted}")

# 📋 同期履歴表示（存在チェックも不要）
st.markdown("### 🧭 NTP同期履歴（最新→過去）")
for i, ts in enumerate(st.session_state.sync_history, 1):
    st.markdown(f"- {i}. {ts}")
