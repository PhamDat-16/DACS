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
    '--remote-debugging-port=9447',
    '--user-data-dir=d:\\smart-parking-system\\.edge_diag',
    'about:blank'
], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(2.0)

async def test_diag():
    try:
        with urllib.request.urlopen('http://127.0.0.1:9447/json') as r:
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
            
            # Click quick admin
            await ws.send(json.dumps({
                'id': 4,
                'method': 'Runtime.evaluate',
                'params': {'returnByValue': True, 'expression': 'document.getElementById("btn-quick-admin") ? "found quick admin" : "no btn-quick-admin"'}
            }))
            
            await ws.send(json.dumps({
                'id': 5,
                'method': 'Runtime.evaluate',
                'params': {'expression': 'document.getElementById("btn-quick-admin").click()'}
            }))
            await asyncio.sleep(1.5)
            
            # Check nav buttons
            await ws.send(json.dumps({
                'id': 6,
                'method': 'Runtime.evaluate',
                'params': {
                    'returnByValue': True,
                    'expression': 'Array.from(document.querySelectorAll("button")).map(b => b.innerText.trim()).filter(Boolean)'
                }
            }))
            
            start = time.time()
            while time.time() - start < 8:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    data = json.loads(msg)
                    msg_id = data.get('id')
                    if msg_id in [4, 6]:
                        print(f"ID {msg_id}:", data.get('result', {}).get('result', {}).get('value'))
                except asyncio.TimeoutError:
                    pass
    finally:
        proc.kill()

asyncio.run(test_diag())

