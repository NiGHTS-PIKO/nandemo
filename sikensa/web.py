import streamlit as st
import matplotlib.pyplot as plt
import re

# セッション初期化
if "blocks" not in st.session_state:
    st.session_state.blocks = []

st.title("🗣️ 自然言語シーケンス図面ビルダー")

# --- 自然言語入力フォーム ---
user_input = st.text_area("自然言語で工程を記述してください（例：センサAがステップ0で2秒間ON）")
if st.button("解析して追加"):
    pattern = r"(\S+)がステップ(\d+)で(\d+)秒"
    matches = re.findall(pattern, user_input)
    for name, step, duration in matches:
        st.session_state.blocks.append({
            "name": name,
            "step": int(step),
            "duration": int(duration)
        })

# --- 図の描画 ---
fig, ax = plt.subplots(figsize=(8, len(st.session_state.blocks)))
for block in st.session_state.blocks:
    ax.barh(block["name"], block["duration"], left=block["step"], color="lightgreen")
ax.set_xlabel("ステップ")
ax.set_ylabel("信号ブロック")
ax.grid(True)
st.pyplot(fig)
