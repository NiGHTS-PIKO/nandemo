# -*- coding: utf-8 -*-
import streamlit as st
import re
import pydot
from PIL import Image
import io

# タイトルと説明
st.title("🧠 日本語入力による自動作図ツール（pydot + PNG）")
st.markdown("自然な日本語で接続関係を記述するだけで、構造図を自動生成し、PNG形式で表示・保存できます。")

# 使い方の説明（折りたたみ）
with st.expander("📘 使い方を見る"):
    st.markdown("""
このツールでは、日本語の文章をもとに構造図（接続図）を自動で作成し、PNG形式で保存できます。

### 🔤 入力例：
モーターは電源に接続される スイッチはモーターに接続される


上記のように、「〇〇は△△に接続される」という形式で複数行入力してください。

### ▶️ 操作手順：
1. 下のテキストボックスに接続関係を入力します。
2. 図の向きを選択します（横向き or 縦向き）。
3. 「図を生成」ボタンを押します。
4. 下に構造図が表示され、PNG形式でダウンロードできます。
""")

# 入力ボックス
user_input = st.text_area("✏️ 接続関係を日本語で入力（複数行可）", height=200)

# 図の向き選択
layout_direction = st.radio(
    "📐 図の向きを選択してください",
    ("左から右（横向き）", "上から下（縦向き）")
)
rankdir = "LR" if layout_direction == "左から右（横向き）" else "TB"

# 図を生成
if st.button("📊 図を生成"):
    pattern = re.compile(r"(.+?)は(.+?)に接続される")
    edges = pattern.findall(user_input)

    if not edges:
        st.warning("⚠️ 接続関係が見つかりませんでした。形式を確認してください。")
    else:
        # DOTソースを構築
        dot_lines = [f'"{src.strip()}" -> "{dst.strip()}";' for src, dst in edges]
        dot_source = f'digraph G {{ rankdir={rankdir}; node [shape=box, style=rounded, fontname="MS Gothic"]; {" ".join(dot_lines)} }}'

        # pydotでグラフ生成
        graphs = pydot.graph_from_dot_data(dot_source)
        if graphs:
            png_data = graphs[0].create_png()
            image = Image.open(io.BytesIO(png_data))

            # 表示
            st.image(image, caption="構造図（PNG）", use_column_width=True)

            # ダウンロード
            st.download_button(
                label="⬇️ PNG形式でダウンロード",
                data=png_data,
                file_name="graph.png",
                mime="image/png"
            )
        else:
            st.error("DOTソースの解析に失敗しました。")
