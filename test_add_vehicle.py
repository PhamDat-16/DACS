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
USER_DATA = r"d:\smart-parking-system\.edge_test_user_data"

proc = subprocess.Popen([
    EDGE_PATH,
    '--headless=new',
    '--no-first-run',
    '--no-default-browser-check',
    '--remote-debugging-port=9888',
    f'--user-data-dir={USER_DATA}',
    'http://localhost:8000'
], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(2.5)

async def run_test():
    try:
        with urllib.request.urlopen('http://127.0.0.1:9888/json') as r:
            targets = json.loads(r.read().decode('utf-8'))
        ws_url = targets[0]['webSocketDebuggerUrl']
        
        async with websockets.connect(ws_url) as ws:
            msg_id = 1
            async def send_cmd(method, params=None):
                nonlocal msg_id
                msg_id += 1
                payload = {'id': msg_id, 'method': method}
                if params:
                    payload['params'] = params
                await ws.send(json.dumps(payload))
                while True:
                    res = json.loads(await ws.recv())
                    if res.get('id') == msg_id:
                        return res.get('result', {})

            await send_cmd('Page.enable')
            await send_cmd('Runtime.enable')
            # Override window.alert so it doesn't block execution and records messages
            await send_cmd('Runtime.evaluate', {
                'expression': 'window.__alerts = []; window.alert = function(msg) { window.__alerts.push(msg); console.log("ALERT:", msg); };'
            })
            await send_cmd('Emulation.setDeviceMetricsOverride', {
                'width': 1366, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False
            })

            # Check if login screen is present, log in as customer
            await asyncio.sleep(1.0)
            res = await send_cmd('Runtime.evaluate', {
                'expression': '''
                (function() {
                    const emailInput = document.querySelector('input[type="email"]');
                    const passInput = document.querySelector('input[type="password"]');
                    if (emailInput && passInput) {
                        emailInput.value = 'customer@smartparking.vn';
                        emailInput.dispatchEvent(new Event('input', { bubbles: true }));
                        passInput.value = 'customer123';
                        passInput.dispatchEvent(new Event('input', { bubbles: true }));
                        const form = document.querySelector('form');
                        if (form) form.dispatchEvent(new Event('submit', { bubbles: true }));
                        return "logged_in";
                    }
                    return "already_in_app";
                })()
                ''',
                'returnByValue': True
            })
            print("Login action:", res)
            await asyncio.sleep(2.0)

            # Navigate to 'cust-vehicles' if not there
            nav_res = await send_cmd('Runtime.evaluate', {
                'expression': '''
                (function() {
                    // Navigate to cust-vehicles tab
                    const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Phương tiện'));
                    if (btn) btn.click();
                    return "clicked_vehicles_tab";
                })()
                ''',
                'returnByValue': True
            })
            print("Nav action:", nav_res)
            await asyncio.sleep(1.0)

            # Click open add vehicle modal
            open_modal = await send_cmd('Runtime.evaluate', {
                'expression': '''
                (function() {
                    const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Thêm phương tiện') || b.textContent.includes('Add Vehicle'));
                    if (btn) {
                        btn.click();
                        return "clicked_add_vehicle_btn";
                    }
                    return "btn_not_found";
                })()
                ''',
                'returnByValue': True
            })
            print("Open modal:", open_modal)
            await asyncio.sleep(1.0)

            # Fill in the form
            fill_res = await send_cmd('Runtime.evaluate', {
                'expression': '''
                (function() {
                    const modal = document.querySelector('.bg-white.rounded-3xl');
                    if (!modal) return "modal_not_found";
                    
                    const inputs = modal.querySelectorAll('input');
                    const select = modal.querySelector('select');
                    
                    // inputs[0]: license plate
                    // select: type
                    // inputs[1]: brand
                    // inputs[2]: model
                    // inputs[3]: color
                    
                    if (inputs[0]) {
                        inputs[0].value = '51G-999.88';
                        inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    if (select) {
                        select.value = 'Car';
                        select.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                    if (inputs[1]) {
                        inputs[1].value = 'Toyota';
                        inputs[1].dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    if (inputs[2]) {
                        inputs[2].value = 'Camry 2.5Q';
                        inputs[2].dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    if (inputs[3]) {
                        inputs[3].value = 'Đen Ánh Kim';
                        inputs[3].dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    
                    return {
                        plate: inputs[0] ? inputs[0].value : null,
                        type: select ? select.value : null,
                        brand: inputs[1] ? inputs[1].value : null,
                        model: inputs[2] ? inputs[2].value : null,
                        color: inputs[3] ? inputs[3].value : null
                    };
                })()
                ''',
                'returnByValue': True
            })
            print("Filled form:", fill_res)
            await asyncio.sleep(1.0)

            # Submit the form
            submit_res = await send_cmd('Runtime.evaluate', {
                'expression': '''
                (function() {
                    const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Lưu phương tiện'));
                    if (submitBtn) {
                        submitBtn.click();
                        return "clicked_save";
                    }
                    return "submit_btn_not_found";
                })()
                ''',
                'returnByValue': True
            })
            print("Submit action:", submit_res)
            await asyncio.sleep(1.5)

            # Check alerts & verify vehicle in list
            verify_res = await send_cmd('Runtime.evaluate', {
                'expression': '''
                (function() {
                    const alerts = window.__alerts || [];
                    const bodyText = document.body.innerText;
                    const foundPlate = bodyText.includes('51G-999.88');
                    const foundBrand = bodyText.includes('Toyota Camry 2.5Q');
                    return {
                        alerts: alerts,
                        foundPlate: foundPlate,
                        foundBrand: foundBrand
                    };
                })()
                ''',
                'returnByValue': True
            })
            print("Verification result:", json.dumps(verify_res, ensure_ascii=False, indent=2))

            # Take screenshot
            ss = await send_cmd('Page.captureScreenshot', {'format': 'png'})
            artifact_path = r"C:\Users\LENOVO\.gemini\antigravity\brain\601e0b20-16bd-443a-b67d-50412978d4fc\customer_add_vehicle_verified.png"
            with open(artifact_path, 'wb') as f:
                f.write(base64.b64decode(ss['data']))
            print(f"Screenshot saved to {artifact_path}")

    finally:
        proc.kill()

asyncio.run(run_test())
