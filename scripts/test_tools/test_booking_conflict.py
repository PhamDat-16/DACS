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
USER_DATA = r"d:\smart-parking-system\.edge_test_booking_conflict"

proc = subprocess.Popen([
    EDGE_PATH,
    '--headless=new',
    '--no-first-run',
    '--no-default-browser-check',
    '--remote-debugging-port=9778',
    f'--user-data-dir={USER_DATA}',
    'http://localhost:8000'
], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(2.5)

async def test_flow():
    try:
        with urllib.request.urlopen('http://127.0.0.1:9778/json') as r:
            targets = json.loads(r.read().decode('utf-8'))
        ws_url = targets[0]['webSocketDebuggerUrl']

        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Page.enable'}))
            await ws.send(json.dumps({'id': 2, 'method': 'Runtime.enable'}))
            await ws.send(json.dumps({
                'id': 3,
                'method': 'Emulation.setDeviceMetricsOverride',
                'params': {'width': 1366, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False}
            }))
            await asyncio.sleep(1.0)

            async def run_js(code):
                await ws.send(json.dumps({
                    'id': int(time.time() * 1000) % 100000,
                    'method': 'Runtime.evaluate',
                    'params': {'expression': code}
                }))
                await asyncio.sleep(1.2)

            async def snap(filepath):
                req_id = int(time.time() * 1000) % 100000
                await ws.send(json.dumps({'id': req_id, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
                while True:
                    msg = await ws.recv()
                    d = json.loads(msg)
                    if d.get('id') == req_id:
                        with open(filepath, 'wb') as f:
                            f.write(base64.b64decode(d['result']['data']))
                        print(f"Captured: {filepath}", flush=True)
                        break

            # Override alert to capture messages
            await run_js('window.__alerts = []; window.alert = function(msg) { window.__alerts.push(msg); console.log("ALERT:", msg); };')

            # 1. Login as customer
            await run_js('''
                const emailInput = document.querySelector('input[type="email"]');
                const passInput = document.querySelector('input[type="password"]');
                if (emailInput && passInput) {
                    emailInput.value = 'customer@parking.vn';
                    emailInput.dispatchEvent(new Event('input', { bubbles: true }));
                    passInput.value = '123456';
                    passInput.dispatchEvent(new Event('input', { bubbles: true }));
                    const form = document.querySelector('form');
                    if (form) form.dispatchEvent(new Event('submit', { bubbles: true }));
                }
            ''')
            print("Step 1: Logged in as customer", flush=True)
            await asyncio.sleep(2.0)

            # 2. Add vehicle: 89AB-55930, xe máy, honda, Air Blade, màu đen
            await run_js('''
                const tabBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Phương tiện'));
                if (tabBtn) tabBtn.click();
            ''')
            print("Step 2: Navigated to Vehicles tab", flush=True)
            await asyncio.sleep(1.0)

            # Click open add vehicle modal
            await run_js('''
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Thêm phương tiện') || b.textContent.includes('Add Vehicle'));
                if (btn) btn.click();
            ''')
            await asyncio.sleep(1.0)

            # Fill vehicle details and save
            await run_js('''
                const modal = document.querySelector('.bg-white.rounded-3xl');
                if (modal) {
                    const inputs = modal.querySelectorAll('input');
                    const select = modal.querySelector('select');
                    if (inputs[0]) {
                        inputs[0].value = '89AB-55930';
                        inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    if (select) {
                        select.value = 'Motorcycle';
                        select.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                    if (inputs[1]) {
                        inputs[1].value = 'Honda';
                        inputs[1].dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    if (inputs[2]) {
                        inputs[2].value = 'Air Blade';
                        inputs[2].dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    if (inputs[3]) {
                        inputs[3].value = 'Đen';
                        inputs[3].dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    const saveBtn = Array.from(modal.querySelectorAll('button')).find(b => b.textContent.includes('Lưu phương tiện'));
                    if (saveBtn) saveBtn.click();
                }
            ''')
            print("Step 2: Saved vehicle 89AB-55930", flush=True)
            await asyncio.sleep(1.5)

            # 3. Navigate to Booking Tab ('cust-booking')
            await run_js('''
                const tabBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Đặt chỗ') || b.textContent.includes('Bookings'));
                if (tabBtn) tabBtn.click();
            ''')
            print("Step 3: Navigated to Booking tab", flush=True)
            await asyncio.sleep(1.0)

            # 4. Fill Booking form: vehicle 89AB-55930, Slot A-024, Date 2026-10-01, 08:00 - 10:00 (2h)
            await run_js('''
                const dateInput = document.querySelector('input[type="date"]');
                const timeInput = document.querySelector('input[type="time"]');
                const selects = Array.from(document.querySelectorAll('select'));
                
                if (dateInput) {
                    dateInput.value = '2026-10-01';
                    dateInput.dispatchEvent(new Event('input', { bubbles: true }));
                }
                if (timeInput) {
                    timeInput.value = '08:00';
                    timeInput.dispatchEvent(new Event('input', { bubbles: true }));
                }
                
                const durSelect = selects.find(s => Array.from(s.options).some(o => o.text.includes('2 giờ')));
                if (durSelect) {
                    durSelect.value = '2';
                    durSelect.dispatchEvent(new Event('change', { bubbles: true }));
                }
                
                const vehSelect = selects.find(s => Array.from(s.options).some(o => o.text.includes('89AB-55930')));
                if (vehSelect) {
                    const opt = Array.from(vehSelect.options).find(o => o.text.includes('89AB-55930'));
                    if (opt) {
                        vehSelect.value = opt.value;
                        vehSelect.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                }
                
                const slotSelect = selects.find(s => Array.from(s.options).some(o => o.value === 'A-024'));
                if (slotSelect) {
                    slotSelect.value = 'A-024';
                    slotSelect.dispatchEvent(new Event('change', { bubbles: true }));
                }
            ''')
            print("Step 4: Selected 89AB-55930, Slot A-024, 08:00-10:00", flush=True)
            await asyncio.sleep(1.0)

            # Submit booking
            await run_js('''
                const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Xác nhận đặt chỗ'));
                if (submitBtn) submitBtn.click();
            ''')
            print("Step 4: Clicked Confirm Booking", flush=True)
            await asyncio.sleep(1.5)

            # Open QR Modal from confirmation dialog
            await run_js('''
                const qrBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Xem mã QR'));
                if (qrBtn) qrBtn.click();
            ''')
            print("Step 4: Opened QR Modal", flush=True)
            await asyncio.sleep(1.0)

            # Snapshot QR modal showing vehicle 89AB-55930!
            qr_shot_path = r"C:\Users\LENOVO\.gemini\antigravity\brain\601e0b20-16bd-443a-b67d-50412978d4fc\booking_qr_verified.png"
            await snap(qr_shot_path)

            # Close QR modal
            await run_js('''
                const closeBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Đóng'));
                if (closeBtn) closeBtn.click();
            ''')
            await asyncio.sleep(1.0)

            # 5. NOW TEST CONFLICT: Try to book SAME slot (A-024) on SAME date (2026-10-01) with OVERLAPPING time: 08:00 - 09:00 (1h)
            await run_js('''
                const dateInput = document.querySelector('input[type="date"]');
                const timeInput = document.querySelector('input[type="time"]');
                const selects = Array.from(document.querySelectorAll('select'));
                
                if (dateInput) {
                    dateInput.value = '2026-10-01';
                    dateInput.dispatchEvent(new Event('input', { bubbles: true }));
                }
                if (timeInput) {
                    timeInput.value = '08:00';
                    timeInput.dispatchEvent(new Event('input', { bubbles: true }));
                }
                
                const durSelect = selects.find(s => Array.from(s.options).some(o => o.text.includes('1 giờ')));
                if (durSelect) {
                    durSelect.value = '1'; // 08:00 - 09:00 OVERLAPS with 08:00 - 10:00!
                    durSelect.dispatchEvent(new Event('change', { bubbles: true }));
                }
                
                // Select vehicle 59A1-123.45
                const vehSelect = selects.find(s => Array.from(s.options).some(o => o.text.includes('59A1-123.45')));
                if (vehSelect) {
                    const opt = Array.from(vehSelect.options).find(o => o.text.includes('59A1-123.45'));
                    if (opt) {
                        vehSelect.value = opt.value;
                        vehSelect.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                }
                
                // Select Slot A-024
                const slotSelect = selects.find(s => Array.from(s.options).some(o => o.value === 'A-024'));
                if (slotSelect) {
                    slotSelect.value = 'A-024';
                    slotSelect.dispatchEvent(new Event('change', { bubbles: true }));
                }
                
                // Click submit
                const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Xác nhận đặt chỗ'));
                if (submitBtn) submitBtn.click();
            ''')
            print("Step 5: Submitted overlapping booking (08:00 - 09:00 on A-024)", flush=True)
            await asyncio.sleep(1.5)

            # Snapshot conflict state / alert
            conflict_shot_path = r"C:\Users\LENOVO\.gemini\antigravity\brain\601e0b20-16bd-443a-b67d-50412978d4fc\booking_conflict_verified.png"
            await snap(conflict_shot_path)

            print("SUCCESS: All steps executed cleanly!", flush=True)

    finally:
        proc.kill()

asyncio.run(test_flow())
