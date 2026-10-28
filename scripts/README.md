# THƯ MỤC CÔNG CỤ VÀ KỊCH BẢN PHỤ TRỢ (SCRIPTS & TOOLS)

Thư mục này quy hoạch toàn bộ các kịch bản phụ trợ của dự án Smart Parking System theo 2 nhóm chức năng chính:

## 1. `document_generators/` (Công cụ sinh tài liệu & báo cáo học thuật)
Chứa các script tự động hóa biên soạn và xuất các báo cáo đồ án, kế hoạch, slide thuyết trình chuẩn định dạng Word (`.docx`) và PDF (`.pdf`):
- `build_full_thesis.py`: Biên soạn toàn bộ Báo cáo ĐACS hoàn chỉnh 100 trang.
- `build_progress_report.py`, `build_progress_report_dot3.py`: Xuất Báo cáo tiến độ đề tài.
- `build_plan_10_weeks.py`: Xuất Kế hoạch thực hiện 10 tuần.
- `build_meeting_minutes.py`: Xuất Biên bản họp nhóm định kỳ.
- `export_presentation_pdf.py`: Xuất Slide thuyết trình đồ án ra PDF.
- `generate_user_manual_pdf.py`: Xuất Sổ tay hướng dẫn sử dụng hệ thống.
- `generate_defense_qa_pdf.py`: Xuất Bộ câu hỏi và đáp án bảo vệ đồ án.

## 2. `test_tools/` (Công cụ kiểm thử độc lập cho các chức năng)
Chứa các kịch bản kiểm thử chức năng chuyên sâu từ bên ngoài:
- `test_booking_conflict.py`: Kiểm thử khóa bi quan chống đặt chỗ trùng.
- `test_vip_gate.py`: Kiểm thử nhận diện xe vé tháng VIP tại cổng.
- `test_checkout_flow.py`: Kiểm thử quy trình xuất bến và thanh toán.
- `test_payment_ux.py`: Kiểm thử giao diện thanh toán VietQR.
- `test_qr.py`: Kiểm thử giải mã và xác thực mã QR.
- `test_add_vehicle.py`: Kiểm thử tạo phương tiện.
- `test_admin_revenue.py`: Kiểm thử tính toán doanh thu và thống kê Admin.
- `test_find_car.py`: Kiểm thử tính năng tìm xe trong bãi.
- `test_forgot_password_flow.py`: Kiểm thử khôi phục mật khẩu.

## 3. `view_db.py`
Script in dữ liệu các bảng cơ sở dữ liệu PostgreSQL ra màn hình console (được gọi tự động bởi `xem_database.bat`).
