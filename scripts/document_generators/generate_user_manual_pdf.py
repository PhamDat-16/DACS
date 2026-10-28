import subprocess
import os
import sys
import base64

sys.stdout.reconfigure(encoding='utf-8')

HTML_FILE = os.path.abspath(r"d:\smart-parking-system\huong_dan_su_dung_he_thong.html")
PDF_FILE = os.path.abspath(r"d:\smart-parking-system\huong_dan_su_dung_he_thong.pdf")
DOWNLOAD_PDF = os.path.abspath(r"C:\Users\LENOVO\Downloads\huong_dan_su_dung_he_thong.pdf")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def get_base64_image(image_path):
    if not os.path.exists(image_path):
        fname = os.path.basename(image_path)
        alt = os.path.join(r"d:\smart-parking-system\screenshots", fname)
        if os.path.exists(alt):
            image_path = alt
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

img_dashboard = get_base64_image(r"d:\smart-parking-system\screenshots\authenticated_dashboard.png")
img_auth = get_base64_image(r"d:\smart-parking-system\screenshots\auth_screen.png")

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Cẩm Nang Hướng Dẫn Sử Dụng Hệ Thống - Smart Parking System</title>
    <style>
        @page {{
            size: A4;
            margin: 10mm 12mm 10mm 12mm;
        }}
        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Times New Roman', Roboto, Arial, sans-serif;
            color: #1e293b;
            line-height: 1.36;
            font-size: 10px;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }}
        
        .doc-header {{
            border-bottom: 2px solid #0f172a;
            padding-bottom: 5px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        .doc-title {{
            font-size: 15px;
            font-weight: 800;
            color: #0f172a;
            margin: 0;
            letter-spacing: -0.2px;
            text-transform: uppercase;
        }}
        .doc-subtitle {{
            font-size: 10px;
            color: #334155;
            margin-top: 2px;
            font-weight: 600;
        }}
        .meta-info {{
            text-align: right;
            font-size: 9px;
            color: #334155;
            line-height: 1.3;
        }}

        .part-banner {{
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            border-left: 4px solid #0f172a;
            padding: 5px 8px;
            font-size: 11px;
            font-weight: 800;
            color: #0f172a;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            margin: 8px 0 6px 0;
        }}

        .section-title {{
            font-size: 10.5px;
            font-weight: 800;
            color: #0f172a;
            text-transform: uppercase;
            letter-spacing: 0.2px;
            margin: 6px 0 4px 0;
            padding-left: 5px;
            border-left: 3px solid #475569;
        }}

        /* BẢNG BIỂU CHUẨN FORMAL */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 6px;
            font-size: 9.5px;
            background-color: #ffffff;
        }}
        th, td {{
            border: 1px solid #cbd5e1;
            padding: 4px 6px;
            text-align: left;
            vertical-align: top;
        }}
        th {{
            background-color: #f1f5f9;
            color: #0f172a;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 8.5px;
            letter-spacing: 0.2px;
        }}
        tr:nth-child(even) {{
            background-color: #fafafa;
        }}
        .text-center {{ text-align: center; }}
        .text-bold {{ font-weight: 700; }}

        .guide-box {{
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            padding: 5px 8px;
            margin-bottom: 6px;
            font-size: 9.5px;
        }}
        .guide-box strong {{
            color: #0f172a;
        }}
        .guide-box ol, .guide-box ul {{
            margin: 2px 0 2px 0;
            padding-left: 16px;
            color: #334155;
        }}
        .guide-box li {{
            margin-bottom: 2px;
        }}

        .badge-color {{
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 2px;
            margin-right: 4px;
            vertical-align: middle;
            border: 1px solid #64748b;
        }}

        .image-container {{
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            overflow: hidden;
            background: #0f172a;
            margin: 6px 0;
            text-align: center;
        }}
        .image-container img {{
            width: 100%;
            max-height: 175px;
            object-fit: cover;
            display: block;
        }}
        .image-caption {{
            font-size: 8.5px;
            color: #334155;
            padding: 3px;
            background: #f8fafc;
            border-top: 1px solid #cbd5e1;
            font-style: italic;
        }}

        .page-break {{
            page-break-before: always;
            break-before: page;
        }}

        .footer-note {{
            margin-top: 5px;
            padding-top: 4px;
            border-top: 1px solid #cbd5e1;
            font-size: 8.5px;
            color: #64748b;
            display: flex;
            justify-content: space-between;
        }}
    </style>
</head>
<body>

    <!-- ==================== TRANG 1 ==================== -->
    <div class="doc-header">
        <div>
            <div class="doc-title">CẨM NANG HƯỚNG DẪN SỬ DỤNG HỆ THỐNG</div>
            <div class="doc-subtitle">Smart Parking System (SPS) — Hệ Thống Quản Lý Bãi Đỗ Xe Thông Minh</div>
        </div>
        <div class="meta-info">
            <div><strong>Tài liệu:</strong> User &amp; Administrator Manual</div>
            <div><strong>Phiên bản:</strong> Release v1.0.0</div>
            <div><strong>Thời điểm:</strong> 26/09/2026</div>
        </div>
    </div>

    <!-- PHẦN I: DÀNH CHO KHÁCH HÀNG -->
    <div class="part-banner">PHẦN I: HƯỚNG DẪN DÀNH CHO KHÁCH HÀNG (CUSTOMER USER GUIDE)</div>

    <div class="section-title">1.1. Đăng Ký, Đăng Nhập &amp; Quy Ước Trạng Thái Ô Đỗ Xe</div>
    <div class="guide-box">
        <strong>Bước 1: Truy cập và Đăng nhập tài khoản khách hàng</strong>
        <ul>
            <li>Truy cập đường dẫn: <code>http://localhost:8000</code>. Nếu chưa có tài khoản, nhấp chọn tab <em>"Đăng Ký"</em>, nhập Họ tên, Email và Mật khẩu để tạo tài khoản phân quyền <code>Customer</code>.</li>
            <li>Sau khi đăng nhập thành công, hệ thống cấp phát token bảo mật JWT tự động ghi nhớ phiên làm việc trên trình duyệt.</li>
        </ul>
    </div>

    <table style="margin-top: 4px;">
        <thead>
            <tr>
                <th style="width: 20%;">Màu Sắc Trực Quan</th>
                <th style="width: 25%;">Trạng Thái Ô Đỗ</th>
                <th style="width: 55%;">Ý Nghĩa Nghiệp Vụ &amp; Hành Động Của Khách Hàng</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><span class="badge-color" style="background: #10b981;"></span> <strong>Màu Xanh Ngọc</strong></td>
                <td><strong>Ô Trống (Available)</strong></td>
                <td>Ô đỗ đang sẵn sàng đón xe. Khách hàng nhấp chuột vào ô này để xem lộ trình dẫn đường A* và đặt chỗ trước.</td>
            </tr>
            <tr>
                <td><span class="badge-color" style="background: #f59e0b;"></span> <strong>Màu Vàng Cam</strong></td>
                <td><strong>Đã Đặt Chỗ (Reserved)</strong></td>
                <td>Ô đỗ đã có khách đặt giữ chỗ thành công qua app nhưng xe chưa đến bãi. Người khác không thể đặt trùng.</td>
            </tr>
            <tr>
                <td><span class="badge-color" style="background: #ef4444;"></span> <strong>Màu Đỏ Rực</strong></td>
                <td><strong>Đang Có Xe (Occupied)</strong></td>
                <td>Xe đã quét mã qua barrier vào đỗ trong ô (cảm biến báo có xe). Không khả dụng để đặt chỗ.</td>
            </tr>
            <tr>
                <td><span class="badge-color" style="background: #64748b;"></span> <strong>Màu Xám Tro</strong></td>
                <td><strong>Vật Cản (Blocked)</strong></td>
                <td>Cột nhà bê tông, tường ngăn hoặc khu vực bảo trì kỹ thuật. Xe không được phép di chuyển qua.</td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">1.2. Tính Năng Dẫn Đường Ngắn Nhất A* (A-Star Smart Navigation)</div>
    <div class="guide-box">
        <strong>Cách sử dụng tính năng tìm đường né vật cản:</strong>
        <ol>
            <li>Trên bản đồ ma trận bãi xe, nhấp chuột vào bất kỳ ô đỗ nào còn <strong>Trống (Màu xanh ngọc)</strong>.</li>
            <li>Hệ thống ngay lập tức kích hoạt thuật toán <strong>A* Search</strong>: tự động tính toán lộ trình ngắn nhất tuyệt đối từ Cổng vào <code>(0, 0)</code> đến ô đích, luồn lách né các ô có cột nhà và né các ô đã có xe khác đang đỗ.</li>
            <li>Diễn hoạt đồ họa <strong>GSAP</strong> sẽ mô phỏng chiếc xe ảo lăn bánh từ từ bám sát theo tọa độ lộ trình và tự động bẻ lái xoay đầu xe theo góc cua rẽ mượt mà.</li>
            <li>Bảng thông tin bên phải sẽ hiển thị: Tọa độ đích, Tổng chiều dài quãng đường (đơn vị bước di chuyển) và Trạng thái ô đỗ.</li>
        </ol>
    </div>

    <div class="section-title">1.3. Quy Trình Đặt Chỗ Trước &amp; Nhận Vé Điện Tử QR Code (Booking)</div>
    <div class="guide-box">
        <strong>Các bước thực hiện đặt chỗ xe:</strong>
        <ol>
            <li>Sau khi chọn được vị trí đỗ ưng ý trên sơ đồ, nhấp nút <strong>"Đặt Chỗ Vị Trí Này"</strong> (hoặc nút <em>"Đặt Chỗ Nhanh"</em> trên thanh công cụ).</li>
            <li>Điền thông tin vào form: <strong>Biển số xe</strong> (ví dụ: <code>30A-999.88</code>), chọn <strong>Thời lượng dự kiến</strong> (1 giờ, 2 giờ, 4 giờ... hoặc chọn <em>"Gửi đến khi checkout"</em>).</li>
            <li>Hệ thống hiển thị cước phí dự kiến &rarr; Bấm <strong>"Xác Nhận Đặt Chỗ"</strong>.</li>
            <li><strong>Nhận Vé QR Code:</strong> Màn hình lập tức hiển thị mã <strong>QR Code điện tử</strong> sắc nét cùng mã vé (ví dụ: <code>BK-7701</code>). Khách hàng có thể chụp màn hình hoặc lưu mã QR về điện thoại để quét khi đến cổng bãi xe.</li>
            <li><em>Cơ chế chống Double-Booking:</em> Nếu cùng lúc có người khác bấm đặt vị trí này, hệ thống sẽ sử dụng khóa dòng Database thông báo vị trí vừa được giữ, bảo vệ quyền lợi người đặt trước.</li>
        </ol>
    </div>

    <div class="section-title">1.4. Quy Trình Quét Vé Qua Barrier Vào/Ra Bãi Xe (Check-In &amp; Check-Out)</div>
    <div class="guide-box">
        <strong>Khi đến barrier bãi đỗ xe:</strong>
        <ul>
            <li><strong>Lúc xe vào (Check-in):</strong> Đưa mã QR trên màn hình điện thoại vào mắt đọc tại barrier cổng vào (hoặc nhân viên quét bằng tab <em>Trạm Barrier</em>). Cổng barrier tự động mở, hệ thống ghi nhận thời gian vào bãi và chuyển trạng thái ô đỗ sang <strong>Đang đỗ (Màu đỏ)</strong>.</li>
            <li><strong>Lúc xe ra (Check-out):</strong> Đưa mã QR quét tại barrier cổng ra. Hệ thống tự động tính toán tổng số phút thực tế đã gửi, tính tiền thanh toán (qua VietQR/MoMo hoặc tiền mặt), mở barrier cho xe ra và trả lại ô đỗ thành <strong>Ô trống (Màu xanh)</strong>.</li>
        </ul>
    </div>

    <div class="footer-note">
        <div>Smart Parking System (SPS) — Cẩm Nang Hướng Dẫn Sử Dụng Toàn Diện</div>
        <div>Trang 1 / 3</div>
    </div>

    <!-- ==================== TRANG 2 ==================== -->
    <div class="page-break"></div>

    <div class="doc-header">
        <div>
            <div class="doc-title">CẨM NANG HƯỚNG DẪN SỬ DỤNG HỆ THỐNG (TIẾP THEO)</div>
            <div class="doc-subtitle">Smart Parking System (SPS) — Hệ Thống Quản Lý Bãi Đỗ Xe Thông Minh</div>
        </div>
        <div class="meta-info">
            <div><strong>Phần II:</strong> Hướng Dẫn Dành Cho Quản Trị Viên (Admin &amp; Operator)</div>
        </div>
    </div>

    <!-- PHẦN II: DÀNH CHO NGƯỜI QUẢN TRỊ -->
    <div class="part-banner">PHẦN II: HƯỚNG DẪN DÀNH CHO NGƯỜI QUẢN TRỊ / VẬN HÀNH (ADMIN GUIDE)</div>

    <div class="section-title">2.1. Đăng Nhập Quyền Quản Trị Viên (Admin Role)</div>
    <div class="guide-box">
        <ul>
            <li>Đăng nhập bằng tài khoản: Email: <code>admin@example.com</code> / Mật khẩu: <code>123456</code>.</li>
            <li><em>Mẹo thao tác nhanh:</em> Tại màn hình đăng nhập, nhấp nút màu xanh <strong>"Quick Admin Login"</strong> để đăng nhập tự động 1 chạm mà không cần nhập tay.</li>
            <li>Khi đăng nhập với quyền Admin, thanh điều hướng sẽ tự động mở khóa thêm 2 phân hệ chuyên sâu: <strong>"Doanh Thu &amp; Quản Trị"</strong> và <strong>"Bản Đồ GIS Chuỗi Bãi"</strong>.</li>
        </ul>
    </div>

    <div class="section-title">2.2. Bảng Đồng Hồ Giám Sát Chỉ Số Vận Hành Thời Gian Thực (KPI Counter)</div>
    <p style="margin: 0 0 4px 0; font-size: 9.5px;">Bảng điều khiển trung tâm cung cấp 4 chỉ số thống kê quan trọng nhất được cập nhật tự động qua WebSocket:</p>
    <table>
        <thead>
            <tr>
                <th style="width: 25%;">Chỉ Số KPI</th>
                <th style="width: 25%;">Đơn Vị Hiển Thị</th>
                <th style="width: 50%;">Ý Nghĩa Giám Sát Của Người Quản Lý</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Tổng Vị Trí Quy Hoạch</strong></td>
                <td>Số lượng ô đỗ (Vị trí)</td>
                <td>Tổng số lượng ô đỗ thực tế có thể sử dụng (đã loại trừ các vị trí cột bê tông, tường ngăn).</td>
            </tr>
            <tr>
                <td><strong>Chỗ Còn Trống</strong></td>
                <td>Số lượng ô trống</td>
                <td>Số lượng ô sẵn sàng tiếp nhận xe mới. Khi chỉ số này về 0, hệ thống tự kích hoạt cảnh báo bãi đầy.</td>
            </tr>
            <tr>
                <td><strong>Tỷ Lệ Lấp Đầy Hiện Tại</strong></td>
                <td>Phần trăm (%)</td>
                <td>Tỷ lệ phần trăm bãi xe đang được sử dụng (Đang đỗ + Đã đặt trước / Tổng vị trí).</td>
            </tr>
            <tr>
                <td><strong>Doanh Thu &amp; Lượt Xe</strong></td>
                <td>VNĐ &amp; Lượt xe/ngày</td>
                <td>Tổng số lượt xe đã check-out và tổng tiền cước thu được trong ngày làm việc.</td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">2.3. Điều Khiển &amp; Khai Thác Mô Hình AI Dự Báo Lấp Đầy 24h (AI Forecast)</div>
    <div class="guide-box">
        <strong>Cách quản trị viên sử dụng AI để điều tiết bãi xe:</strong>
        <ol>
            <li>Nhấp chọn tab <strong>"AI &amp; Định Giá Động"</strong> trên thanh điều hướng.</li>
            <li>Màn hình hiển thị biểu đồ đường cong tỷ lệ lấp đầy theo 24 giờ trong ngày sinh bởi mô hình <strong>Random Forest Regressor</strong>.</li>
            <li><strong>Thao tác kéo thanh trượt (Scrubber Slider):</strong> Quản trị viên kéo thanh trượt theo từng mốc giờ (từ 0h đến 23h) &rarr; Hệ thống lập tức hiển thị công suất dự báo của khung giờ đó kèm khuyến nghị vận hành:
                <br>&bull; <em>Dưới 40%:</em> Thấp điểm &rarr; Gợi ý giảm giá cước để thu hút xe gửi.
                <br>&bull; <em>Từ 70% - 90%:</em> Cao điểm &rarr; Cảnh báo bố trí thêm nhân sự điều tiết tại barrier.
                <br>&bull; <em>Trên 90%:</em> Sắp quá tải &rarr; Tự động kích hoạt chuyển hướng xe sang các bãi vệ tinh lân cận.
            </li>
        </ol>
    </div>

    <div class="section-title">2.4. Trạm Barrier Cổng: Giám Sát Luồng Xe Ra Vào &amp; Xử Lý Sự Cố</div>
    <div class="guide-box">
        <strong>Chức năng vận hành tại phòng điều hành cổng:</strong>
        <ul>
            <li>Nhấp chọn tab <strong>"Trạm Barrier Cổng"</strong> để mở giao diện kiểm soát chuyên dụng cho nhân viên bảo vệ.</li>
            <li><strong>Quét mã QR tự động:</strong> Khi camera barrier đọc mã vé, hệ thống tự động đối soát biển số xe, hiển thị ảnh chụp xe, thời gian bắt đầu gửi và số tiền cước tích lũy.</li>
            <li><strong>Nút mở barrier thủ công:</strong> Cho phép bảo vệ mở barrier khẩn cấp cho xe ưu tiên (xe cứu hỏa, cứu thương) hoặc xử lý trường hợp khách mất vé.</li>
        </ul>
    </div>

    <div class="section-title">2.5. Quản Lý Doanh Thu &amp; Thuê Bao Vé Tháng Cư Dân (Analytics &amp; Passes)</div>
    <div class="guide-box">
        <strong>Quản lý tài chính và thẻ cư dân:</strong>
        <ul>
            <li>Nhấp chọn tab <strong>"Doanh Thu &amp; Quản Trị"</strong>: Xem báo cáo doanh thu theo 7 ngày trong tuần, biểu đồ tròn phân bổ phương thức thanh toán (VietQR 65%, MoMo 25%, Tiền mặt 10%) và tỷ lệ loại phương tiện (Ô tô 72%, Xe máy 22%, Xe điện 6%).</li>
            <li><strong>Cấp phát Vé tháng cư dân:</strong> Nhập Biển số, Tên chủ xe, Số điện thoại, Số căn hộ &rarr; Bấm <em>"Tạo Thẻ Tháng"</em> &rarr; Hệ thống tự động cấp mã thuê bao định danh và ghi nhận doanh thu tháng vào sổ quỹ.</li>
        </ul>
    </div>

    <div class="footer-note">
        <div>Smart Parking System (SPS) — Cẩm Nang Hướng Dẫn Sử Dụng Toàn Diện</div>
        <div>Trang 2 / 3</div>
    </div>

    <!-- ==================== TRANG 3 ==================== -->
    <div class="page-break"></div>

    <div class="doc-header">
        <div>
            <div class="doc-title">CẨM NANG HƯỚNG DẪN SỬ DỤNG HỆ THỐNG (TIẾP THEO)</div>
            <div class="doc-subtitle">Smart Parking System (SPS) — Hệ Thống Quản Lý Bãi Đỗ Xe Thông Minh</div>
        </div>
        <div class="meta-info">
            <div><strong>Phần III:</strong> Hình Ảnh Minh Họa Thực Tế &amp; Xử Lý Tình Huống</div>
        </div>
    </div>

    <!-- PHẦN III: HÌNH ẢNH MINH HỌA -->
    <div class="part-banner">PHẦN III: HÌNH ẢNH MINH HỌA CÁC VÍ DỤ SỬ DỤNG THỰC TẾ</div>

    <div class="section-title">3.1. Hình Ảnh Minh Họa Thực Tế Các Giao Diện Chức Năng</div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 4px 0 6px 0;">
        <div class="image-container">
            <img src="{img_auth}" alt="Màn hình đăng nhập">
            <div class="image-caption">Hình 1: Màn hình Đăng nhập phân quyền (Khách hàng &amp; Quản trị viên) với JWT</div>
        </div>
        <div class="image-container">
            <img src="{img_dashboard}" alt="Bảng điều khiển bãi xe">
            <div class="image-caption">Hình 2: Bảng điều khiển trung tâm với Sơ đồ bãi xe, xe chạy A* và chỉ số KPI</div>
        </div>
    </div>

    <!-- PHẦN IV: CÁC VÍ DỤ SỬ DỤNG ĐIỂN HÌNH -->
    <div class="section-title">3.2. Ví Dụ Tình Huống Sử Dụng Thực Tế (Practical Use Cases)</div>
    <table>
        <thead>
            <tr>
                <th style="width: 25%;">Tình Huống Sử Dụng</th>
                <th style="width: 45%;">Hành Động Của Người Dùng</th>
                <th style="width: 30%;">Phản Hồi Tự Động Của Hệ Thống</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Ví dụ 1: Khách hàng muốn giữ chỗ trước giờ cao điểm</strong></td>
                <td>Mở web &rarr; Xem sơ đồ bãi &rarr; Chọn ô A-01 còn trống &rarr; Bấm "Đặt chỗ" &rarr; Nhập biển số <code>29A-123.45</code> và chọn gửi 2 tiếng &rarr; Xác nhận.</td>
                <td>Hệ thống khóa ô A-01 chuyển sang màu vàng (Reserved), sinh mã vé QR Base64 trên màn hình, các máy khác không thể đặt trùng ô này.</td>
            </tr>
            <tr>
                <td><strong>Ví dụ 2: Lái xe vào bãi cần tìm đường ngắn nhất</strong></td>
                <td>Khách lái xe qua cổng vào &rarr; Nhấp vào vị trí ô đã đặt trên màn hình điện thoại.</td>
                <td>Thuật toán A* vẽ vệt màu tím dẫn đường ngắn nhất; xe ảo lăn bánh bẻ lái chỉ dẫn lái xe di chuyển đúng làn tránh cột bê tông.</td>
            </tr>
            <tr>
                <td><strong>Ví dụ 3: Quản trị viên muốn dự đoán lượng xe tối nay</strong></td>
                <td>Admin mở tab "AI &amp; Định Giá Động" &rarr; Kéo thanh trượt Scrubber đến mốc <strong>19:00</strong>.</td>
                <td>Mô hình Random Forest tính toán công suất dự báo đạt <strong>89%</strong> &rarr; Hệ thống khuyến nghị bố trí 2 nhân viên trực barrier cổng.</td>
            </tr>
            <tr>
                <td><strong>Ví dụ 4: Khách hàng đến TTTM nhưng bãi chính bị đầy</strong></td>
                <td>Khách thấy bãi chính báo 100% lấp đầy &rarr; Mở tab <em>"Bản Đồ GIS Chuỗi Bãi"</em>.</td>
                <td>Hệ thống hiển thị danh sách 3 bãi xe vệ tinh lân cận cách 250m còn chỗ &rarr; Khách chuyển sang đặt chỗ bãi gần nhất.</td>
            </tr>
        </tbody>
    </table>

    <!-- PHẦN V: XỬ LÝ SỰ CỐ & CÂU HỎI THƯỜNG GẶP -->
    <div class="part-banner">PHẦN IV: CÂU HỎI THƯỜNG GẶP &amp; HƯỚNG DẪN XỬ LÝ SỰ CỐ (FAQ)</div>
    <div class="guide-box">
        <ul>
            <li><strong>Câu hỏi 1: Làm sao để chạy hệ thống khi không có mạng Internet?</strong>
                <br>&rarr; Hệ thống hoạt động 100% Offline trên môi trường Localhost. Ngoài ra, giao diện Frontend tích hợp sẵn <strong>Standalone Mock Engine</strong>, bạn chỉ cần nhấp đúp file <code>frontend/index.html</code> là toàn bộ thuật toán A* và biểu đồ AI đều chạy mượt mà ngay trên trình duyệt mà không cần bật server!
            </li>
            <li><strong>Câu hỏi 2: Nếu mất mã vé QR thì khách hàng lấy xe ra bằng cách nào?</strong>
                <br>&rarr; Nhân viên quản trị vào tab <strong>"Trạm Barrier Cổng"</strong> hoặc <strong>"Vé &amp; Đặt Chỗ"</strong>, tìm kiếm theo <strong>Biển số xe</strong> của khách, hệ thống sẽ hiển thị lại thông tin vé, số tiền cần thanh toán và cho phép xác nhận Check-out hợp lệ.
            </li>
            <li><strong>Câu hỏi 3: Hai khách hàng cùng bấm đặt 1 ô đỗ cùng 1 lúc thì xử lý thế nào?</strong>
                <br>&rarr; Nhờ cơ chế khóa cấp hàng Database (<code>SELECT FOR UPDATE</code>), khách hàng bấm trước 1 mili-giây sẽ đặt thành công, khách hàng thứ hai sẽ nhận được thông báo lịch sự: <em>"Vị trí này vừa có người đặt, vui lòng chọn vị trí khác"</em> mà không bao giờ xảy ra lỗi xung đột.
            </li>
        </ul>
    </div>

    <div class="footer-note">
        <div>Smart Parking System (SPS) — Cẩm Nang Hướng Dẫn Sử Dụng Toàn Diện</div>
        <div>Trang 3 / 3</div>
    </div>

</body>
</html>
"""

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML manual saved to: {HTML_FILE}")

# Use Edge headless to generate PDF
args = [
    EDGE_PATH,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_FILE}",
    f"file:///{HTML_FILE.replace(os.sep, '/')}"
]

print("Rendering PDF with Edge...")
subprocess.run(args, check=True)

if os.path.exists(PDF_FILE):
    import shutil
    try:
        shutil.copy2(PDF_FILE, DOWNLOAD_PDF)
        print(f"SUCCESS! Created PDF: {PDF_FILE} and copied to Downloads: {DOWNLOAD_PDF}")
    except PermissionError:
        alt_download = os.path.abspath(r"C:\Users\LENOVO\Downloads\huong_dan_su_dung_he_thong_v2.pdf")
        shutil.copy2(PDF_FILE, alt_download)
        print(f"SUCCESS! Created PDF: {PDF_FILE} and copied to alternative: {alt_download}")
