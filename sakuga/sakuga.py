# -*- coding: utf-8 -*-
import streamlit as st
import re
from graphviz import Digraph

# タイトルと説明
st.title("🧠 日本語入力による自動作図ツール（SVG対応）")
st.markdown("自然な日本語で接続関係を記述するだけで、構造図を自動生成し、SVG形式で保存できます。")

# 入力ボックス
user_input = st.text_area("✏️ 接続関係を日本語で入力（複数行可）", height=200)

# 図の向き選択
layout_direction = st.radio(
    "📐 図の向きを選択してください",
    ("左から右（横向き）", "上から下（縦向き）")
)
rankdir = "LR" if layout_direction == "左から右（横向き）" else "TB"

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

        # ダウンロードボタンを表示
        st.download_button(
            label="⬇️ SVG形式でダウンロード",
            data=svg_data,
            file_name="graph.svg",
            mime="image/svg+xml"
        )
