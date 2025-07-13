import streamlit as st
import time
import ntplib
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# ⏳ 自動更新（1秒ごと）
st_autorefresh(interval=256, limit=None, key="autorefresh")

# 🗓️ 日本語曜日マップ
weekday_map = {
    "Mon": "月", "Tue": "火", "Wed": "水",
    "Thu": "木", "Fri": "金", "Sat": "土", "Sun": "日"
}

# 🧠 セッション初期化（初回取得＆履歴）
if "start_time" not in st.session_state:
    st.session_state.sync_history = []  # 履歴初期化
    try:
        c = ntplib.NTPClient()
        response = c.request("time.apple.com", version=3)
        utc_time = datetime.utcfromtimestamp(response.tx_time)
        jst_time = utc_time + timedelta(hours=9)
        st.session_state.start_time = jst_time
        st.session_state.last_sync = time.time()

        # 履歴追加（1行構成）
        weekday_ja = weekday_map[jst_time.strftime("%a")]
        formatted = jst_time.strftime(f"%Y年%m月%d日（{weekday_ja}） %H:%M:%S")
        st.session_state.sync_history.insert(0, formatted)
    except Exception as e:
        st.error("NTP初期取得失敗。インターネット接続を確認してください。")
        st.stop()

# ⏳ 経過時間で現在時刻を自走表示
elapsed = time.time() - st.session_state.last_sync
current_time = st.session_state.start_time + timedelta(seconds=int(elapsed))

# 🔄 1分ごとにNTP再同期（履歴記録）
if int(elapsed) >= 60:
    try:
        c = ntplib.NTPClient()
        response = c.request("time.apple.com", version=3)
        new_utc = datetime.utcfromtimestamp(response.tx_time)
        new_jst = new_utc + timedelta(hours=9)
        st.session_state.start_time = new_jst
        st.session_state.last_sync = time.time()

        # 履歴追加（最大5件まで）
        weekday_ja = weekday_map[new_jst.strftime("%a")]
        formatted = new_jst.strftime(f"%Y年%m月%d日（{weekday_ja}） %H:%M:%S")
        st.session_state.sync_history.insert(0, formatted)
        st.session_state.sync_history = st.session_state.sync_history[:5]
    except Exception:
        st.warning("NTP再取得失敗：自走を継続します")

# 🎨 表示（中央・大文字・2行）
date_line = current_time.strftime(f"%Y年%m月%d日（{weekday_map[current_time.strftime('%a')]})")
time_line = current_time.strftime("%H:%M:%S")

st.markdown("## 🕰️ 現在の日本標準時")
st.markdown(f"<h1 style='text-align:center;'>{date_line}</h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align:center;'>{time_line}</h1>", unsafe_allow_html=True)

# 📜 履歴表示（1行構成）
st.markdown("### 🧭 NTP同期履歴（最新 → 過去）")
for i, entry in enumerate(st.session_state.sync_history, 1):
    st.markdown(f"- {i}. {entry}")
