import streamlit as st
import time
import ntplib
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# 🔁 自動更新（1秒ごと）
st_autorefresh(interval=1000, limit=None, key="autorefresh")

# 🗓️ 日本語曜日マップ
weekday_map = {
    "Mon": "月", "Tue": "火", "Wed": "水",
    "Thu": "木", "Fri": "金", "Sat": "土", "Sun": "日"
}

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

        # 📋 履歴へ初回追加（フォーマット済み）
        weekday_ja = weekday_map[jst_time.strftime("%a")]
        formatted = jst_time.strftime(f"%Y年%m月%d日（{weekday_ja}） %H:%M:%S")
        st.session_state.sync_history.insert(0, formatted)
    except Exception as e:
        st.error("初回NTP取得失敗。ネット接続をご確認ください。")
        st.stop()

# ⏳ 経過時間で現在時刻を構築
elapsed = time.time() - st.session_state.last_sync
current_time = st.session_state.start_time + timedelta(seconds=int(elapsed))

# 🔄 1分ごとに再同期（履歴へ追加）
if int(elapsed) >= 60:
    try:
        c = ntplib.NTPClient()
        response = c.request("time.apple.com", version=3)
        new_utc = datetime.utcfromtimestamp(response.tx_time)
        new_jst = new_utc + timedelta(hours=9)
        st.session_state.start_time = new_jst
        st.session_state.last_sync = time.time()

        weekday_ja = weekday_map[new_jst.strftime("%a")]
        formatted = new_jst.strftime(f"%Y年%m月%d日（{weekday_ja}） %H:%M:%S")
        st.session_state.sync_history.insert(0, formatted)
        st.session_state.sync_history = st.session_state.sync_history[:5]
    except Exception:
        st.warning("NTP再取得失敗：自走中")

# 🎨 3行分割表示（現在の日本標準時）
date_str = current_time.strftime("%Y年%m月%d日")
weekday_str = f"（{weekday_map[current_time.strftime('%a')]}）"
time_str = current_time.strftime("%H:%M:%S")

st.markdown("## 🕰️ 現在の日本標準時")
st.markdown(f"**{date_str}**")
st.markdown(f"**{weekday_str}**")
st.markdown(f"**{time_str}**")

# 📜 同期履歴表示（同様に3行構成）
st.markdown("### 🧭 NTP同期履歴（最新 → 過去）")
for i, entry in enumerate(st.session_state.sync_history, 1):
    try:
        dt = datetime.strptime(entry, "%Y年%m月%d日（%a） %H:%M:%S")
        weekday_ja = weekday_map[dt.strftime("%a")]
        st.markdown(f"- {i}.")
        st.markdown(f"　📅 **{dt.strftime('%Y年%m月%d日')}**")
        st.markdown(f"　🗓️ **（{weekday_ja}）**")
        st.markdown(f"　⏱️ **{dt.strftime('%H:%M:%S')}**")
    except:
        st.markdown(f"- {i}. {entry}")
