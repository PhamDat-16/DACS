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
    '--remote-debugging-port=9448',
    '--user-data-dir=d:\\smart-parking-system\\.edge_vip_chk',
    'about:blank'
], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(2.0)

async def test_vip():
    try:
        with urllib.request.urlopen('http://127.0.0.1:9448/json') as r:
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
            
            # Login as Admin
            await ws.send(json.dumps({
                'id': 4,
                'method': 'Runtime.evaluate',
                'params': {'expression': 'document.getElementById("btn-quick-admin").click()'}
            }))
            await asyncio.sleep(2.0)
            
            # Switch to Barrier Tab
            await ws.send(json.dumps({
                'id': 5,
                'method': 'Runtime.evaluate',
                'params': {
                    'returnByValue': True,
                    'expression': '''
                    (function() {
                        const buttons = Array.from(document.querySelectorAll("button"));
                        const barBtn = buttons.find(b => b.innerText.includes("Trạm Barrier"));
                        if (barBtn) barBtn.click();
                        
                        const inputs = Array.from(document.querySelectorAll("input"));
                        const barInput = inputs.find(i => i.value && (i.value.includes("51K") || i.value.includes("51F") || i.value.includes("30")));
                        if (barInput) {
                            barInput.value = "30H-999.99";
                            barInput.dispatchEvent(new Event("input"));
                        }
                        return { has_input: !!barInput };
                    })()
                    '''
                }
            }))
            await asyncio.sleep(1.0)
            
            # Check gate status text
            await ws.send(json.dumps({
                'id': 6,
                'method': 'Runtime.evaluate',
                'params': {
                    'returnByValue': True,
                    'expression': '''
                    (function() {
                        const textEl = Array.from(document.querySelectorAll("span")).find(s => s.innerText.includes("Thẻ Cư Dân VIP"));
                        return { vip_text: textEl ? textEl.innerText : null };
                    })()
                    '''
                }
            }))
            
            # Take screenshot of VIP Recognition at Gate
            await ws.send(json.dumps({'id': 7, 'method': 'Page.captureScreenshot'}))
            
            start = time.time()
            while time.time() - start < 10:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    data = json.loads(msg)
                    if data.get('id') == 6:
                        print("GATE VIP TEXT:", data.get('result', {}).get('result', {}).get('value'))
                    elif data.get('id') == 7:
                        img_b64 = data.get('result', {}).get('data')
                        if img_b64:
                            with open(r'C:\Users\LENOVO\.gemini\antigravity\brain\601e0b20-16bd-443a-b67d-50412978d4fc\gate_vip_recognized.png', 'wb') as f:
                                f.write(base64.b64decode(img_b64))
                            print("Saved gate_vip_recognized.png")
                            break
                except asyncio.TimeoutError:
                    pass
    finally:
        proc.kill()

asyncio.run(test_vip())

