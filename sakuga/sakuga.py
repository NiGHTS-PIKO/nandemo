# -*- coding: utf-8 -*-
import streamlit as st
import re
from graphviz import Digraph
import cairosvg
import tempfile
import os

# タイトルと説明
st.title("🧠 日本語入力による自動作図ツール（Graphviz + CairoSVG）")
st.markdown("自然な日本語で接続関係を記述するだけで、構造図を自動生成し、PNGやPDFで保存できます。")

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
        dot = Digraph(format='svg')
        dot.attr(rankdir=rankdir, fontname="MS Gothic")
        dot.attr('node', shape='box', style='rounded', fontname="MS Gothic")

        for src, dst in edges:
            dot.edge(src.strip(), dst.strip())

        # プレビュー表示
        st.graphviz_chart(dot)

        # SVGデータを取得
        svg_data = dot.pipe(format='svg')

        # 一時ファイルに保存してダウンロードリンクを表示
        with tempfile.TemporaryDirectory() as tmpdirname:
            if export_png:
                png_path = os.path.join(tmpdirname, "graph.png")
                cairosvg.svg2png(bytestring=svg_data, write_to=png_path)
                with open(png_path, "rb") as f:
                    st.download_button("⬇️ PNG形式でダウンロード", f, "graph.png", "image/png")

            if export_pdf:
                pdf_path = os.path.join(tmpdirname, "graph.pdf")
                cairosvg.svg2pdf(bytestring=svg_data, write_to=pdf_path)
                with open(pdf_path, "rb") as f:
                    st.download_button("⬇️ PDF形式でダウンロード", f, "graph.pdf", "application/pdf")

        if not export_png and not export_pdf:
            st.info("💡 PNGまたはPDFのいずれかを選択すると、ダウンロードボタンが表示されます。")
