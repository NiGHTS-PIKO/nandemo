import asyncio
import json
import wmi
import websockets
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

PORT = 8080          # HTTP for HTML
WS_PORT = 8888       # WebSocket for JSON
w = wmi.WMI()

# HTML with dynamic WebSocket connection for Tailnet compatibility
html_content = """
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <title>リアルタイムシステム情報</title>
  <style>
    body { font-family: 'Segoe UI', sans-serif; background: #f8f9fa; margin: 20px; }
    h1 { color: #333; }
    #status { font-weight: bold; color: #0066cc; margin-bottom: 10px; }
    table { width: 100%; border-collapse: collapse; background: #fff; margin-bottom: 20px; }
    th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
    th { background: #e9ecef; }
    #rawJson { white-space: pre-wrap; background: #eee; padding: 10px; border: 1px solid #ccc; max-height: 300px; overflow-y: scroll; font-size: 12px; }
  </style>
</head>
<body>
  <h1>🖥️ システムモニターダッシュボード</h1>
  <div id="status">🔄 接続待機中...</div>

  <table id="systemTable">
    <thead><tr><th>項目</th><th>値</th></tr></thead>
    <tbody></tbody>
  </table>

  <h2>🧪 受信したJSON（デバッグ）</h2>
  <pre id="rawJson">まだデータを受信していません...</pre>

  <script>
    const status = document.getElementById("status");
    const tableBody = document.querySelector("#systemTable tbody");
    const rawJson = document.getElementById("rawJson");

    const socketHost = window.location.hostname;
    const socket = new WebSocket("ws://" + socketHost + ":8888");

    socket.onopen = () => {
      status.textContent = "✅ WebSocket接続成功！";
    };

    socket.onmessage = (event) => {
      rawJson.textContent = event.data;

      try {
        const data = JSON.parse(event.data);
        tableBody.innerHTML = "";

        const displayOrder = [
          ["CPU_Name", "CPU名"],
          ["CPU_Load_Percent", "CPU使用率（%）"],
          ["RAM_Used_MB", "RAM使用量（MB）"],
          ["RAM_Total_MB", "RAM総容量（MB）"],
          ["RAM_Usage_Percent", "RAM使用率（%）"]
        ];

        displayOrder.forEach(([key, label]) => {
          const value = key in data ? data[key] : "—";
          const row = document.createElement("tr");
          row.innerHTML = `<td>${label}</td><td>${value}</td>`;
          tableBody.appendChild(row);
        });
      } catch (e) {
        status.textContent = "🚨 JSON解析エラー: " + e.message;
      }
    };

    socket.onerror = (err) => {
      status.textContent = "🚨 WebSocketエラー: " + err.message;
    };
  </script>
</body>
</html>
"""

# WMIセンサー取得関数
def get_wmi_data():
    data = {}
    try:
        for cpu in w.Win32_Processor():
            data["CPU_Name"] = cpu.Name
            data["CPU_Load_Percent"] = cpu.LoadPercentage
        for os in w.Win32_OperatingSystem():
            total = int(os.TotalVisibleMemorySize)
            free = int(os.FreePhysicalMemory)
            used = total - free
            data["RAM_Total_MB"] = total // 1024
            data["RAM_Used_MB"] = used // 1024
            data["RAM_Usage_Percent"] = round((used / total) * 100, 2)
        return data
    except Exception as e:
        return {"error": str(e)}

# WebSocket配信ハンドラー（v15対応：1引数）
async def send_sensor_data(websocket):
    try:
        while True:
            data = get_wmi_data()
            await websocket.send(json.dumps(data))
            await asyncio.sleep(1)
    except Exception as e:
        print("🚨 WebSocket送信エラー:", e)

# WebSocketサーバー起動
async def start_ws_server():
    async with websockets.serve(send_sensor_data, "0.0.0.0", WS_PORT):
        print(f"✅ WebSocket配信中 → ws://localhost:{WS_PORT}")
        await asyncio.Future()

# HTTP配信ハンドラー（HTML返却）
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

def start_http_server():
    print(f"🌐 HTTP表示中 → http://localhost:{PORT}")
    httpd = HTTPServer(("0.0.0.0", PORT), SimpleHandler)
    httpd.serve_forever()

# 並列起動処理
def run_servers():
    threading.Thread(target=start_http_server, daemon=True).start()
    asyncio.run(start_ws_server())

if __name__ == "__main__":
    print("🚀 統合型システム起動中...")
    run_servers()