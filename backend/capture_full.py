import os
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\LENOVO\.gemini\antigravity\brain\601e0b20-16bd-443a-b67d-50412978d4fc"

with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge', headless=True)
    page = b.new_page(viewport={'width': 1400, 'height': 900})
    page.goto('http://127.0.0.1:8000')
    page.wait_for_timeout(1000)

    page.locator('button:has-text("Admin:")').click()
    page.wait_for_timeout(300)
    page.locator('button[type="submit"]').click()
    page.wait_for_timeout(1000)

    # Go to reports
    page.locator('button:has-text("6. Reports")').click()
    page.wait_for_timeout(1000)

    # Full page screenshot of Admin Reports
    page.screenshot(path=os.path.join(ARTIFACT_DIR, "admin_reports_passes_full.png"), full_page=True)
    print("Saved admin_reports_passes_full.png")

    b.close()
