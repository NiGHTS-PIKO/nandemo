# -*- coding: utf-8 -*-
import streamlit as st
import re
from graphviz import Digraph
import tempfile
import os

# タイトルと説明
st.title("🧠 日本語入力による自動作図ツール")
st.markdown("自然な日本語で接続関係を記述するだけで、構造図を自動生成します。")

# 使い方の説明（折りたたみ可能）
with st.expander("📘 使い方を見る"):
    st.markdown("""
    このツールでは、日本語の文章をもとに構造図（接続図）を自動で作成できます。

    ### 🔤 入力例：
    ```
    モーターは電源に接続される
    スイッチはモーターに接続される
    ```
    上記のように、「〇〇は△△に接続される」という形式で複数行入力してください。

    ### ▶️ 操作手順：
    1. 下のテキストボックスに接続関係を入力します。
    2. 図の向きを選択します（横向き or 縦向き）。
    3. 出力形式（PNG / PDF）を選びます。
    4. 「図を生成」ボタンを押します。
    5. 下に構造図が表示され、選んだ形式でダウンロードできます。
    """)

# 入力ボックス
user_input = st.text_area("✏️ 接続関係を日本語で入力（複数行可）", height=200)

# 図の向き選択
layout_direction = st.radio(
    "📐 図の向きを選択してください",
    ("左から右（横向き）", "上から下（縦向き）")
)
rankdir = "LR" if layout_direction == "左から右（横向き）" else "TB"

# 出力形式の選択
st.markdown("💾 出力形式を選択してください（複数可）")
export_png = st.checkbox("PNG形式で保存")
export_pdf = st.checkbox("PDF形式で保存")

# ボタンで処理開始
if st.button("📊 図を生成"):
    # ノードとエッジの抽出
    pattern = re.compile(r"(.+?)は(.+?)に接続される")
    edges = pattern.findall(user_input)

    if not edges:
        st.warning("⚠️ 接続関係が見つかりませんでした。形式を確認してください。")
    else:
        # Graphvizオブジェクトの作成
        dot = Digraph(format='png')
        dot.attr(rankdir=rankdir, fontname="MS Gothic")
        dot.attr('node', shape='box', style='rounded', fontname="MS Gothic")

        for src, dst in edges:
            dot.edge(src.strip(), dst.strip())

        # 表示
        st.graphviz_chart(dot)

        # 一時ファイルに保存してダウンロードリンクを表示
        with tempfile.TemporaryDirectory() as tmpdirname:
            if export_png:
                dot.render(filename="graph", directory=tmpdirname, format="png", cleanup=True)
                png_path = os.path.join(tmpdirname, "graph.png")
                with open(png_path, "rb") as f:
                    st.download_button("⬇️ PNG形式でダウンロード", f, "graph.png", "image/png")

            if export_pdf:
                dot.render(filename="graph", directory=tmpdirname, format="pdf", cleanup=True)
                pdf_path = os.path.join(tmpdirname, "graph.pdf")
                with open(pdf_path, "rb") as f:
                    st.download_button("⬇️ PDF形式でダウンロード", f, "graph.pdf", "application/pdf")

        if not export_png and not export_pdf:
            st.info("💡 PNGまたはPDFのいずれかを選択すると、ダウンロードボタンが表示されます。")
