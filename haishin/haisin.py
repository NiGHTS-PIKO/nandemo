import os
import subprocess
import threading
from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)

# 📁 出力フォルダの準備
os.makedirs('static', exist_ok=True)

# 🎥 ffmpeg：3秒セグメント・低遅延ライブ構成
ffmpeg_cmd = [
    'ffmpeg',
    '-f', 'gdigrab',
    '-framerate', '10',
    '-i', 'desktop',
    '-vcodec', 'libx264',
    '-preset', 'ultrafast',
    '-tune', 'zerolatency',
    '-g', '10',                         # 10fps × 3秒 → GOP=30
    '-pix_fmt', 'yuv420p',
    '-start_number', '0',
    '-hls_time', '1',                   # 🔧 セグメント長秒
    '-hls_list_size', '1',              # 🔧 プレイリスト直近
    '-hls_flags', 'delete_segments+append_list',
    '-hls_allow_cache', '0',
    '-f', 'hls',
    'static/playlist.m3u8'
]

def start_ffmpeg():
    subprocess.Popen(ffmpeg_cmd)

# 🧵 Flaskと並行してffmpeg起動
threading.Thread(target=start_ffmpeg, daemon=True).start()

# 🌐 ライブ配信ページ（videoタグ＋hls.js補完）
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
            hls.startPosition = -1;  // 🔧 最新セグメントから開始
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

# 📁 配信ルート
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
