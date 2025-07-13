import streamlit as st
import time
import ntplib
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# 🔁 自動更新（1秒単位表示更新）
st_autorefresh(interval=1000, limit=None, key="autorefresh")

# 🧠 時刻セッション管理
if "start_time" not in st.session_state:
    try:
        # ⏱️ NTPからUTC時刻取得
        c = ntplib.NTPClient()
        response = c.request("time.apple.com", version=3)
        utc_time = datetime.utcfromtimestamp(response.tx_time)

        # 🌏 JSTに変換（UTC +9）
        jst_time = utc_time + timedelta(hours=9)
        st.session_state.start_time = jst_time
        st.session_state.last_sync = time.time()
    except Exception as e:
        st.error("NTP取得に失敗しました")
        st.stop()

# ⏳ 経過時間で自走クロックを再構成
elapsed = time.time() - st.session_state.last_sync
current_time = st.session_state.start_time + timedelta(seconds=int(elapsed))

# ⏱️ 1分経過したら再同期
if int(elapsed) >= 60:
    try:
        c = ntplib.NTPClient()
        response = c.request("time.apple.com", version=3)
        new_utc = datetime.utcfromtimestamp(response.tx_time)
        st.session_state.start_time = new_utc + timedelta(hours=9)
        st.session_state.last_sync = time.time()
    except Exception as e:
        st.warning("NTP再取得に失敗：継続自走中")

# 🕒 表示形式
formatted = current_time.strftime("%H:%M:%S")
st.markdown(f"## ⏱️ 日本標準時（JST）： {formatted}")
