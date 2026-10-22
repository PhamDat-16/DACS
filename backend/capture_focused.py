import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ARTIFACT_DIR = r"C:\Users\LENOVO\.gemini\antigravity\brain\601e0b20-16bd-443a-b67d-50412978d4fc"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 950})
        page.on("dialog", lambda d: d.accept())

        print("1. Opening app...")
        page.goto("http://127.0.0.1:8000")
        page.wait_for_timeout(1000)

        # Login Admin
        page.click('button:has-text("Admin:")')
        page.wait_for_timeout(300)
        page.click('button[type="submit"]')
        page.wait_for_timeout(1000)

        # Click Reports
        page.click('button:has-text("6. Reports")')
        page.wait_for_timeout(1000)

        # Scroll to table container
        table_container = page.locator('div:has(> h3:has-text("Quản Lý Thuê Bao / Vé Tháng"))').first
        table_container.scroll_into_view_if_needed()
        page.wait_for_timeout(800)

        # Screenshot the table container directly
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "admin_monthly_passes_detail.png"))
        print("Captured admin_monthly_passes_detail.png")

        # Cycle to Staff (Admin -> Staff)
        page.click('header span:has-text("ADMIN")')
        page.wait_for_timeout(1000)

        # In Staff Dashboard: Click tab 'Thanh toán & Xuất bến'
        checkout_tab = page.locator('button:has-text("Thanh toán & Xuất bến")')
        if checkout_tab.is_visible():
            checkout_tab.click()
            page.wait_for_timeout(1000)

            # Click session for 59A1-123.45 (Active Monthly Pass)
            sess = page.locator('div[class*="cursor-pointer"]:has-text("59A1-123.45")').first
            if sess.is_visible():
                sess.click()
                page.wait_for_timeout(800)
                page.screenshot(path=os.path.join(ARTIFACT_DIR, "staff_checkout_vip_0đ.png"))
                print("Captured staff_checkout_vip_0đ.png")

        browser.close()

if __name__ == "__main__":
    run()
