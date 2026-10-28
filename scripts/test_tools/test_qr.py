import subprocess
import time
import urllib.request
import json
import asyncio
import websockets
import base64
import sys

sys.stdout.reconfigure(encoding='utf-8')

proc = subprocess.Popen([
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '--headless=new',
    '--no-first-run',
    '--no-default-browser-check',
    '--remote-debugging-port=9333',
    '--user-data-dir=d:\\smart-parking-system\\.edge_qr_test',
    'http://localhost:8000'
], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(2)

async def test_booking_qr():
    try:
        with urllib.request.urlopen('http://127.0.0.1:9333/json') as r:
            targets = json.loads(r.read().decode('utf-8'))
        ws_url = targets[0]['webSocketDebuggerUrl']
        
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Runtime.enable'}))
            await ws.send(json.dumps({'id': 2, 'method': 'Page.enable'}))
            await ws.send(json.dumps({
                'id': 3,
                'method': 'Emulation.setDeviceMetricsOverride',
                'params': {'width': 1280, 'height': 850, 'deviceScaleFactor': 1, 'mobile': False}
            }))
            
            await asyncio.sleep(2.0)
            
            # Login via Quick Admin button
            await ws.send(json.dumps({
                'id': 4,
                'method': 'Runtime.evaluate',
                'params': {'expression': 'document.getElementById("btn-quick-admin").click()'}
            }))
            await asyncio.sleep(2.0)
            
            # Select an available slot
            await ws.send(json.dumps({
                'id': 5,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': 'document.querySelectorAll(".slot-cell")[0].click()'
                }
            }))
            await asyncio.sleep(1.0)
            
            # Open booking modal
            await ws.send(json.dumps({
                'id': 6,
                'method': 'Runtime.evaluate',
                'params': {'expression': 'document.getElementById("btn-open-booking-modal").click()'}
            }))
            await asyncio.sleep(1.0)
            
            # Click Confirm Booking
            await ws.send(json.dumps({
                'id': 7,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': '''
                    const buttons = Array.from(document.querySelectorAll("button"));
                    const confirmBtn = buttons.find(b => b.innerText.includes("Xác Nhận Đặt Chỗ"));
                    if (confirmBtn) confirmBtn.click();
                    '''
                }
            }))
            await asyncio.sleep(1.5)
            
            # Check QR image and decoded data
            await ws.send(json.dumps({
                'id': 8,
                'method': 'Runtime.evaluate',
                'params': {
                    'returnByValue': True,
                    'expression': '({ qr_src: document.querySelector("img[alt=\'QR Code\']") ? document.querySelector("img[alt=\'QR Code\']").src : null, has_modal: !!document.querySelector(".backdrop-blur-sm") })'
                }
            }))
            
            start = time.time()
            while time.time() - start < 5:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    data = json.loads(msg)
                    if data.get('id') == 8:
                        val = data.get('result', {}).get('result', {}).get('value')
                        print('QR RESULT:', json.dumps(val, indent=2))
                        break
                except asyncio.TimeoutError:
                    break
                    
            # Capture QR modal screenshot
            await ws.send(json.dumps({'id': 9, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
            start = time.time()
            while time.time() - start < 5:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    data = json.loads(msg)
                    if data.get('id') == 9:
                        img_data = base64.b64decode(data['result']['data'])
                        with open('d:\\smart-parking-system\\qr_booking_modal.png', 'wb') as f:
                            f.write(img_data)
                        print('QR MODAL SCREENSHOT SAVED, size:', len(img_data))
                        break
                except asyncio.TimeoutError:
                    break
    finally:
        proc.terminate()

asyncio.run(test_booking_qr())
