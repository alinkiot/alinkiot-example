#!/usr/bin/env python3
"""高速公路边坡监测大盘 · 本地静态服务 + 数据接口
用法：
    python3 server.py            # 默认端口 8080
    python3 server.py 9000       # 指定端口
访问：
    http://127.0.0.1:<port>/index.html      总览大盘
    http://127.0.0.1:<port>/index_3D.html   三维地形
接口：
    GET /api/dashboard                       返回大盘所需全部数据（读取 data/dashboard.json）
"""
import http.server
import socketserver
import json
import os
import sys
import webbrowser

# 以本脚本所在目录为站点根目录
ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ROOT, "data", "dashboard.json")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def _send_json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        # 数据接口：从本地 JSON 文件读取后返回
        if self.path.split("?")[0] == "/api/dashboard":
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._send_json({"code": 200, "message": "ok", "data": data})
            except FileNotFoundError:
                self._send_json({"code": 404, "message": f"data file not found: {DATA_FILE}"}, 404)
            except json.JSONDecodeError as e:
                self._send_json({"code": 500, "message": f"invalid json: {e}"}, 500)
            return
        # 其余走静态文件
        return super().do_GET()

    def end_headers(self):
        # 开发期禁用缓存，避免改了页面刷新看不到
        if not self.path.split("?")[0].startswith("/api/"):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main():
    os.chdir(ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        url = f"http://127.0.0.1:{PORT}/index.html"
        print(f"站点根目录: {ROOT}")
        print(f"服务已启动: {url}")
        print(f"三维页面:   http://127.0.0.1:{PORT}/index_3D.html")
        print("按 Ctrl+C 停止")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止")


if __name__ == "__main__":
    main()
