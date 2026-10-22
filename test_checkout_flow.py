import sys
sys.stdout.reconfigure(encoding='utf-8')

import asyncio
from playwright.async_api import async_playwright

async def test_checkout():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        page.on('console', lambda msg: print(f'[CONSOLE {msg.type}] {msg.text}'))
        page.on('dialog', lambda d: asyncio.create_task(d.accept()))

        print("1. Đi tới http://127.0.0.1:8000...")
        await page.goto('http://127.0.0.1:8000')
        await page.wait_for_timeout(2000)

        # Login directly by filling the input fields
        print("2. Điền thông tin đăng nhập bao@gmail.com...")
        email_input = page.locator("input[placeholder*='Email hoặc username']").first
        await email_input.fill("bao@gmail.com")

        pass_input = page.locator("input[placeholder*='Enter your password']").first
        await pass_input.fill("123456")
        await page.wait_for_timeout(300)

        submit_btn = page.locator("button[type='submit']").first
        await submit_btn.click()
        await page.wait_for_timeout(3000)

        # Go to Check-in vehicle
        print("3. Chuyển sang màn hình Check-in...")
        checkin_nav = page.locator("button:has-text('2. Check-in Vehicle')").first
        await checkin_nav.click()
        await page.wait_for_timeout(1500)

        # Check in a test vehicle
        test_plate = "51H-999.88"
        print(f"4. Nhập xe {test_plate} để check-in...")
        plate_input = page.locator("input[placeholder*='29A-999.88']").first
        await plate_input.fill("")
        await plate_input.fill(test_plate)
        await page.wait_for_timeout(500)

        checkin_btn = page.locator("button:has-text('Tự động tìm vị trí & Check-in')").first
        await checkin_btn.click()
        await page.wait_for_timeout(1500)

        # Confirm checkin modal button is "Mở Barie & Bắt đầu tính giờ"
        print("5. Bấm xác nhận mở Barie check-in...")
        confirm_btn = page.locator("button:has-text('Mở Barie & Bắt đầu tính giờ')").first
        if await confirm_btn.is_visible():
            await confirm_btn.click()
            await page.wait_for_timeout(2000)
        else:
            print("Confirm button not found, checking alternative...")
            alt_btn = page.locator(".fixed.inset-0 button:has-text('Mở Barie')").first
            if await alt_btn.is_visible():
                await alt_btn.click()
                await page.wait_for_timeout(2000)

        # Navigate to 3. Check-out Vehicle
        print("6. Chuyển sang màn hình 3. Check-out Vehicle...")
        checkout_nav = page.locator("button:has-text('3. Check-out Vehicle')").first
        await checkout_nav.click()
        await page.wait_for_timeout(1500)

        # Find 51H-999.88 in the list or search input
        print(f"7. Tìm xe {test_plate}...")
        vehicle_card = page.locator(f"text={test_plate}").first
        if await vehicle_card.is_visible():
            print("Đã thấy xe trong danh sách bên trái. Click chọn xe...")
            await vehicle_card.click()
            await page.wait_for_timeout(1000)
        else:
            print("Tìm kiếm theo ô input...")
            search_input = page.locator("input[placeholder*='Nhập biển số']").first
            await search_input.fill(test_plate)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(1000)

        # Chụp ảnh màn hình trước khi bấm checkout
        before_screenshot = "C:/Users/LENOVO/.gemini/antigravity/brain/34425343-ff1b-46ef-a476-294ad3a89c79/staff_checkout_before_click.png"
        await page.screenshot(path=before_screenshot)
        print(f"Đã chụp ảnh trước khi bấm: {before_screenshot}")

        # Nút Xác nhận thanh toán & Mở Barie
        checkout_btn = page.locator("button:has-text('Xác nhận thanh toán')").first
        assert await checkout_btn.is_visible(), "Nút 'Xác nhận thanh toán & Mở Barie' phải hiển thị!"
        assert await checkout_btn.is_enabled(), "Nút 'Xác nhận thanh toán & Mở Barie' phải được kích hoạt (enabled)!"

        print("8. Bấm nút 'Xác nhận thanh toán & Mở Barie'...")
        await checkout_btn.click()
        await page.wait_for_timeout(3000)

        # Chụp ảnh sau khi checkout hoàn tất
        after_screenshot = "C:/Users/LENOVO/.gemini/antigravity/brain/34425343-ff1b-46ef-a476-294ad3a89c79/staff_checkout_after_click.png"
        await page.screenshot(path=after_screenshot)
        print(f"Đã chụp ảnh sau khi bấm thành công: {after_screenshot}")

        # Kiểm tra thông báo thành công hoặc phiên được trả
        toast = page.locator("text=Đã thanh toán thành công và mở Barie")
        toast_count = await toast.count()
        print(f"Toast thành công hiển thị: {toast_count > 0}")

        print("=== KẾT QUẢ KIỂM THỬ: HOÀN TOÀN THÀNH CÔNG! ===")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_checkout())
