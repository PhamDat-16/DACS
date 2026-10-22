import time
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ARTIFACT_DIR = r"C:\Users\LENOVO\.gemini\antigravity\brain\601e0b20-16bd-443a-b67d-50412978d4fc"

def run_staff_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(viewport={"width": 1400, "height": 950})
        page = context.new_page()

        page.on("dialog", lambda dialog: dialog.accept())
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}", flush=True))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}", flush=True))

        print("1. Opening app at http://127.0.0.1:8000...", flush=True)
        page.goto("http://127.0.0.1:8000")
        page.wait_for_timeout(1000)

        # 1. Login as Admin
        print("2. Logging in as Admin...", flush=True)
        page.click('button:has-text("Admin:")')
        page.wait_for_timeout(300)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # 2. Go to Staff Accounts
        print("3. Navigating to Staff Accounts screen...", flush=True)
        page.click('button:has-text("Staff Accounts")')
        page.wait_for_timeout(1000)

        # 3. Open Add Staff modal
        print("4. Opening '+ Thêm nhân viên mới' modal...", flush=True)
        page.click('button:has-text("Thêm nhân viên mới")')
        page.wait_for_timeout(500)

        # 4. Fill Staff details
        test_email = f"staff_{int(time.time())}@parking.vn"
        test_username = f"stf_{int(time.time()) % 10000}"
        test_password = "staffpassword123"
        test_fullname = "Nguyễn Văn Bảo Vệ Mới"

        print(f"5. Filling new staff: {test_email} / {test_password}...", flush=True)
        page.fill("#addStaffFullName", test_fullname)
        page.fill("#addStaffUsername", test_username)
        page.fill("#addStaffEmail", test_email)
        page.fill("#addStaffPhone", "0911222333")
        page.fill("#addStaffPassword", test_password)

        # Submit modal
        print("6. Submitting staff creation form...", flush=True)
        page.click('button:has-text("Lưu & Cấp tài khoản")')
        page.wait_for_timeout(1500)

        # Verify staff appears in table
        print("7. Verifying staff appears in Admin table...", flush=True)
        assert page.locator(f"text='{test_email}'").is_visible(), f"Email {test_email} not found in staff table!"

        # Take screenshot of Admin Staff table with new staff
        admin_screenshot = f"{ARTIFACT_DIR}\\admin_staff_created_verified.png"
        page.screenshot(path=admin_screenshot)
        print(f"Admin screenshot saved to: {admin_screenshot}", flush=True)

        # 8. Logout
        print("8. Logging out from Admin...", flush=True)
        page.click('button:has-text("Logout")')
        page.wait_for_timeout(1000)

        # 9. Login with NEW STAFF credentials!
        print(f"9. Logging in with NEW STAFF credentials ({test_email} / {test_password})...", flush=True)
        page.fill('input[placeholder="Enter your email"]', test_email)
        page.fill('input[placeholder="Enter your password"]', test_password)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2500)

        # 10. Verify Staff Portal is active!
        print("10. Verifying Staff Portal...", flush=True)
        staff_badge = page.locator('span:has-text("STAFF")').first
        assert staff_badge.is_visible(), "STAFF role badge not found! Staff login failed!"
        
        # Check Staff name or welcome message
        user_name_element = page.locator(f"text='{test_fullname}'").first
        assert user_name_element.is_visible(), f"Staff name {test_fullname} not found on dashboard!"

        # Take screenshot of the newly logged in Staff Dashboard
        staff_screenshot = f"{ARTIFACT_DIR}\\new_staff_login_verified.png"
        page.screenshot(path=staff_screenshot)
        print(f"Staff login screenshot saved to: {staff_screenshot}", flush=True)

        print("=== ALL TESTS PASSED! NEW STAFF REGISTERED TO POSTGRESQL AND LOGGED IN SUCCESSFULLY! ===", flush=True)
        browser.close()

if __name__ == "__main__":
    run_staff_verification()
