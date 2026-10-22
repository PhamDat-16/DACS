import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

def test_shift_handover_and_lot_locking():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(viewport={"width": 1400, "height": 950})
        page = context.new_page()

        alerts = []
        page.on("dialog", lambda dialog: (alerts.append(dialog.message), dialog.accept()))
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}", flush=True))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}", flush=True))

        print("=== BƯỚC 1: ĐĂNG NHẬP VỚI TÀI KHOẢN NHÂN VIÊN CA SÁNG (BAO@GMAIL.COM) ===", flush=True)
        page.goto("http://127.0.0.1:8001")
        page.wait_for_timeout(1000)

        # Click quick fill for Staff Ca Sáng
        page.click('button:has-text("Staff Ca Sáng")')
        page.wait_for_timeout(300)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Chuyển sang màn hình Check-in Vehicle
        page.click('button:has-text("Check-in Vehicle")')
        page.wait_for_timeout(1000)

        # Kiểm tra 1: Bốt trực bị khóa cố định, không có dropdown đổi bãi
        locked_badge = page.locator('text="Bốt trực phân công (Cố định)"')
        assert locked_badge.is_visible(), "LỖI: Nhân viên không thấy huy hiệu bốt trực cố định!"
        print("✓ Đã xác minh: Nhân viên bị khóa cố định vào đúng 1 bãi được phân công, không có dropdown đổi bãi.", flush=True)

        # Thiết lập giờ mô phỏng: 09:30 (Trong Ca Sáng)
        page.select_option('#simulatedHourSelect', '09:30')
        page.wait_for_timeout(500)

        shift_badge = page.locator('#staffShiftBadge')
        badge_text = shift_badge.inner_text()
        print(f"Trạng thái ca trực lúc 09:30: {badge_text}", flush=True)
        assert "ĐANG TRONG CA TRỰC" in badge_text, "LỖI: Nhân viên Ca Sáng lúc 09:30 phải đang trong ca trực!"

        # Check-in 1 xe khách vãng lai: 30A-999.88
        print("\n=== BƯỚC 2: CHECK-IN PHƯƠNG TIỆN 30A-999.88 TRONG CA SÁNG ===", flush=True)
        page.fill('input[placeholder*="29A-999.88"]', '30A-999.88')
        page.fill('input[placeholder*="Anh Tuấn"]', 'Bác Hoàng')
        page.fill('input[placeholder*="0912 345 678"]', '0988776655')
        page.click('button:has-text("Tự động tìm vị trí")')
        page.wait_for_timeout(800)

        # Bấm nút xác nhận trong modal
        page.click('button:has-text("Mở Barie & Bắt đầu tính giờ")')
        page.wait_for_timeout(1500)

        print("✓ Nhân viên Ca Sáng đã check-in thành công xe 30A-999.88 vào bãi lúc 09:30.", flush=True)

        # Kiểm tra 2: Đổi giờ mô phỏng sang 16:30 (Đã sang Ca Chiều, Nhân viên Ca Sáng HẾT CA)
        print("\n=== BƯỚC 3: MÔ PHỎNG HẾT CA SÁNG (CHUYỂN SANG 16:30) VÀ KIỂM TRA CHẶN NGOÀI GIỜ ===", flush=True)
        page.select_option('#simulatedHourSelect', '16:30')
        page.wait_for_timeout(500)

        badge_text_afternoon = shift_badge.inner_text()
        print(f"Trạng thái ca trực lúc 16:30: {badge_text_afternoon}", flush=True)
        assert "NGOÀI CA TRỰC" in badge_text_afternoon, "LỖI: Nhân viên Ca Sáng lúc 16:30 phải báo NGOÀI CA TRỰC!"

        # Thử bấm check-in xe mới lúc ngoài giờ -> PHẢI BỊ CHẶN
        alerts.clear()
        page.fill('input[placeholder*="29A-999.88"]', '29B-123.45')
        page.click('button:has-text("Tự động tìm vị trí")')
        page.wait_for_timeout(500)
        assert any("NGOÀI CA TRỰC" in msg or "TỪ CHỐI" in msg for msg in alerts), f"LỖI: Chưa chặn tự động phân ô ngoài ca trực! Alerts: {alerts}"
        print(f"✓ Đã chặn thành công thao tác check-in ngoài ca trực: {alerts[-1]}", flush=True)

        # Thử sang màn hình Check-out lúc ngoài giờ -> PHẢI BỊ CHẶN
        print("\n=== BƯỚC 4: NHÂN VIÊN CA SÁNG CỐ TÌNH CHECK-OUT LÚC 16:30 (HẾT CA) -> PHẢI BỊ CHẶN ===", flush=True)
        page.click('button:has-text("Check-out Vehicle")')
        page.wait_for_timeout(1000)

        # Chọn xe 30A-999.88 để checkout
        page.click('text="30A-999.88"')
        page.wait_for_timeout(500)

        alerts.clear()
        # Bấm Xác nhận thanh toán & Mở Barie
        page.click('button:has-text("Xác nhận thanh toán")')
        page.wait_for_timeout(500)
        assert any("TỪ CHỐI CHECK-OUT" in msg or "kết thúc" in msg for msg in alerts), f"LỖI: Chưa chặn checkout ngoài giờ làm việc! Alerts: {alerts}"
        print(f"✓ Đã chặn thành công nhân viên hết ca thực hiện checkout: {alerts[-1]}", flush=True)

        # Đăng xuất tài khoản Ca Sáng (Nút Sign Out trên thanh bên trái)
        page.click('button:has-text("Sign Out")')
        page.wait_for_timeout(1000)

        # Đăng nhập tài khoản Ca Chiều (dan@gmai.com)
        print("\n=== BƯỚC 5: ĐĂNG NHẬP NHÂN VIÊN CA CHIỀU (DAN@GMAI.COM) VÀ THỰC HIỆN CHECKOUT LIÊN CA ===", flush=True)
        page.click('button:has-text("Staff Ca Chiều")')
        page.wait_for_timeout(300)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Vào màn hình Check-out
        page.click('button:has-text("Check-out Vehicle")')
        page.wait_for_timeout(1000)

        # Thiết lập giờ mô phỏng tại Check-out thành 16:30 (Thuộc Ca Chiều 14h - 22h)
        page.select_option('div:has-text("Giờ mô phỏng:") select', '16:30')
        page.wait_for_timeout(500)

        # Chọn xe 30A-999.88 trong danh sách bên trái
        session_item = page.locator('div:has-text("30A-999.88")').last
        session_item.click()
        page.wait_for_timeout(500)

        # In nội dung cột chi tiết để debug
        detail_card = page.locator('div.lg\\:col-span-2')
        print("NỘI DUNG THẺ CHECKOUT:\n", detail_card.inner_text(), flush=True)

        alerts.clear()
        # Thực hiện checkout bởi Nhân viên Ca Chiều
        checkout_btn = page.locator('button:has-text("Xác nhận thanh toán")')
        print(f"Nút checkout visible: {checkout_btn.is_visible()}, enabled: {checkout_btn.is_enabled()}", flush=True)
        checkout_btn.click()
        page.wait_for_timeout(2000)

        print(f"Alerts sau checkout: {alerts}", flush=True)
        toast = page.locator('div.bg-emerald-500:has-text("thanh toán thành công")')
        print(f"Toast visible: {toast.is_visible()}", flush=True)
        if toast.is_visible():
            print(f"Toast text: {toast.inner_text()}", flush=True)

        # Chụp ảnh minh chứng
        screenshot_path = r"d:\smart-parking-system\shift_handover_verified.png"
        page.screenshot(path=screenshot_path)
        print(f"\n✓ Đã chụp ảnh kết quả kiểm thử tại: {screenshot_path}", flush=True)
        browser.close()

if __name__ == '__main__':
    test_shift_handover_and_lot_locking()
