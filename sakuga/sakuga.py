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
    3. 「図を生成（プレビュー）」ボタンを押します。
    4. 図を確認してから、保存形式を選んで「ファイルを保存」ボタンを押します。

    ⚠️ 文の形式が正しくない場合は、図が生成されませんのでご注意ください。
    """)

# 入力ボックス
user_input = st.text_area("✏️ 接続関係を日本語で入力（複数行可）", height=200)

# 図の向き選択
layout_direction = st.radio(
    "📐 図の向きを選択してください",
    ("左から右（横向き）", "上から下（縦向き）")
)
rankdir = "LR" if layout_direction == "左から右（横向き）" else "TB"

# 正規表現パターン
pattern = re.compile(r"(.+?)は(.+?)に接続される")

# 図を生成（プレビュー）
if st.button("📊 図を生成（プレビュー）"):
    edges = pattern.findall(user_input)
    if not edges:
        st.warning("⚠️ 接続関係が見つかりませんでした。形式を確認してください。")
    else:
        dot = Digraph(format='png')
        dot.attr(rankdir=rankdir, fontname="MS Gothic")
        dot.attr('node', shape='box', style='rounded', fontname="MS Gothic")
        for src, dst in edges:
            dot.edge(src.strip(), dst.strip())

        st.graphviz_chart(dot)
        st.session_state["dot"] = dot  # セッションに保存

# 保存処理（プレビュー後に表示）
if "dot" in st.session_state:
    st.markdown("💾 出力形式を選んで保存してください")
    export_png = st.checkbox("PNG形式で保存")
    export_pdf = st.checkbox("PDF形式で保存")

    if st.button("⬇️ ファイルを保存"):
        with tempfile.TemporaryDirectory() as tmpdirname:
            base_path = os.path.join(tmpdirname, "graph")
            dot = st.session_state["dot"]

            if export_png:
                png_path = dot.render(base_path, format='png', cleanup=False)
                with open(png_path, "rb") as f:
                    st.download_button("PNG形式でダウンロード", f, "graph.png", "image/png")

            if export_pdf:
                pdf_path = dot.render(base_path, format='pdf', cleanup=False)
                with open(pdf_path, "rb") as f:
                    st.download_button("PDF形式でダウンロード", f, "graph.pdf", "application/pdf")

        if not export_png and not export_pdf:
            st.info("💡 PNGまたはPDFのいずれかを選択してください。")
