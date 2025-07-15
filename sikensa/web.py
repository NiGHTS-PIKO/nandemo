import streamlit as st
import re

st.set_page_config(page_title="自然言語ラダー図ビューア", layout="centered")
st.title("🗣️ 自然言語ラダー図ビューア")

# --- 初期化 ---
if "ladder" not in st.session_state:
    st.session_state.ladder = []

# --- 自然言語入力 ---
user_input = st.text_area("自然言語でラダー構造を記述してください（例：X0がONのときY1を動作）")

# --- 解析と追加 ---
def parse_ladder(sentence):
    pattern = r"(X\d+)(?:と(X\d+))?(?:が)?(ON|OFF)?のとき(Y\d+)を(ON|OFF|動作)"
    matches = re.findall(pattern, sentence)
    results = []
    for match in matches:
        x1, x2, x_state, y, y_state = match
        elements = []
        if x1:
            elements.append({"type": "X", "label": x1, "state": x_state or "ON"})
        if x2:
            elements.append({"type": "X", "label": x2, "state": x_state or "ON"})
        elements.append({"type": "Y", "label": y, "state": y_state or "ON"})
        results.append({"line": len(st.session_state.ladder)+1, "elements": elements})
    return results

if st.button("解析して追加"):
    new_lines = parse_ladder(user_input)
    if new_lines:
        st.session_state.ladder.extend(new_lines)
        st.success(f"{len(new_lines)} 行追加されました")
    else:
        st.warning("認識できる構文が見つかりませんでした")

# --- 表示 ---
for line in st.session_state.ladder:
    diagram = " ― ".join([f"[{e['type']}] {e['label']} ({e['state']})" for e in line["elements"]])
    st.markdown(f"**ライン {line['line']}**")
    st.code(diagram, language="text")
