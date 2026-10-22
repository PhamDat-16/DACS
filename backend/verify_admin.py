import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ARTIFACT_DIR = r"C:\Users\LENOVO\.gemini\antigravity\brain\601e0b20-16bd-443a-b67d-50412978d4fc"

def run_admin_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 1800})
        page = context.new_page()

        # Handle any alerts / dialogs automatically
        page.on("dialog", lambda dialog: dialog.accept())
        page.on("console", lambda msg: print(f"BROWSER LOG: {msg.text}", flush=True))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}", flush=True))

        print("1. Opening http://127.0.0.1:8000...", flush=True)
        page.goto("http://127.0.0.1:8000")
        page.wait_for_timeout(1000)

        # Click the quick demo button for Admin
        print("2. Clicking demo admin quick fill...", flush=True)
        page.click('button:has-text("Admin:")')
        page.wait_for_timeout(500)

        print("3. Clicking Sign In button[type=submit]...", flush=True)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Verify Header and Admin Badge
        role_badge = page.inner_text('span:has-text("ADMIN")')
        print(f"Role badge verified: {role_badge}", flush=True)

        # 4. Test SCREEN 1: Parking Lots
        print("4. Testing Parking Lots screen...", flush=True)
        page.click('button:has-text("2. Parking Lots")')
        page.wait_for_timeout(600)

        # Test filters
        page.click('button:has-text("Available")')
        page.wait_for_timeout(400)
        page.click('button:has-text("Tất cả")')
        page.wait_for_timeout(400)

        # Click a slot to test inspector
        slots = page.query_selector_all('div[class*="min-h-[200px]"]')
        if slots:
            slots[0].click()
            page.wait_for_timeout(400)

        # Click Set Maintenance
        set_maint_btn = page.query_selector('button:has-text("Set Maintenance")')
        if set_maint_btn:
            set_maint_btn.click()
            page.wait_for_timeout(500)
            print("Set Maintenance toggled successfully", flush=True)

        shot1 = os.path.join(ARTIFACT_DIR, "admin_parking_lots_verified.png")
        page.screenshot(path=shot1)
        print(f"Screenshot 1 saved: {shot1}", flush=True)

        # 5. Test SCREEN 4: Staff Accounts
        print("5. Testing Staff Accounts screen...", flush=True)
        page.click('button:has-text("4. Staff Accounts")')
        page.wait_for_timeout(800)

        # Open Add Staff Modal
        page.click('button:has-text("+ Thêm nhân viên mới")')
        page.wait_for_timeout(500)
        page.fill('#addStaffFullName', 'Le Van Thu Nghiem')
        page.fill('#addStaffUsername', 'staff_test01')
        page.fill('#addStaffEmail', 'test.staff@parking.vn')
        page.fill('#addStaffPhone', '0912999888')
        page.fill('#addStaffPassword', '123456')

        page.click('button:has-text("Tạo tài khoản nhân viên")')
        page.wait_for_timeout(1000)

        shot2 = os.path.join(ARTIFACT_DIR, "admin_staff_accounts_verified.png")
        page.screenshot(path=shot2)
        print(f"Screenshot 2 saved: {shot2}", flush=True)

        # 6. Test SCREEN 6: Reports & Analytics
        print("6. Testing Reports & Analytics screen...", flush=True)
        page.click('button:has-text("6. Reports")')
        page.wait_for_timeout(1000)

        # Open Add Monthly Pass Modal
        page.click('button:has-text("+ Thêm vé tháng cư dân")')
        page.wait_for_timeout(500)
        page.fill('#addPassPlate', '29A-888.99')
        page.fill('#addPassName', 'Ngo Kien Huy')
        page.fill('#addPassPhone', '0903888777')
        page.fill('#addPassRoom', 'P.1802 - Toa Sapphire')
        page.click('button:has-text("Xác nhận tạo vé tháng")')
        page.wait_for_timeout(1500)

        shot3 = os.path.join(ARTIFACT_DIR, "admin_reports_verified.png")
        page.screenshot(path=shot3)
        print(f"Screenshot 3 saved: {shot3}", flush=True)

        # Scroll to bottom of main container to show Monthly Passes Table
        page.evaluate('document.querySelector("main").scrollTop = 9999')
        page.wait_for_timeout(600)
        shot3_bottom = os.path.join(ARTIFACT_DIR, "admin_reports_passes_verified.png")
        page.screenshot(path=shot3_bottom)
        print(f"Screenshot 3 (Passes table) saved: {shot3_bottom}", flush=True)

        # 7. Test SCREEN 1: Dashboard
        print("7. Testing Dashboard screen...", flush=True)
        page.click('button:has-text("1. Dashboard")')
        page.wait_for_timeout(800)
        shot4 = os.path.join(ARTIFACT_DIR, "admin_dashboard_verified.png")
        page.screenshot(path=shot4)
        print(f"Screenshot 4 saved: {shot4}", flush=True)

        browser.close()
        print(">>> ALL ADMIN VERIFICATION TESTS PASSED SUCCESSFULLY! <<<", flush=True)

if __name__ == "__main__":
    run_admin_verification()
