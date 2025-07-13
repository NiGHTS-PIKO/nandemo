# -*- coding: utf-8 -*-
import streamlit as st
import re
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import tempfile
import os
from pathlib import Path

# ✅ 日本語フォントの設定（Path(__file__).parent を使って絶対パスを取得）
base_dir = Path(__file__).parent
font_path = base_dir / "fonts" / "ipaexg.ttf"

st.text(f"📁 フォントパス: {font_path}")
st.text(f"✅ 存在する？: {font_path.exists()}")

if font_path.exists():
    font_prop = fm.FontProperties(fname=str(font_path))
    font_name = font_prop.get_name()
    plt.rcParams['font.family'] = font_name
    st.text(f"📝 使用フォント名: {font_name}")
else:
    font_prop = None
    font_name = None
    st.warning("⚠️ IPAexフォントが見つかりません。文字化けの可能性があります。")

# タイトルと説明
st.title("🧠 日本語入力による自動作図ツール（networkx + matplotlib）")
st.markdown("自然な日本語で接続関係を記述するだけで、構造図を自動生成し、PNGやPDF形式で保存できます。")

# 使い方の説明（折りたたみ）
with st.expander("📘 使い方を見る"):
    st.markdown("""
このツールでは、日本語の文章をもとに構造図（接続図）を自動で作成し、PNGやPDF形式で保存できます。

### 🔤 入力例：
モーターは電源に接続される  
スイッチはモーターに接続される

上記のように、「〇〇は△△に接続される」という形式で複数行入力してください。

### ▶️ 操作手順：
1. 下のテキストボックスに接続関係を入力します。
2. 図の向きを選択します（横向き or 縦向き）。
3. 出力形式（PNG / PDF）を選びます。
4. 「図を生成」ボタンを押します。
5. 下に構造図が表示され、選んだ形式でダウンロードできます。
""")

# 入力
user_input = st.text_area("✏️ 接続関係を日本語で入力（複数行可）", height=200)

# 図の向き
layout_direction = st.radio("📐 図の向きを選択してください", ("左から右（横向き）", "上から下（縦向き）"))
horizontal = layout_direction == "左から右（横向き）"

# 出力形式
export_png = st.checkbox("PNG形式で保存")
export_pdf = st.checkbox("PDF形式で保存")

# 図を生成
if st.button("📊 図を生成"):
    pattern = re.compile(r"(.+?)は(.+?)に接続される")
    edges = pattern.findall(user_input)

    if not edges:
        st.warning("⚠️ 接続関係が見つかりませんでした。形式を確認してください。")
    else:
        G = nx.DiGraph()
        for src, dst in edges:
            G.add_edge(src.strip(), dst.strip())

        pos = nx.spring_layout(G, seed=42) if not horizontal else nx.shell_layout(G)

        fig, ax = plt.subplots(figsize=(6, 4))
        nx.draw(G, pos, with_labels=True, arrows=True,
                node_color='lightblue', edge_color='gray',
                node_size=2000, font_size=10,
                font_family=font_name if font_name else None,
                ax=ax)

        st.pyplot(fig)

        with tempfile.TemporaryDirectory() as tmpdir:
            if export_png:
                png_path = os.path.join(tmpdir, "graph.png")
                fig.savefig(png_path, format="png", bbox_inches='tight')
                with open(png_path, "rb") as f:
                    st.download_button("⬇️ PNG形式でダウンロード", f, "graph.png", "image/png")

            if export_pdf:
                pdf_path = os.path.join(tmpdir, "graph.pdf")
                fig.savefig(pdf_path, format="pdf", bbox_inches='tight')
                with open(pdf_path, "rb") as f:
                    st.download_button("⬇️ PDF形式でダウンロード", f, "graph.pdf", "application/pdf")

        if not export_png and not export_pdf:
            st.info("💡 PNGまたはPDFのいずれかを選択すると、ダウンロードボタンが表示されます。")
