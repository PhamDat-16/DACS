import sys
sys.stdout.reconfigure(encoding='utf-8')
import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1400, 'height': 900})
        page.on('console', lambda m: print('CONSOLE:', m.text))
        page.on('pageerror', lambda e: print('PAGEERROR:', e))

        print("Navigating to http://127.0.0.1:8000...")
        await page.goto('http://127.0.0.1:8000')
        await page.wait_for_timeout(1500)

        # Login customer
        print("Logging in customer...")
        await page.locator("input[placeholder*='Email hoặc username']").first.fill('customer@parking.vn')
        await page.locator("input[placeholder*='Enter your password']").first.fill('123456')
        await page.click("button[type='submit']")
        await page.wait_for_timeout(2000)

        # Click Find Parking
        print("Clicking Find Parking...")
        await page.locator("button:has-text('Find Parking')").first.click()
        await page.wait_for_timeout(1000)

        btn_count = await page.locator("button:has-text('Xem sơ đồ')").count()
        print(f"Found {btn_count} 'Xem sơ đồ' buttons.")

        if btn_count > 0:
            print("Clicking first 'Xem sơ đồ' button...")
            await page.locator("button:has-text('Xem sơ đồ')").first.click()
            await page.wait_for_timeout(1500)
            target_path = 'C:/Users/LENOVO/.gemini/antigravity/brain/34425343-ff1b-46ef-a476-294ad3a89c79/find_parking_clicked_map.png'
            await page.screenshot(path=target_path)
            print("Saved screenshot to:", target_path)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(inspect())

