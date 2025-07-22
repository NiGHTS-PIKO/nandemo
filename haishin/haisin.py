import os
import shutil
import subprocess
import threading
from flask import Flask, render_template_string, send_from_directory
import tkinter as tk
from tkinter import messagebox

# 🎬 配信フォルダ名
static_dir = 'static'

# 🌐 Flaskアプリ初期化
app = Flask(__name__)
os.makedirs(static_dir, exist_ok=True)

# 🎥 ffmpeg ライブ配信構成（1秒セグメント＋最小記憶）
ffmpeg_cmd = [
    'ffmpeg',
    '-f', 'gdigrab',
    '-framerate', '10',
    '-i', 'desktop',
    '-vcodec', 'libx264',
    '-preset', 'ultrafast',
    '-tune', 'zerolatency',
    '-g', '10',
    '-pix_fmt', 'yuv420p',
    '-start_number', '0',
    '-hls_time', '1',
    '-hls_list_size', '1',
    '-hls_flags', 'delete_segments+append_list',
    '-hls_allow_cache', '0',
    '-f', 'hls',
    f'{static_dir}/playlist.m3u8'
]

# 🔧 ffmpegプロセス管理用ロックと状態
ffmpeg_process = None
ffmpeg_lock = threading.Lock()

# 🧹 staticフォルダの初期化（開始時に削除）
def clean_static_folder():
    try:
        shutil.rmtree(static_dir)
    except FileNotFoundError:
        pass
    os.makedirs(static_dir, exist_ok=True)

# 🚀 ffmpeg起動
def start_ffmpeg():
    global ffmpeg_process
    with ffmpeg_lock:
        if ffmpeg_process is None:
            ffmpeg_process = subprocess.Popen(ffmpeg_cmd)

# 🛑 ffmpeg停止
def stop_ffmpeg():
    global ffmpeg_process
    with ffmpeg_lock:
        if ffmpeg_process is not None:
            ffmpeg_process.terminate()
            ffmpeg_process = None

# 🎥 ライブ配信ページ
@app.route('/video')
def video():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ナイツ式ライブ演出</title>
        <style>
            body { background-color: black; color: white; text-align: center; font-family: sans-serif; }
            h2 { margin-top: 30px; }
            video { border: 2px solid white; width: 90%; max-width: 1080px; }
        </style>
        <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    </head>
    <body>
        <h2>VPN越しのリアルタイム・デスクトップ配信</h2>
        <video id="video" controls autoplay muted></video>
        <script>
        if (Hls.isSupported()) {
            var video = document.getElementById('video');
            var hls = new Hls({ liveDurationInfinity: true });
            hls.startPosition = -1;
            hls.loadSource('/static/playlist.m3u8');
            hls.attachMedia(video);
            hls.on(Hls.Events.MANIFEST_PARSED, function() {
                video.play();
            });
        } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
            video.src = '/static/playlist.m3u8';
            video.addEventListener('loadedmetadata', function() {
                video.play();
            });
        }
        </script>
        <p>※ Safariはネイティブ再生、Chromeはhls.js経由でライブ再生されます</p>
    </body>
    </html>
    """
    return render_template_string(html)

# 📁 ts/m3u8 ファイル配信ルート
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(static_dir, filename)

# 🖥️ GUI構成（開始／停止ボタン）
def launch_gui():
    def on_start():
        clean_static_folder()
        start_ffmpeg()
        messagebox.showinfo("配信開始", "古いセグメントを削除し、ライブ配信を開始しました")

    def on_stop():
        stop_ffmpeg()
        messagebox.showinfo("配信停止", "ライブ配信を停止しました")

    root = tk.Tk()
    root.title("ナイツ式ライブ演出 GUI")
    root.geometry("300x150")
    root.configure(bg="black")

    start_btn = tk.Button(root, text="開始", command=on_start, bg="green", fg="white", font=("sans-serif", 14))
    stop_btn = tk.Button(root, text="停止", command=on_stop, bg="red", fg="white", font=("sans-serif", 14))

    start_btn.pack(pady=20)
    stop_btn.pack(pady=10)

    root.mainloop()

# 🌍 Flaskサーバは非同期起動
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000), daemon=True).start()

# 🔘 GUI起動
launch_gui()
