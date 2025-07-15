import streamlit as st

st.set_page_config(page_title="ラダー図ビューア", layout="centered")
st.title("🪜 ラダー図ビューア（表示専用）")

# --- ラダー図データの初期化 ---
if "ladder" not in st.session_state:
    st.session_state.ladder = []

# --- ライン追加 ---
if st.button("➕ ラダーラインを追加"):
    new_line = {"line": len(st.session_state.ladder)+1, "elements": []}
    st.session_state.ladder.append(new_line)

# --- ライン表示と要素追加UI ---
for line in st.session_state.ladder:
    with st.expander(f"🧩 ライン {line['line']} の編集", expanded=True):
        # 要素入力（接点・コイルなど）
        col1, col2 = st.columns([2, 1])
        with col1:
            new_element = st.text_input("要素名（例：X0 / Y1）", key=f"element_{line['line']}")
        with col2:
            elem_type = st.selectbox("タイプ", ["接点 (X)", "コイル (Y)"], key=f"type_{line['line']}")
        if st.button("追加", key=f"add_{line['line']}") and new_element.strip():
            line["elements"].append({
                "type": "X" if "接点" in elem_type else "Y",
                "label": new_element.strip()
            })

        # 表示（水平論理回路イメージ）
        st.markdown("**論理構成図：**")
        diagram = " ― ".join([f"[{e['type']}] {e['label']}" for e in line["elements"]]) or "（未入力）"
        st.code(diagram, language="text")
