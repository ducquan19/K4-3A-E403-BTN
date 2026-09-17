# -*- coding: utf-8 -*-
"""
VLearn Grounded Tutor - Main Launcher
Run this single command to launch backend & frontend:
    python run.py
"""

import os
import sys
import webbrowser
import threading
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
sys.path.insert(0, backend_dir)

from app import app

def open_browser(port):
    time.sleep(1.2)
    url = f"http://localhost:{port}"
    print(f"✨ Ứng dụng đã sẵn sàng! Mở trình duyệt tại: {url}")
    try:
        webbrowser.open(url)
    except Exception:
        pass

if __name__ == "__main__":
    port = 5000
    print("="*60)
    print("🎓 VLEARN GROUNDED TUTOR — NHÓM BTN (TRACK A1)")
    print("🚀 Đang khởi động Backend API & Frontend...")
    print(f"🔗 URL: http://localhost:{port}")
    print("="*60)

    # Open browser automatically in a separate thread
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()

    app.run(host="127.0.0.1", port=port, debug=False)
