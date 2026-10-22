import time
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ARTIFACT_DIR = r"C:\Users\LENOVO\.gemini\antigravity\brain\601e0b20-16bd-443a-b67d-50412978d4fc"

def capture_detailed():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(viewport={"width": 1400, "height": 950})
        page = context.new_page()
        page.on("dialog", lambda dialog: dialog.accept())

        # 1. Admin Reports Table view
        page.goto("http://127.0.0.1:8000")
        page.wait_for_timeout(1000)

        # Login
        admin_quick = page.locator('button:has-text("Admin:")')
        if admin_quick.is_visible():
            admin_quick.click()
            page.wait_for_timeout(300)
            page.click('button[type="submit"]')
            page.wait_for_timeout(1000)

        page.click('button:has-text("6. Reports")')
        page.wait_for_timeout(1000)

        # Scroll right to the table
        table_el = page.locator('table')
        if table_el.is_visible():
            table_el.scroll_into_view_if_needed()
            page.wait_for_timeout(800)

        page.screenshot(path=os.path.join(ARTIFACT_DIR, "admin_monthly_passes_detail.png"))
        print("Captured admin_monthly_passes_detail.png")

        # 2. Staff checkout view
        page.click('header span:has-text("ADMIN")')
        page.wait_for_timeout(500)

        # Checkout tab
        page.click('button:has-text("Thanh toán & Xuất bến")')
        page.wait_for_timeout(1000)

        # Select vehicle 59A1-123.45 (Active VIP Pass -> 0 VNĐ)
        sess_vip = page.locator('div[class*="cursor-pointer"]:has-text("59A1-123.45")').first
        if sess_vip.is_visible():
            sess_vip.click()
            page.wait_for_timeout(800)
            page.screenshot(path=os.path.join(ARTIFACT_DIR, "staff_checkout_vip_zero_fee.png"))
            print("Captured staff_checkout_vip_zero_fee.png")

        browser.close()

if __name__ == "__main__":
    capture_detailed()
