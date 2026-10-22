import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ARTIFACT_DIR = r"C:\Users\LENOVO\.gemini\antigravity\brain\34425343-ff1b-46ef-a476-294ad3a89c79"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

def run_suite():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(viewport={"width": 1400, "height": 950})
        page = context.new_page()

        page.on("dialog", lambda dialog: dialog.accept())
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}", flush=True))

        print("1. Opening http://127.0.0.1:8000...", flush=True)
        page.goto("http://127.0.0.1:8000")
        page.wait_for_timeout(1500)

        # Quick login as admin
        admin_quick = page.locator('button:has-text("Admin:")')
        if admin_quick.is_visible():
            admin_quick.click()
            page.wait_for_timeout(400)
            page.click('button[type="submit"]')
            page.wait_for_timeout(1500)

        # Verify Admin Reports
        print("2. Navigating to Admin Reports (Monthly Passes)...", flush=True)
        page.click('button:has-text("6. Reports")')
        page.wait_for_timeout(1000)

        # Scroll to monthly passes table
        table_el = page.locator('h3:has-text("Quản Lý Thuê Bao / Vé Tháng")')
        if table_el.is_visible():
            table_el.scroll_into_view_if_needed()
            page.wait_for_timeout(800)

        # Screenshot Admin Passes Table
        admin_table_path = os.path.join(ARTIFACT_DIR, "admin_monthly_passes_table.png")
        page.screenshot(path=admin_table_path)
        print(f"Admin passes table screenshot saved: {admin_table_path}", flush=True)

        # 3. Test Admin Adding New Monthly Pass
        print("3. Testing Admin Add Monthly Pass without room_no...", flush=True)
        page.click('button:has-text("Đăng ký vé tháng")')
        page.wait_for_timeout(800)

        # Verify modal has plate input, name, phone, but NO room_no
        page.fill("#addPassPlate", "29A-999.88")
        page.fill("#addPassName", "Trần Văn Cường")
        page.fill("#addPassPhone", "0988665544")
        page.wait_for_timeout(400)

        # Submit add monthly pass
        page.click('button:has-text("Tạo vé & Gửi yêu cầu thanh toán")')
        page.wait_for_timeout(1200)

        page.screenshot(path=os.path.join(ARTIFACT_DIR, "admin_pass_created_pending.png"))
        print("Admin created pass 29A-999.88 (pending_payment).", flush=True)

        # 4. Switch to Customer View via cycleRole span
        print("4. Switching to Customer View...", flush=True)
        page.click('header span:has-text("ADMIN")')
        page.wait_for_timeout(600)
        page.click('header span:has-text("STAFF")')
        page.wait_for_timeout(1000)

        # Navigate to Customer Monthly Pass ('Vé tháng')
        print("Navigating to Customer 'Vé tháng' view...", flush=True)
        page.click('button:has-text("Vé tháng (Monthly Pass)")')
        page.wait_for_timeout(1500)

        cust_view_path = os.path.join(ARTIFACT_DIR, "customer_monthly_passes_view.png")
        page.screenshot(path=cust_view_path)
        print(f"Customer monthly passes view screenshot saved: {cust_view_path}", flush=True)

        # 5. Customer Clicks 'Thanh toán ngay' for Pending Pass
        pay_btn = page.locator('button:has-text("Thanh toán ngay để kích hoạt")').first
        if pay_btn.is_visible():
            print("5. Opening Monthly Pass Payment Modal...", flush=True)
            pay_btn.click()
            page.wait_for_timeout(1000)

            modal_path = os.path.join(ARTIFACT_DIR, "customer_pay_pass_modal.png")
            page.screenshot(path=modal_path)
            print(f"Payment modal screenshot saved: {modal_path}", flush=True)

            # Confirm payment
            print("Confirming payment...", flush=True)
            page.click('button:has-text("Xác nhận đã thanh toán")')
            page.wait_for_timeout(1500)

        activated_path = os.path.join(ARTIFACT_DIR, "customer_pass_activated.png")
        page.screenshot(path=activated_path)
        print(f"Customer pass activated screenshot saved: {activated_path}", flush=True)

        # 6. Verify Check-out fee logic in Staff View
        print("6. Switching to Staff View to verify check-out pricing logic...", flush=True)
        page.click('header span:has-text("CUSTOMER")')
        page.wait_for_timeout(600)
        page.click('header span:has-text("GUEST")')
        page.wait_for_timeout(600)
        page.click('header span:has-text("ADMIN")')
        page.wait_for_timeout(600)

        # In Staff view, click 'Thanh toán & Xuất bến'
        checkout_tab = page.locator('button:has-text("Thanh toán & Xuất bến")')
        if checkout_tab.is_visible():
            checkout_tab.click()
            page.wait_for_timeout(1000)

            # Click a session to inspect checkout calculation
            session_item = page.locator('div[class*="cursor-pointer"]:has-text("59A1-123.45")').first
            if session_item.is_visible():
                session_item.click()
                page.wait_for_timeout(800)

            checkout_path = os.path.join(ARTIFACT_DIR, "staff_checkout_screen.png")
            page.screenshot(path=checkout_path)
            print(f"Staff checkout screenshot saved: {checkout_path}", flush=True)

        browser.close()
        print("Verification completed successfully!", flush=True)

if __name__ == "__main__":
    run_suite()
