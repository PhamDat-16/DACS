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
    '--remote-debugging-port=9446',
    '--user-data-dir=d:\\smart-parking-system\\.edge_admin_test',
    'about:blank'
], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(2.0)

async def test_admin():
    try:
        with urllib.request.urlopen('http://127.0.0.1:9446/json') as r:
            targets = json.loads(r.read().decode('utf-8'))
        ws_url = targets[0]['webSocketDebuggerUrl']
        
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Runtime.enable'}))
            await ws.send(json.dumps({'id': 2, 'method': 'Page.enable'}))
            await ws.send(json.dumps({
                'id': 3,
                'method': 'Emulation.setDeviceMetricsOverride',
                'params': {'width': 1280, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False}
            }))
            
            await ws.send(json.dumps({'id': 100, 'method': 'Page.navigate', 'params': {'url': 'http://localhost:8000'}}))
            await asyncio.sleep(2.5)
            
            # Quick login as Admin
            await ws.send(json.dumps({
                'id': 4,
                'method': 'Runtime.evaluate',
                'params': {'expression': 'document.getElementById("btn-quick-admin").click()'}
            }))
            await asyncio.sleep(2.0)
            
            # Check for console errors
            await ws.send(json.dumps({
                'id': 5,
                'method': 'Runtime.evaluate',
                'params': {
                    'returnByValue': True,
                    'expression': '({ last_err: window.__last_error, vue_err: window.__vue_error, mount_err: window.__mount_error })'
                }
            }))
            
            # Click Tab "Doanh Thu & Quản Trị"
            await ws.send(json.dumps({
                'id': 6,
                'method': 'Runtime.evaluate',
                'params': {
                    'returnByValue': True,
                    'expression': '''
                    (function() {
                        const buttons = Array.from(document.querySelectorAll("button"));
                        const revBtn = buttons.find(b => b.innerText.includes("Doanh Thu"));
                        if (revBtn) revBtn.click();
                        return { clicked_revenue: !!revBtn };
                    })()
                    '''
                }
            }))
            await asyncio.sleep(2.0)
            
            # Take screenshot of Revenue Dashboard
            await ws.send(json.dumps({'id': 7, 'method': 'Page.captureScreenshot'}))
            
            # Test Adding a VIP resident pass
            await ws.send(json.dumps({
                'id': 8,
                'method': 'Runtime.evaluate',
                'params': {
                    'returnByValue': True,
                    'expression': '''
                    (function() {
                        const addBtn = Array.from(document.querySelectorAll("button")).find(b => b.innerText.includes("Cấp Thẻ Cư Dân"));
                        if (addBtn) addBtn.click();
                        return { clicked_add_pass: !!addBtn };
                    })()
                    '''
                }
            }))
            await asyncio.sleep(1.0)
            
            # Fill form
            await ws.send(json.dumps({
                'id': 9,
                'method': 'Runtime.evaluate',
                'params': {
                    'returnByValue': True,
                    'expression': '''
                    (function() {
                        const inputs = Array.from(document.querySelectorAll("input"));
                        const plateInput = inputs.find(i => i.placeholder && i.placeholder.includes("30H"));
                        if (plateInput) {
                            plateInput.value = "30K-123.45";
                            plateInput.dispatchEvent(new Event("input"));
                        }
                        const nameInput = inputs.find(i => i.placeholder && i.placeholder.includes("Nguyễn Văn A"));
                        if (nameInput) {
                            nameInput.value = "Nguyễn Quốc Hưng (Căn B-1802)";
                            nameInput.dispatchEvent(new Event("input"));
                        }
                        const submitBtn = Array.from(document.querySelectorAll("button")).find(b => b.innerText.includes("Kích Hoạt Thẻ VIP"));
                        if (submitBtn) submitBtn.click();
                        return { submitted: !!submitBtn };
                    })()
                    '''
                }
            }))
            await asyncio.sleep(1.5)
            
            # Switch to Barrier Tab to test VIP recognition
            await ws.send(json.dumps({
                'id': 10,
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
                            barInput.value = "30K-123.45";
                            barInput.dispatchEvent(new Event("input"));
                        }
                        return { clicked_barrier: !!barBtn };
                    })()
                    '''
                }
            }))
            await asyncio.sleep(1.5)
            
            # Take screenshot of Barrier Tab with VIP resident recognition
            await ws.send(json.dumps({'id': 11, 'method': 'Page.captureScreenshot'}))
            
            # Click Check-in
            await ws.send(json.dumps({
                'id': 12,
                'method': 'Runtime.evaluate',
                'params': {
                    'returnByValue': True,
                    'expression': '''
                    (function() {
                        const inBtn = Array.from(document.querySelectorAll("button")).find(b => b.innerText.includes("Check-in (Vào Bãi)"));
                        if (inBtn) inBtn.click();
                        return { clicked_checkin: !!inBtn };
                    })()
                    '''
                }
            }))
            await asyncio.sleep(1.0)
            
            start = time.time()
            results = {}
            while time.time() - start < 15:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    data = json.loads(msg)
                    msg_id = data.get('id')
                    if msg_id in [5, 6, 8, 9, 10, 12]:
                        results[msg_id] = data.get('result', {}).get('result', {}).get('value')
                        print(f"ID {msg_id}:", results[msg_id])
                    elif msg_id == 7:
                        img_b64 = data.get('result', {}).get('data')
                        if img_b64:
                            with open(r'C:\Users\LENOVO\.gemini\antigravity\brain\601e0b20-16bd-443a-b67d-50412978d4fc\admin_revenue_screenshot.png', 'wb') as f:
                                f.write(base64.b64decode(img_b64))
                            print("Saved admin_revenue_screenshot.png")
                    elif msg_id == 11:
                        img_b64 = data.get('result', {}).get('data')
                        if img_b64:
                            with open(r'C:\Users\LENOVO\.gemini\antigravity\brain\601e0b20-16bd-443a-b67d-50412978d4fc\barrier_vip_screenshot.png', 'wb') as f:
                                f.write(base64.b64decode(img_b64))
                            print("Saved barrier_vip_screenshot.png")
                            break
                except asyncio.TimeoutError:
                    pass
            print("TEST ADMIN REVENUE COMPLETED!")
    finally:
        proc.kill()

asyncio.run(test_admin())
