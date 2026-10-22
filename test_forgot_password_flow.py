import sys
sys.stdout.reconfigure(encoding='utf-8')

import asyncio
from playwright.async_api import async_playwright

async def check_ui():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1400, 'height': 900})
        page.on('console', lambda m: print(f'CONSOLE: {m.text}'))
        page.on('pageerror', lambda e: print(f'PAGEERROR: {e}'))

        print("1. Đang truy cập http://127.0.0.1:8000...")
        await page.goto('http://127.0.0.1:8000')
        await page.wait_for_timeout(2000)

        # Kiểm tra link Quên mật khẩu
        forgot_link = page.locator('text=Quên mật khẩu?').first
        assert await forgot_link.is_visible(), "Link Quên mật khẩu phải hiển thị!"
        print("✓ Link 'Quên mật khẩu? (Forgot password)' hiển thị đầy đủ.")

        # Click link Quên mật khẩu
        print("2. Bấm link Quên mật khẩu...")
        await forgot_link.click()
        await page.wait_for_timeout(1000)

        # Modal phải hiển thị
        modal = page.locator('text=Khôi phục mật khẩu').first
        assert await modal.is_visible(), "Modal Khôi phục mật khẩu phải xuất hiện!"
        print("✓ Modal Khôi phục mật khẩu đã mở đẹp mắt.")

        # Chụp ảnh modal mở
        screenshot_path = 'C:/Users/LENOVO/.gemini/antigravity/brain/34425343-ff1b-46ef-a476-294ad3a89c79/forgot_password_modal_open.png'
        await page.screenshot(path=screenshot_path)
        print("Đã lưu ảnh chụp modal:", screenshot_path)

        # Thử nhập sai số điện thoại để kiểm tra tính năng bảo mật
        print("3. Kiểm tra bảo mật: Thử nhập sai số điện thoại...")
        email_inp = page.locator("input[placeholder*='customer@parking.vn']").first
        await email_inp.fill('customer@parking.vn')
        phone_inp = page.locator("input[placeholder*='0988999888']").first
        await phone_inp.fill('0111222333')
        new_pass_inp = page.locator("input[placeholder='Nhập mật khẩu mới']").first
        await new_pass_inp.fill('matkhau123')
        confirm_pass_inp = page.locator("input[placeholder='Nhập lại mật khẩu mới']").first
        await confirm_pass_inp.fill('matkhau123')

        submit_btn = page.locator("button:has-text('Xác nhận đổi mật khẩu')").first
        await submit_btn.click()
        await page.wait_for_timeout(1000)

        error_banner = page.locator('text=không khớp với thông tin').first
        assert await error_banner.is_visible(), "Hệ thống phải chặn khi SĐT xác thực không khớp!"
        print("✓ Bảo mật hoạt động tốt: Hệ thống chặn khi SĐT không chính xác.")

        # Nhập đúng số điện thoại của customer (0988999888)
        print("4. Nhập đúng số điện thoại (0988999888) và đổi mật khẩu mới (123456)...")
        await phone_inp.fill('0988999888')
        await new_pass_inp.fill('123456')
        await confirm_pass_inp.fill('123456')

        await submit_btn.click()
        await page.wait_for_timeout(1500)

        success_banner = page.locator('text=Đặt lại mật khẩu thành công').first
        assert await success_banner.is_visible(), "Thông báo thành công phải hiển thị!"
        print("✓ Đổi mật khẩu thành công xuất sắc!")

        # Chụp ảnh banner thành công
        success_screenshot_path = 'C:/Users/LENOVO/.gemini/antigravity/brain/34425343-ff1b-46ef-a476-294ad3a89c79/forgot_password_success.png'
        await page.screenshot(path=success_screenshot_path)
        print("Đã lưu ảnh chụp thành công:", success_screenshot_path)

        # Chờ modal tự đóng và form login tự động điền sẵn
        print("5. Đợi modal tự đóng và kiểm tra tự động điền form...")
        await page.wait_for_timeout(3500)
        email_val = await page.locator("input[placeholder*='Email hoặc username']").first.input_value()
        pass_val = await page.locator("input[placeholder*='Enter your password']").first.input_value()
        print(f"Form đăng nhập đã sẵn sàng: Email={email_val}, Mật khẩu={pass_val}")

        # Thử đăng nhập ngay lập tức với mật khẩu vừa đổi
        print("6. Thử đăng nhập ngay lập tức...")
        await page.click("button[type='submit']")
        await page.wait_for_timeout(2500)

        # Kiểm tra khách hàng đã đăng nhập thành công vào hệ thống
        is_logged_in = await page.locator("text=CUSTOMER").count() > 0 or await page.locator("text=Khách hàng").count() > 0 or await page.locator("text=customer@parking.vn").count() > 0
        print("Khách hàng đăng nhập vào App thành công:", is_logged_in)
        assert is_logged_in, "Khách hàng phải đăng nhập thành công sau khi đặt lại mật khẩu!"

        # Chụp ảnh dashboard sau khi đăng nhập thành công
        after_login_path = 'C:/Users/LENOVO/.gemini/antigravity/brain/34425343-ff1b-46ef-a476-294ad3a89c79/forgot_password_logged_in.png'
        await page.screenshot(path=after_login_path)
        print("Đã lưu ảnh sau đăng nhập:", after_login_path)

        print("=== TOÀN BỘ QUY TRÌNH KHÔI PHỤC MẬT KHẨU HOÀN THÀNH 100% ===")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(check_ui())

