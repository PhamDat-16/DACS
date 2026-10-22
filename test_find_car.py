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
    '--disable-features=msFirstRunExperience,msEdgeSync',
    '--remote-debugging-port=9445',
    '--user-data-dir=d:\\smart-parking-system\\.edge_map_test',
    'about:blank'
], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(2.0)

async def test_map_find():
    try:
        with urllib.request.urlopen('http://127.0.0.1:9445/json') as r:
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
            
            await ws.send(json.dumps({'id': 100, 'method': 'Page.navigate', 'params': {'url': 'http://localhost:8000'}}))
            await asyncio.sleep(2.5)
            
            # Quick login
            await ws.send(json.dumps({
                'id': 4,
                'method': 'Runtime.evaluate',
                'params': {'expression': 'document.getElementById("btn-quick-admin").click()'}
            }))
            await asyncio.sleep(2.0)
            
            # Find My Car for 51F-889.92
            await ws.send(json.dumps({
                'id': 5,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': '''
                    const inputs = Array.from(document.querySelectorAll("input"));
                    const findInput = inputs.find(i => i.placeholder && i.placeholder.includes("Nhập biển số"));
                    if (findInput) {
                        findInput.value = "51F-889.92";
                        findInput.dispatchEvent(new Event("input"));
                    }
                    const buttons = Array.from(document.querySelectorAll("button"));
                    const findBtn = buttons.find(b => b.innerText.includes("Tìm xe"));
                    if (findBtn) findBtn.click();
                    '''
                }
            }))
            await asyncio.sleep(2.0)
            
            # Capture screenshot
            await ws.send(json.dumps({'id': 6, 'method': 'Page.captureScreenshot'}))
            
            start = time.time()
            while time.time() - start < 10:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    data = json.loads(msg)
                    if data.get('id') == 6:
                        img_b64 = data.get('result', {}).get('data')
                        if img_b64:
                            with open(r'C:\Users\LENOVO\.gemini\antigravity\brain\601e0b20-16bd-443a-b67d-50412978d4fc\find_my_car_screenshot.png', 'wb') as f:
                                f.write(base64.b64decode(img_b64))
                            print("Saved find_my_car_screenshot.png")
                            break
                except asyncio.TimeoutError:
                    pass
    finally:
        proc.kill()

asyncio.run(test_map_find())

