import os
import shutil
import subprocess
import threading
from flask import Flask, render_template_string, send_from_directory
import tkinter as tk
from tkinter import messagebox

# 📁 出力フォルダ名
static_dir = 'static'
app = Flask(__name__)
os.makedirs(static_dir, exist_ok=True)

# 🎧 VB-CABLE用オーディオデバイス名（環境によって調整可）
AUDIO_DEVICE_NAME = "CABLE Output (VB-Audio Virtual Cable)"

# 🎥 ffmpegコマンド構成（映像＋音声）
ffmpeg_cmd = [
    'ffmpeg',
    '-f', 'dshow',
    '-i', f'audio={AUDIO_DEVICE_NAME}',    # 🔊 スピーカー出力
    '-f', 'gdigrab',
    '-framerate', '10',
    '-i', 'desktop',                        # 🎬 デスクトップ映像
    '-map', '0:a',
    '-map', '1:v',
    '-c:v', 'libx264',
    '-preset', 'ultrafast',
    '-tune', 'zerolatency',
    '-pix_fmt', 'yuv420p',
    '-g', '20',
    '-c:a', 'aac',
    '-b:a', '128k',
    '-ac', '2',
    '-ar', '44100',
    '-start_number', '0',
    '-hls_time', '5',
    '-hls_list_size', '3',
    '-hls_flags', 'delete_segments+append_list',
    '-hls_allow_cache', '0',
    '-f', 'hls',
    f'{static_dir}/playlist.m3u8'
]

# 🔧 ffmpegプロセス管理
ffmpeg_process = None
ffmpeg_lock = threading.Lock()

# 🧹 staticフォルダ初期化
def clean_static_folder():
    try:
        shutil.rmtree(static_dir)
    except FileNotFoundError:
        pass
    os.makedirs(static_dir, exist_ok=True)

# ▶️ ffmpeg起動
def start_ffmpeg():
    global ffmpeg_process
    with ffmpeg_lock:
        if ffmpeg_process is None:
            ffmpeg_process = subprocess.Popen(ffmpeg_cmd)

# ⏹️ ffmpeg停止
def stop_ffmpeg():
    global ffmpeg_process
    with ffmpeg_lock:
        if ffmpeg_process is not None:
            ffmpeg_process.terminate()
            ffmpeg_process = None

# 🌐 映像ページ（videoタグ＋hls.js）
@app.route('/video')
def video():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ナイツ式 映像＋音声ライブ</title>
        <style>
            body { background-color: black; color: white; text-align: center; font-family: sans-serif; }
            h2 { margin-top: 30px; }
            video { border: 2px solid white; width: 90%; max-width: 1080px; }
        </style>
        <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    </head>
    <body>
        <h2>デスクトップ＆音声リアルタイム配信</h2>
        <video id="video" controls autoplay></video>
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
        <p>※ 音声再生にはChromeなどでユーザー操作が必要な場合があります</p>
    </body>
    </html>
    """
    return render_template_string(html)

# 📁 セグメント配信ルート
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(static_dir, filename)

# 🖱️ GUI：開始・停止ボタン（Tkinter）
def launch_gui():
    def on_start():
        clean_static_folder()
        start_ffmpeg()
        messagebox.showinfo("配信開始", "映像＋音声のライブ配信を開始しました")

    def on_stop():
        stop_ffmpeg()
        messagebox.showinfo("配信停止", "配信を停止しました")

    root = tk.Tk()
    root.title("ナイツ式ライブ演出 GUI")
    root.geometry("320x160")
    root.configure(bg="black")

    start_btn = tk.Button(root, text="開始", command=on_start, bg="green", fg="white", font=("sans-serif", 14))
    stop_btn = tk.Button(root, text="停止", command=on_stop, bg="red", fg="white", font=("sans-serif", 14))

    start_btn.pack(pady=20)
    stop_btn.pack(pady=10)

    root.mainloop()

# 🌀 Flask 非同期起動
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000), daemon=True).start()

# 🔘 GUI起動
launch_gui()
