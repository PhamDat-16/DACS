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
    '--remote-debugging-port=9444',
    '--user-data-dir=d:\\smart-parking-system\\.edge_pay_test',
    'about:blank'
], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(2.0)

async def test_all():
    try:
        with urllib.request.urlopen('http://127.0.0.1:9444/json') as r:
            targets = json.loads(r.read().decode('utf-8'))
        
        # Tìm target thích hợp
        ws_url = targets[0]['webSocketDebuggerUrl']
        
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Runtime.enable'}))
            await ws.send(json.dumps({'id': 2, 'method': 'Page.enable'}))
            await ws.send(json.dumps({
                'id': 3,
                'method': 'Emulation.setDeviceMetricsOverride',
                'params': {'width': 1280, 'height': 850, 'deviceScaleFactor': 1, 'mobile': False}
            }))
            
            # Navigate explicitly to localhost:8000
            await ws.send(json.dumps({'id': 100, 'method': 'Page.navigate', 'params': {'url': 'http://localhost:8000'}}))
            await asyncio.sleep(2.5)
            
            # Quick login
            await ws.send(json.dumps({
                'id': 4,
                'method': 'Runtime.evaluate',
                'params': {'expression': 'document.getElementById("btn-quick-admin").click()'}
            }))
            await asyncio.sleep(2.0)
            
            # Check for JS errors
            await ws.send(json.dumps({
                'id': 5,
                'method': 'Runtime.evaluate',
                'params': {
                    'returnByValue': True,
                    'expression': '({ last_err: window.__last_error, vue_err: window.__vue_error, mount_err: window.__mount_error })'
                }
            }))
            
            # Test Find My Car
            await ws.send(json.dumps({
                'id': 6,
                'method': 'Runtime.evaluate',
                'params': {
                    'returnByValue': True,
                    'expression': '''
                    (function() {
                        const inputs = Array.from(document.querySelectorAll("input"));
                        const findInput = inputs.find(i => i.placeholder && i.placeholder.includes("Nhập biển số"));
                        if (findInput) {
                            findInput.value = "51F-889.92";
                            findInput.dispatchEvent(new Event("input"));
                        }
                        const buttons = Array.from(document.querySelectorAll("button"));
                        const findBtn = buttons.find(b => b.innerText.includes("Tìm xe"));
                        if (findBtn) findBtn.click();
                        return { has_input: !!findInput, has_btn: !!findBtn };
                    })()
                    '''
                }
            }))
            await asyncio.sleep(1.5)
            
            # Switch to Tab 4 (Bookings) and click "Thanh toán"
            await ws.send(json.dumps({
                'id': 7,
                'method': 'Runtime.evaluate',
                'params': {
                    'returnByValue': True,
                    'expression': '''
                    (function() {
                        const navBtns = Array.from(document.querySelectorAll("nav button"));
                        const tabBtn = navBtns.find(b => b.innerText.includes("Vé & Đặt Chỗ"));
                        if (tabBtn) tabBtn.click();
                        return { clicked_tab: !!tabBtn };
                    })()
                    '''
                }
            }))
            await asyncio.sleep(1.0)
            
            # Click the "Thanh toán" button on the first unpaid booking
            await ws.send(json.dumps({
                'id': 8,
                'method': 'Runtime.evaluate',
                'params': {
                    'returnByValue': True,
                    'expression': '''
                    (function() {
                        const buttons = Array.from(document.querySelectorAll("button"));
                        const payBtn = buttons.find(b => b.innerText.includes("Thanh toán") && !b.innerText.includes("Xác Nhận"));
                        if (payBtn) payBtn.click();
                        return { clicked_pay: !!payBtn };
                    })()
                    '''
                }
            }))
            await asyncio.sleep(1.5)
            
            # Check payment modal content
            await ws.send(json.dumps({
                'id': 9,
                'method': 'Runtime.evaluate',
                'params': {
                    'returnByValue': True,
                    'expression': '''
                    (function() {
                        const vietQrImg = document.querySelector("img[alt='VietQR Napas 247']");
                        return {
                            has_vietqr: !!vietQrImg,
                            qr_src: vietQrImg ? vietQrImg.src : null
                        };
                    })()
                    '''
                }
            }))
            
            # Take screenshot of Payment Modal
            await ws.send(json.dumps({'id': 10, 'method': 'Page.captureScreenshot'}))
            
            # Click "Xác Nhận Đã Thanh Toán"
            await ws.send(json.dumps({
                'id': 11,
                'method': 'Runtime.evaluate',
                'params': {
                    'returnByValue': True,
                    'expression': '''
                    (function() {
                        const buttons = Array.from(document.querySelectorAll("button"));
                        const confirmBtn = buttons.find(b => b.innerText.includes("Xác Nhận Đã Thanh Toán"));
                        if (confirmBtn) confirmBtn.click();
                        return { clicked_confirm: !!confirmBtn };
                    })()
                    '''
                }
            }))
            await asyncio.sleep(1.5)
            
            # Click "In Biên Lai"
            await ws.send(json.dumps({
                'id': 12,
                'method': 'Runtime.evaluate',
                'params': {
                    'returnByValue': True,
                    'expression': '''
                    (function() {
                        const buttons = Array.from(document.querySelectorAll("button"));
                        const receiptBtn = buttons.find(b => b.innerText.includes("In Biên Lai"));
                        if (receiptBtn) receiptBtn.click();
                        return { clicked_receipt: !!receiptBtn };
                    })()
                    '''
                }
            }))
            await asyncio.sleep(1.5)
            
            # Take screenshot of Receipt Modal
            await ws.send(json.dumps({'id': 13, 'method': 'Page.captureScreenshot'}))
            
            start = time.time()
            results = {}
            while time.time() - start < 15:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    data = json.loads(msg)
                    msg_id = data.get('id')
                    if msg_id in [5, 6, 7, 8, 9, 11, 12]:
                        results[msg_id] = data.get('result', {}).get('result', {}).get('value')
                        print(f"ID {msg_id}:", results[msg_id])
                    elif msg_id == 10:
                        img_b64 = data.get('result', {}).get('data')
                        if img_b64:
                            with open(r'C:\Users\LENOVO\.gemini\antigravity\brain\601e0b20-16bd-443a-b67d-50412978d4fc\payment_modal_screenshot.png', 'wb') as f:
                                f.write(base64.b64decode(img_b64))
                            print("Saved payment_modal_screenshot.png")
                    elif msg_id == 13:
                        img_b64 = data.get('result', {}).get('data')
                        if img_b64:
                            with open(r'C:\Users\LENOVO\.gemini\antigravity\brain\601e0b20-16bd-443a-b67d-50412978d4fc\receipt_modal_screenshot.png', 'wb') as f:
                                f.write(base64.b64decode(img_b64))
                            print("Saved receipt_modal_screenshot.png")
                            break
                except asyncio.TimeoutError:
                    pass
                    
            print("ALL COMPLETED!")
    finally:
        proc.kill()

asyncio.run(test_all())
