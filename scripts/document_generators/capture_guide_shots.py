import subprocess
import time
import urllib.request
import json
import asyncio
import websockets
import base64
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
USER_DATA = r"d:\smart-parking-system\.edge_guide_shot"

proc = subprocess.Popen([
    EDGE_PATH,
    '--headless=new',
    '--no-first-run',
    '--no-default-browser-check',
    '--remote-debugging-port=9777',
    f'--user-data-dir={USER_DATA}',
    'http://localhost:8000'
], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(2.5)

async def capture():
    try:
        with urllib.request.urlopen('http://127.0.0.1:9777/json') as r:
            targets = json.loads(r.read().decode('utf-8'))
        ws_url = targets[0]['webSocketDebuggerUrl']
        
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Page.enable'}))
            await ws.send(json.dumps({'id': 2, 'method': 'Runtime.enable'}))
            await ws.send(json.dumps({
                'id': 3,
                'method': 'Emulation.setDeviceMetricsOverride',
                'params': {'width': 1366, 'height': 820, 'deviceScaleFactor': 1, 'mobile': False}
            }))
            await asyncio.sleep(1.5)

            async def run_js(code):
                await ws.send(json.dumps({
                    'id': 100,
                    'method': 'Runtime.evaluate',
                    'params': {'expression': code}
                }))
                await asyncio.sleep(0.8)

            async def snap(filename):
                req_id = int(time.time() * 1000) % 100000
                await ws.send(json.dumps({'id': req_id, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
                while True:
                    msg = await ws.recv()
                    d = json.loads(msg)
                    if d.get('id') == req_id:
                        img_path = os.path.join(r"d:\smart-parking-system", filename)
                        with open(img_path, 'wb') as f:
                            f.write(base64.b64decode(d['result']['data']))
                        print(f"Captured: {img_path}")
                        break

            # 1. Đăng nhập Admin một chạm
            await run_js('if (document.getElementById("btn-quick-admin")) document.getElementById("btn-quick-admin").click();')
            await asyncio.sleep(2.0)

            # 2. Sơ đồ A* & bấm slot để hiện lộ trình
            await run_js('const btn = document.querySelector(".slot-cell"); if(btn) btn.click();')
            await asyncio.sleep(1.0)
            await snap('guide_map_astar.png')

            # 3. Tab Bản đồ GIS chuỗi bãi xe
            await run_js('const tabs = document.querySelectorAll("nav button"); for(const t of tabs) if(t.innerText.includes("Chuỗi Bãi")) t.click();')
            await asyncio.sleep(1.0)
            await snap('guide_city_map.png')

            # 4. Tab AI & Định Giá Động
            await run_js('const tabs = document.querySelectorAll("nav button"); for(const t of tabs) if(t.innerText.includes("Định Giá Động") || t.innerText.includes("Dự Báo")) t.click();')
            await asyncio.sleep(1.0)
            await snap('guide_ai_forecast.png')

            # 5. Tab Trạm Barrier Cổng
            await run_js('const tabs = document.querySelectorAll("nav button"); for(const t of tabs) if(t.innerText.includes("Barrier")) t.click();')
            await asyncio.sleep(1.0)
            await snap('guide_barrier.png')

            # 6. Tab Doanh Thu & Quản Trị
            await run_js('const tabs = document.querySelectorAll("nav button"); for(const t of tabs) if(t.innerText.includes("Doanh Thu")) t.click();')
            await asyncio.sleep(1.0)
            await snap('guide_revenue.png')

            # 7. Mở Modal đặt chỗ có QR
            await run_js('const tabs = document.querySelectorAll("nav button"); for(const t of tabs) if(t.innerText.includes("Sơ Đồ")) t.click();')
            await asyncio.sleep(0.5)
            await run_js('const bBtn = Array.from(document.querySelectorAll("button")).find(b => b.innerText.includes("Đặt Chỗ")); if(bBtn) bBtn.click();')
            await asyncio.sleep(1.0)
            await snap('guide_booking_qr.png')

    finally:
        proc.terminate()

asyncio.run(capture())
