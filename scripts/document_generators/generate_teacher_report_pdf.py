import subprocess
import os
import sys
import base64

sys.stdout.reconfigure(encoding='utf-8')

HTML_FILE = os.path.abspath(r"d:\smart-parking-system\bao_cao_giang_vien.html")
PDF_FILE = os.path.abspath(r"d:\smart-parking-system\bao_cao_ket_qua_du_an_gui_giang_vien.pdf")
DOWNLOAD_PDF = os.path.abspath(r"C:\Users\LENOVO\Downloads\bao_cao_ket_qua_du_an_gui_giang_vien.pdf")
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
    <title>Báo Cáo Kết Quả Đã Hoàn Thành - Dự Án Smart Parking System</title>
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
            font-size: 10.5px;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }}
        
        /* HEADER BÁO CÁO HỌC THUẬT CHUẨN MỰC */
        .academic-header {{
            border-bottom: 2px solid #0f172a;
            padding-bottom: 6px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        .doc-title {{
            font-size: 16px;
            font-weight: 800;
            color: #0f172a;
            margin: 0;
            letter-spacing: -0.2px;
            text-transform: uppercase;
        }}
        .doc-subtitle {{
            font-size: 10.5px;
            color: #334155;
            margin-top: 2px;
            font-weight: 600;
        }}
        .meta-box {{
            text-align: right;
            font-size: 9.5px;
            color: #334155;
            line-height: 1.35;
        }}

        /* KHUNG THỐNG KÊ TỔNG QUAN (KPI) */
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            margin-bottom: 9px;
        }}
        .kpi-box {{
            border: 1px solid #cbd5e1;
            border-top: 3px solid #0f172a;
            background: #f8fafc;
            border-radius: 4px;
            padding: 6px 8px;
            text-align: center;
        }}
        .kpi-num {{
            font-size: 16px;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.1;
        }}
        .kpi-label {{
            font-size: 9px;
            font-weight: 700;
            color: #475569;
            text-transform: uppercase;
            margin-top: 2px;
        }}

        .section-title {{
            font-size: 11px;
            font-weight: 800;
            color: #0f172a;
            text-transform: uppercase;
            letter-spacing: 0.2px;
            margin: 8px 0 5px 0;
            padding-left: 6px;
            border-left: 3px solid #0f172a;
        }}

        /* BẢNG BIỂU CHUẨN FORMAL */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 7px;
            font-size: 9.5px;
            background-color: #ffffff;
        }}
        th, td {{
            border: 1px solid #cbd5e1;
            padding: 4px 6px;
            text-align: left;
            vertical-align: middle;
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

        .tag-done {{
            display: inline-block;
            padding: 1px 5px;
            border-radius: 3px;
            font-size: 8.5px;
            font-weight: 700;
            background: #e2e8f0;
            color: #0f172a;
            border: 1px solid #94a3b8;
            text-transform: uppercase;
        }}

        .highlight-box {{
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-left: 3px solid #334155;
            border-radius: 4px;
            padding: 6px 10px;
            margin-bottom: 6px;
            font-size: 10px;
        }}
        .highlight-box strong {{
            color: #0f172a;
        }}
        .highlight-box ul {{
            margin: 3px 0 0 0;
            padding-left: 15px;
            color: #334155;
            font-size: 9.5px;
        }}
        .highlight-box li {{
            margin-bottom: 2px;
        }}

        .image-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin: 6px 0;
        }}
        .image-card {{
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            overflow: hidden;
            background: #0f172a;
            text-align: center;
        }}
        .image-card img {{
            width: 100%;
            height: 160px;
            object-fit: cover;
            display: block;
        }}
        .image-desc {{
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
            margin-top: 6px;
            padding-top: 5px;
            border-top: 1px solid #cbd5e1;
            font-size: 9px;
            color: #64748b;
            display: flex;
            justify-content: space-between;
        }}
    </style>
</head>
<body>

    <!-- ==================== TRANG 1 ==================== -->
    <div class="academic-header">
        <div>
            <div class="doc-title">BÁO CÁO KẾT QUẢ ĐÃ HOÀN THÀNH CỦA DỰ ÁN</div>
            <div class="doc-subtitle">Hệ Thống Quản Lý Bãi Đỗ Xe Thông Minh (Smart Parking System - SPS)</div>
        </div>
        <div class="meta-box">
            <div><strong>Nhóm sinh viên:</strong> Phạm Văn Đạt, Nguyễn Duy Bảo, Trần Tuấn Anh</div>
            <div><strong>Thời điểm báo cáo:</strong> 24/09/2026</div>
            <div><strong>Tiến độ thực tế:</strong> <strong>ĐÃ HOÀN THÀNH 95% MỤC TIÊU</strong></div>
        </div>
    </div>

    <!-- 4 KHUNG KPI CHỈ SỐ -->
    <div class="kpi-row">
        <div class="kpi-box">
            <div class="kpi-num">95%</div>
            <div class="kpi-label">Tiến Độ Tổng Thể</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-num">5 / 5 Phases</div>
            <div class="kpi-label">Giai Đoạn Cốt Lõi</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-num">11 / 11 Passed</div>
            <div class="kpi-label">Automated Unit Tests</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-num">MAE ~ 5.8%</div>
            <div class="kpi-label">Sai Số Mô Hình AI</div>
        </div>
    </div>

    <!-- MỤC 1: TÓM TẮT TRẢ LỜI CÔ GIÁO -->
    <div class="section-title">1. Tóm Tắt Trả Lời: "Dự Án Hiện Tại Đã Làm Được Những Gì?"</div>
    <div class="highlight-box">
        <strong>Kính gửi Cô giáo hướng dẫn:</strong> Dự án <em>Smart Parking System</em> hiện đã hoàn thiện toàn diện phần mềm từ <strong>Backend API &rarr; Thuật toán &amp; AI &rarr; Giao diện Frontend thời gian thực</strong>. Toàn bộ các chức năng đã kết nối chạy thông suốt từ đầu đến cuối (End-to-End) và sẵn sàng để demo trực tiếp:
        <ul>
            <li><strong>Đã xây dựng xong Hệ thống CSDL &amp; Xác thực:</strong> 6 bảng cơ sở dữ liệu quan hệ trên PostgreSQL qua SQLAlchemy ORM và Alembic; bảo mật băm mật khẩu Bcrypt, xác thực JWT token và phân quyền 3 vai trò (Admin, Staff, Customer).</li>
            <li><strong>Đã giải quyết triệt để bài toán Đặt chỗ &amp; Vé QR:</strong> Quản lý sơ đồ slot, tự động sinh mã QR vé điện tử (Base64), xử lý Check-in / Check-out tại barrier cổng và áp dụng <strong>khóa cấp hàng (Row-Level Locking)</strong> chống 100% tình trạng 2 người đặt trùng 1 ô (Double-Booking).</li>
            <li><strong>Đã làm chủ Thuật toán tìm đường ngắn nhất A* (Pathfinding):</strong> Cài đặt giải thuật A* trên ma trận lưới 2D, tự động tìm đường ngắn nhất né tường/cột và né xe đang đỗ từ Cổng vào (0, 0) đến ô đỗ mục tiêu với độ trễ siêu tốc &lt; 5ms.</li>
            <li><strong>Đã huấn luyện Mô hình Trí tuệ nhân tạo (Machine Learning):</strong> Huấn luyện mô hình Random Forest Regressor trên tập dữ liệu lịch sử 4,320 mẫu, dự báo chính xác tỷ lệ lấp đầy bãi xe trong 24 giờ tới với sai số tuyệt đối cực thấp (MAE ~ 5.8%).</li>
            <li><strong>Đã hoàn thiện Giao diện Web điều hành Dark Cyberpunk:</strong> Giao diện SPA Vue 3 + Tailwind CSS tích hợp diễn hoạt <strong>GSAP</strong> cho xe ảo lăn bánh bẻ lái mượt mà theo lộ trình A*, biểu đồ AI 24h kèm thanh trượt tương tác và bộ đếm KPI số liệu thực tế.</li>
        </ul>
    </div>

    <!-- MỤC 2: BẢNG CHI TIẾT TỪNG PHÂN HỆ ĐÃ HOÀN THÀNH -->
    <div class="section-title">2. Bảng Thống Kê Chi Tiết Các Hạng Mục Kỹ Thuật Đã Hoàn Thành</div>
    <table>
        <thead>
            <tr>
                <th style="width: 22%;">Phân Hệ Công Việc</th>
                <th style="width: 48%;">Nội Dung Kỹ Thuật Đã Thực Hiện &amp; Kết Quả</th>
                <th style="width: 18%;">Minh Chứng / Mã Nguồn</th>
                <th style="width: 12%;" class="text-center">Kết Quả</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>1. CSDL &amp; Backend Core</strong></td>
                <td>Thiết kế ERD 6 bảng (Users, Lots, Slots, Bookings, Sessions, History), migration Alembic, cấu hình CORS, no-cache headers và FastAPI server.</td>
                <td><code>app/main.py</code><br><code>app/models/*</code></td>
                <td class="text-center"><span class="tag-done">100% Xong</span></td>
            </tr>
            <tr>
                <td><strong>2. Bảo Mật &amp; Phân Quyền</strong></td>
                <td>Mã hóa bcrypt, cấp phát &amp; giải mã JWT Bearer, phân quyền Role-Based Access Control (Admin, Staff, Customer), bảo vệ các endpoint.</td>
                <td><code>core/security.py</code><br><code>routers/auth.py</code></td>
                <td class="text-center"><span class="tag-done">100% Xong</span></td>
            </tr>
            <tr>
                <td><strong>3. Đặt Chỗ, QR &amp; Khóa Hàng</strong></td>
                <td>Quy trình đặt chỗ, sinh mã QR vé Base64, Check-in/out barrier, áp dụng khóa <code>with_for_update()</code> chống xung đột giao dịch đồng thời.</td>
                <td><code>services/booking_service.py</code><br><code>test_double_booking.py</code></td>
                <td class="text-center"><span class="tag-done">100% Xong</span></td>
            </tr>
            <tr>
                <td><strong>4. Thuật Toán Tìm Đường A*</strong></td>
                <td>Biểu diễn lưới 2D độc lập thuần Python, hàm Heuristic Manhattan tối ưu, né vật cản tĩnh/động, API trả về mảng tọa độ (waypoints).</td>
                <td><code>app/pathfinding/*</code><br><code>tests/test_astar.py</code></td>
                <td class="text-center"><span class="tag-done">6/6 Tests Pass</span></td>
            </tr>
            <tr>
                <td><strong>5. Mô Hình Học Máy (ML)</strong></td>
                <td>Sinh 4,320 mẫu dữ liệu lịch sử chuẩn chu kỳ, train Random Forest (200 cây, max depth 10), xuất model <code>.joblib</code>, API dự báo 24h.</td>
                <td><code>app/ml_engine/*</code><br><code>test_ml_engine.py</code></td>
                <td class="text-center"><span class="tag-done">5/5 Tests Pass</span></td>
            </tr>
            <tr>
                <td><strong>6. Giao Diện &amp; Diễn Hoạt GSAP</strong></td>
                <td>Giao diện điều hành Cyberpunk Vue 3, xe ảo lăn bánh bám lộ trình A*, biểu đồ AI với thanh trượt scrubber, chế độ Mock chạy offline.</td>
                <td><code>frontend/index.html</code><br><code>frontend/src/*</code></td>
                <td class="text-center"><span class="tag-done">100% Xong</span></td>
            </tr>
            <tr>
                <td><strong>7. Realtime WebSocket</strong></td>
                <td>Kênh truyền dữ liệu Full-Duplex hai chiều, đo RTT latency Ping/Pong, broadcast cập nhật trạng thái bãi xe thời gian thực.</td>
                <td><code>core/websocket_manager.py</code><br><code>routers/websocket.py</code></td>
                <td class="text-center"><span class="tag-done">100% Xong</span></td>
            </tr>
        </tbody>
    </table>

    <div class="footer-note">
        <div>Báo Cáo Tiến Độ Dự Án Smart Parking System — Gửi Giảng Viên Hướng Dẫn</div>
        <div>Trang 1 / 2</div>
    </div>

    <!-- ==================== TRANG 2 ==================== -->
    <div class="page-break"></div>

    <div class="academic-header">
        <div>
            <div class="doc-title">BÁO CÁO KẾT QUẢ ĐÃ HOÀN THÀNH CỦA DỰ ÁN (TIẾP THEO)</div>
            <div class="doc-subtitle">Hệ Thống Quản Lý Bãi Đỗ Xe Thông Minh (Smart Parking System - SPS)</div>
        </div>
        <div class="meta-box">
            <div><strong>Phần II:</strong> Minh Chứng Giao Diện Thực Tế, Kết Quả Kiểm Thử &amp; Demo</div>
        </div>
    </div>

    <!-- MỤC 3: HÌNH ẢNH MINH CHỨNG THỰC TẾ -->
    <div class="section-title">3. Hình Ảnh Minh Chứng Hệ Thống Đang Chạy Thực Tế</div>
    <div class="image-grid">
        <div class="image-card">
            <img src="{img_auth}" alt="Màn hình đăng nhập">
            <div class="image-desc">Hình 1: Màn hình Đăng nhập / Phân quyền bảo mật JWT và bảo vệ giao diện</div>
        </div>
        <div class="image-card">
            <img src="{img_dashboard}" alt="Bảng điều khiển bãi xe">
            <div class="image-desc">Hình 2: Bảng điều khiển trung tâm tích hợp sơ đồ A*, xe chạy GSAP và dự báo AI 24h</div>
        </div>
    </div>

    <!-- MỤC 4: KẾT QUẢ KIỂM THỬ ĐỘ TIN CẬY -->
    <div class="section-title">4. Kết Quả Kiểm Thử Tự Động &amp; Đánh Giá Chất Lượng Phần Mềm (QA)</div>
    <table>
        <thead>
            <tr>
                <th style="width: 25%;">Hạng Mục Kiểm Thử</th>
                <th style="width: 45%;">Kịch Bản Kiểm Tra Chuyên Sâu</th>
                <th style="width: 18%;">Công Cụ / Framework</th>
                <th style="width: 12%;" class="text-center">Tỷ Lệ Đạt</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Kiểm thử thuật toán A*</strong></td>
                <td>Kiểm tra 6 kịch bản: đường thẳng, né vật cản zíc zắc, bãi xe bị chặn hoàn toàn, điểm xuất phát trùng đích, độ dài đường đi tối ưu Manhattan.</td>
                <td>Pytest (Python 3.11)</td>
                <td class="text-center"><strong>6 / 6 (100%)</strong></td>
            </tr>
            <tr>
                <td><strong>Kiểm thử mô hình AI (ML)</strong></td>
                <td>Kiểm tra dữ liệu synthetic, tính tái lập theo seed, quy luật giờ đêm thấp hơn giờ cao điểm, mô hình hội tụ và dự báo trong khoảng [0, 1].</td>
                <td>Pytest / Scikit-learn</td>
                <td class="text-center"><strong>5 / 5 (100%)</strong></td>
            </tr>
            <tr>
                <td><strong>Kiểm thử chống Double-Booking</strong></td>
                <td>Mô phỏng 2 thread khách cùng lúc bấm đặt 1 vị trí đỗ tại cùng 1 mili-giây &rarr; khóa hàng Row-level lock chặn chính xác 1 thành công và 1 lỗi 409.</td>
                <td>Multi-threading Concurrency</td>
                <td class="text-center"><strong>Đạt 100%</strong></td>
            </tr>
            <tr>
                <td><strong>Kiểm thử giao diện E2E</strong></td>
                <td>Kiểm thử tự động trên trình duyệt thật (Edge headless qua CDP): Đăng xuất, Đăng nhập 1 chạm, Render 25 ô đỗ, nhận diện token và giải phóng RAM.</td>
                <td>Chrome DevTools Protocol</td>
                <td class="text-center"><strong>Đạt 100%</strong></td>
            </tr>
        </tbody>
    </table>

    <!-- MỤC 5: HƯỚNG DẪN TRÌNH CHIẾU DEMO CHO CÔ GIÁO -->
    <div class="section-title">5. Hướng Dẫn Trình Chiếu Demo Trực Tiếp Cho Cô Giáo</div>
    <div class="highlight-box">
        <strong>Cách khởi chạy hệ thống để demo cho cô giáo (Chỉ mất 5 giây):</strong>
        <ul>
            <li><strong>Bước 1:</strong> Vào thư mục dự án <code>D:\\smart-parking-system</code>, nhấp đúp chuột vào file <strong><code>run.bat</code></strong>.</li>
            <li><strong>Bước 2:</strong> Mở trình duyệt web truy cập địa chỉ: <strong><code>http://localhost:8000</code></strong>.</li>
            <li><strong>Bước 3: Thực hiện 4 kịch bản demo trực quan nhất:</strong>
                <br>1. Bấm nút <strong>"Quick Admin Login"</strong> để đăng nhập 1 chạm vào bảng điều khiển.
                <br>2. Bấm vào bất kỳ ô đỗ nào còn <strong>Trống (Màu xanh ngọc)</strong> &rarr; Chiếc xe ảo sẽ tự lăn bánh và bẻ lái theo thuật toán <strong>A*</strong> từ Cổng vào (0, 0) đến đúng ô đỗ.
                <br>3. Bấm <strong>"Đặt Chỗ Nhanh"</strong> &rarr; Nhập biển số &rarr; Xem mã vé <strong>QR Code điện tử</strong> tự động sinh ra.
                <br>4. Kéo thanh trượt <strong>Scrubber 24h</strong> tại bảng Dự Báo Lấp Đầy &rarr; Xem công suất bãi xe biến thiên theo mô hình <strong>Random Forest AI</strong>.
            </li>
        </ul>
    </div>

    <!-- MỤC 6: KẾT LUẬN & ĐỊNH HƯỚNG BƯỚC TIẾP THEO -->
    <div class="section-title">6. Kế Hoạch Hoàn Thiện Bước Tiếp Theo &amp; Lời Cảm Ơn</div>
    <p style="margin: 0 0 5px 0; font-size: 9.5px; color: #334155;">
        Nhóm đang tiến hành hoàn thiện nốt 5% khối lượng công việc mở rộng còn lại: (1) Bổ sung kịch bản tìm kiếm bãi xe lân cận theo bán kính GPS khi bãi chính hết chỗ, (2) Đóng gói Docker Compose phục vụ triển khai Cloud. Nhóm xin chân thành cảm ơn sự hướng dẫn tận tình của Cô giáo!
    </p>

    <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 9.5px;">
        <div style="width: 45%; text-align: center;">
            <strong>Ý KIẾN CỦA GIẢNG VIÊN HƯỚNG DẪN</strong><br>
            <span style="font-size: 8.5px; color: #64748b;">(Ký và ghi rõ họ tên)</span>
            <div style="height: 38px;"></div>
        </div>
        <div style="width: 45%; text-align: center;">
            <strong>ĐẠI DIỆN NHÓM SINH VIÊN</strong><br>
            <span style="font-size: 8.5px; color: #64748b;">(Ký và ghi rõ họ tên)</span>
            <div style="height: 38px;"></div>
            <strong>Phạm Văn Đạt</strong>
        </div>
    </div>

    <div class="footer-note">
        <div>Báo Cáo Tiến Độ Dự Án Smart Parking System — Gửi Giảng Viên Hướng Dẫn</div>
        <div>Trang 2 / 2</div>
    </div>

</body>
</html>
"""

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML teacher report saved to: {HTML_FILE}")

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
        alt_download = os.path.abspath(r"C:\Users\LENOVO\Downloads\bao_cao_ket_qua_du_an_gui_giang_vien_v2.pdf")
        shutil.copy2(PDF_FILE, alt_download)
        print(f"SUCCESS! Created PDF: {PDF_FILE} and copied to alternative: {alt_download}")

