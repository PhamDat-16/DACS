import asyncio
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.async_api import async_playwright

ARTIFACT_DIR = r"C:\Users\LENOVO\.gemini\antigravity\brain\34425343-ff1b-46ef-a476-294ad3a89c79"

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        errors = []
        page.on("console", lambda msg: print(f"[CONSOLE {msg.type}]: {msg.text}"))
        page.on("pageerror", lambda err: errors.append(str(err)))

        print("1. Opening file:///d:/smart-parking-system/frontend/index.html ...")
        await page.goto("file:///d:/smart-parking-system/frontend/index.html")
        await page.wait_for_timeout(2000)

        # Login
        cust_btn = page.locator("button:has-text('customer@parking.vn')")
        if await cust_btn.count() > 0:
            await cust_btn.first.click()
            await page.wait_for_timeout(300)
            await page.click("button[type='submit']")
            await page.wait_for_timeout(2000)

        # Click Find Parking
        print("2. Clicking Find Parking...")
        await page.click("button:has-text('Find Parking')")
        await page.wait_for_timeout(1000)

        # Let's take screenshot of Find Parking initial state
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "debug_find_parking_initial.png"))

        # Look at the buttons
        all_buttons = await page.locator("button").all_text_contents()
        print("Buttons found on page:", [b.strip() for b in all_buttons if 'sơ đồ' in b.lower() or 'map' in b.lower()])

        # Click the button
        map_btn = page.locator("button:has-text('Xem sơ đồ')").first
        if await map_btn.count() > 0:
            print("3. Clicking Xem sơ đồ button...")
            await map_btn.click()
            await page.wait_for_timeout(1500)
        else:
            # Maybe it already says Đang xem sơ đồ?
            active_btn = page.locator("button:has-text('Đang xem sơ đồ')").first
            if await active_btn.count() > 0:
                print("Button already says 'Đang xem sơ đồ'! Clicking it...")
                await active_btn.click()
                await page.wait_for_timeout(1500)

        # Check scroll position
        scroll_y = await page.evaluate("window.scrollY")
        print(f"Current window.scrollY: {scroll_y}")

        # Check if #customerLotMapSection exists and is visible
        map_section = page.locator("#customerLotMapSection")
        section_count = await map_section.count()
        is_visible = await map_section.is_visible() if section_count > 0 else False
        print(f"#customerLotMapSection count: {section_count}, is_visible: {is_visible}")

        # Let's take screenshot of what the user sees in the viewport right now
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "debug_user_viewport_after_click.png"))
        # Also full page screenshot
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "debug_full_page_after_click.png"), full_page=True)

        print("Errors encountered:", errors)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check())
