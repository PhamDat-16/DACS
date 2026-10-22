import sys
sys.stdout.reconfigure(encoding='utf-8')
import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1400, 'height': 900})

        await page.goto('http://127.0.0.1:8000')
        await page.wait_for_timeout(1500)

        # Login customer
        await page.locator("input[placeholder*='Email hoặc username']").first.fill('customer@parking.vn')
        await page.locator("input[placeholder*='Enter your password']").first.fill('123456')
        await page.click("button[type='submit']")
        await page.wait_for_timeout(2000)

        # Click Find Parking
        await page.locator("button:has-text('Find Parking')").first.click()
        await page.wait_for_timeout(1000)

        # Click Xem sơ đồ
        await page.locator("button:has-text('Xem sơ đồ')").first.click()
        await page.wait_for_timeout(1000)

        map_el = page.locator("text=Sơ đồ bãi xe:")
        count = await map_el.count()
        print(f"Map section count: {count}")
        if count > 0:
            await map_el.first.scroll_into_view_if_needed()
            await page.wait_for_timeout(500)
            target_path = 'C:/Users/LENOVO/.gemini/antigravity/brain/34425343-ff1b-46ef-a476-294ad3a89c79/find_parking_scrolled_to_map.png'
            await page.screenshot(path=target_path)
            print("Saved scrolled screenshot to:", target_path)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(inspect())

