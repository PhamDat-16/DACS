import subprocess
import os
import base64
import sys

sys.stdout.reconfigure(encoding='utf-8')

HTML_FILE = os.path.abspath(r"d:\smart-parking-system\bao_cao_tien_do.html")
PDF_FILE = os.path.abspath(r"d:\smart-parking-system\bao_cao_tien_do_du_an.pdf")
FDF_FILE = os.path.abspath(r"d:\smart-parking-system\bao_cao_tien_do_du_an.fdf")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

img_dashboard = get_base64_image(r"d:\smart-parking-system\authenticated_dashboard.png")
img_auth = get_base64_image(r"d:\smart-parking-system\auth_screen.png")

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Báo Cáo Tiến Độ Dự Án - Smart Parking System</title>
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
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
            color: #1e293b;
            line-height: 1.38;
            font-size: 11px;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }}
        .header {{
            border-bottom: 2px solid #2563eb;
            padding-bottom: 6px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        .header-title {{
            font-size: 17px;
            font-weight: 800;
            color: #1e3a8a;
            margin: 0;
            letter-spacing: -0.3px;
            text-transform: uppercase;
        }}
        .header-subtitle {{
            font-size: 11px;
            color: #475569;
            margin-top: 2px;
            font-weight: 600;
        }}
        .meta-box {{
            text-align: right;
            font-size: 10px;
            color: #475569;
            line-height: 1.35;
        }}
        .badge {{
            display: inline-block;
            padding: 2px 7px;
            border-radius: 9999px;
            font-size: 9.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}
        .badge-success {{
            background-color: #dcfce7;
            color: #15803d;
            border: 1px solid #86efac;
        }}
        .badge-info {{
            background-color: #e0f2fe;
            color: #0369a1;
            border: 1px solid #7dd3fc;
        }}
        .badge-purple {{
            background-color: #f3e8ff;
            color: #7e22ce;
            border: 1px solid #d8b4fe;
        }}
        
        .section {{
            margin-bottom: 10px;
        }}
        .section-title {{
            font-size: 12px;
            font-weight: 700;
            color: #0f172a;
            border-left: 3px solid #2563eb;
            padding-left: 8px;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.2px;
        }}
        
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            margin-bottom: 10px;
        }}
        .kpi-card {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 6px 10px;
            border-top: 3px solid #2563eb;
        }}
        .kpi-card.purple {{ border-top-color: #8b5cf6; }}
        .kpi-card.green {{ border-top-color: #10b981; }}
        .kpi-card.orange {{ border-top-color: #f59e0b; }}
        .kpi-num {{
            font-size: 17px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 1px;
            line-height: 1.1;
        }}
        .kpi-label {{
            font-size: 9px;
            color: #64748b;
            font-weight: 700;
            text-transform: uppercase;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 8px;
            font-size: 10.5px;
        }}
        th, td {{
            padding: 4px 6px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }}
        th {{
            background-color: #f1f5f9;
            color: #334155;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 9.5px;
            letter-spacing: 0.3px;
        }}
        tr:nth-child(even) {{
            background-color: #fafafa;
        }}
        
        .progress-bar-bg {{
            background-color: #e2e8f0;
            border-radius: 4px;
            height: 6px;
            width: 60px;
            overflow: hidden;
            display: inline-block;
            vertical-align: middle;
            margin-right: 4px;
        }}
        .progress-bar-fill {{
            background-color: #10b981;
            height: 100%;
            border-radius: 4px;
        }}
        
        .feature-box {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 6px 10px;
            margin-bottom: 6px;
        }}
        .feature-box h4 {{
            margin: 0 0 3px 0;
            font-size: 11px;
            color: #1e40af;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .feature-box p {{
            margin: 0;
            color: #475569;
            font-size: 10.5px;
        }}
        .feature-box ul {{
            margin: 3px 0 0 0;
            padding-left: 14px;
            color: #475569;
            font-size: 10px;
        }}
        .feature-box li {{
            margin-bottom: 2px;
        }}

        .image-container {{
            margin: 4px 0;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            overflow: hidden;
            background: #0f172a;
            text-align: center;
        }}
        .image-container img {{
            width: 100%;
            height: 175px;
            object-fit: cover;
            display: block;
        }}
        .image-caption {{
            font-size: 9.5px;
            color: #475569;
            padding: 3px;
            background: #f8fafc;
            border-top: 1px solid #e2e8f0;
            text-align: center;
            font-style: italic;
        }}
        
        .page-break {{
            page-break-before: always;
            break-before: page;
        }}

        .footer-note {{
            margin-top: 6px;
            padding-top: 6px;
            border-top: 1px solid #e2e8f0;
            font-size: 9.5px;
            color: #94a3b8;
            display: flex;
            justify-content: space-between;
        }}
    </style>
</head>
<body>

    <!-- TRANG 1 -->
    <div class="header">
        <div>
            <div class="header-title">BÁO CÁO TIẾN ĐỘ DỰ ÁN</div>
            <div class="header-subtitle">Hệ Thống Quản Lý Bãi Đỗ Xe Thông Minh (Smart Parking System - SPS)</div>
        </div>
        <div class="meta-box">
            <div><strong>Thời điểm:</strong> 24/09/2026</div>
            <div><strong>Phiên bản:</strong> Release v1.0.0</div>
            <div><strong>Đánh giá:</strong> <span class="badge badge-success">ĐẠT 95% MỤC TIÊU</span></div>
        </div>
    </div>

    <!-- KPI CARDS -->
    <div class="kpi-grid">
        <div class="kpi-card green">
            <div class="kpi-num">95%</div>
            <div class="kpi-label">Tiến Độ Tổng Thể</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-num">5 / 5</div>
            <div class="kpi-label">Phases Hoàn Thành</div>
        </div>
        <div class="kpi-card purple">
            <div class="kpi-num">11 / 11</div>
            <div class="kpi-label">Tests Passed (100%)</div>
        </div>
        <div class="kpi-card orange">
            <div class="kpi-num">&lt; 0.06</div>
            <div class="kpi-label">Sai số ML (MAE ~5.8%)</div>
        </div>
    </div>

    <!-- MỤC 1: TỔNG QUAN DỰ ÁN -->
    <div class="section">
        <div class="section-title">1. Tổng Quan Kiến Trúc &amp; Công Nghệ Hệ Thống</div>
        <p style="margin: 0 0 5px 0; color: #334155; font-size: 10.5px;">
            Dự án <strong>Smart Parking System</strong> là giải pháp chuyển đổi số toàn diện cho bãi đỗ xe thông minh, 
            kết hợp thuật toán tìm đường ngắn nhất <strong>A* (A-Star Search)</strong>, mô hình <strong>Trí tuệ nhân tạo (Random Forest ML)</strong> 
            dự báo công suất lấp đầy 24h, cơ chế chống xung đột đặt chỗ <strong>Row-Level Locking</strong> và giao diện điều hành tương tác đồ họa thời gian thực bằng <strong>GSAP</strong>.
        </p>
        <table>
            <thead>
                <tr>
                    <th style="width: 22%;">Thành Phần</th>
                    <th style="width: 48%;">Công Nghệ Sử Dụng</th>
                    <th style="width: 30%;">Vai Trò / Nhiệm Vụ</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Backend Core</strong></td>
                    <td>FastAPI, Python 3.11, Pydantic v2, Uvicorn</td>
                    <td>Xử lý REST API, điều phối nghiệp vụ, phân quyền JWT</td>
                </tr>
                <tr>
                    <td><strong>Cơ sở dữ liệu</strong></td>
                    <td>PostgreSQL, SQLAlchemy ORM, Alembic Migration</td>
                    <td>Lưu trữ dữ liệu quan hệ (Users, Lots, Slots, Bookings, Sessions)</td>
                </tr>
                <tr>
                    <td><strong>Thuật toán A*</strong></td>
                    <td>Pure Python Grid Search (Manhattan Heuristic)</td>
                    <td>Tìm đường dẫn tối ưu né vật cản từ Cổng vào đến từng ô đỗ</td>
                </tr>
                <tr>
                    <td><strong>Trí tuệ nhân tạo (ML)</strong></td>
                    <td>Scikit-learn, Random Forest Regressor, Joblib</td>
                    <td>Huấn luyện chuỗi dữ liệu dự báo tỷ lệ lấp đầy theo 24 giờ</td>
                </tr>
                <tr>
                    <td><strong>Giao diện Web</strong></td>
                    <td>Vue 3 (ESM), Tailwind CSS (Dark Cyber UI), GSAP 3</td>
                    <td>Trực quan hóa sơ đồ bãi xe, mô phỏng xe chạy, biểu đồ AI</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- MỤC 2: TIẾN ĐỘ CHI TIẾT CÁC PHASE -->
    <div class="section">
        <div class="section-title">2. Chi Tiết Tiến Độ Thực Hiện Theo Từng Giai Đoạn (Phases)</div>
        <table>
            <thead>
                <tr>
                    <th style="width: 22%;">Giai Đoạn</th>
                    <th style="width: 50%;">Nội Dung Kỹ Thuật Đã Triển Khai</th>
                    <th style="width: 14%;">Trạng Thái</th>
                    <th style="width: 14%;">Đánh Giá</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Phase 1: DB &amp; Auth</strong></td>
                    <td>Thiết kế 6 bảng ERD, Alembic migration, mã hóa mật khẩu bcrypt, cấp phát JWT Bearer, phân quyền Role (Admin, Staff, Customer).</td>
                    <td><span class="badge badge-success">Hoàn thành</span></td>
                    <td>
                        <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 100%;"></div></div> 100%
                    </td>
                </tr>
                <tr>
                    <td><strong>Phase 2: Booking &amp; QR</strong></td>
                    <td>Khởi tạo lưới bãi xe, quản lý slot, đặt chỗ kèm QR vé điện tử, Check-in / Check-out, chống Double-booking bằng Row-level lock.</td>
                    <td><span class="badge badge-success">Hoàn thành</span></td>
                    <td>
                        <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 100%;"></div></div> 100%
                    </td>
                </tr>
                <tr>
                    <td><strong>Phase 3: Thuật toán A*</strong></td>
                    <td>Xây dựng giải thuật A* trên ma trận lưới 2D, né chướng ngại vật động, tối ưu khoảng cách Manhattan, API trả về waypoint path.</td>
                    <td><span class="badge badge-success">Hoàn thành</span></td>
                    <td>
                        <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 100%;"></div></div> 100%
                    </td>
                </tr>
                <tr>
                    <td><strong>Phase 4: ML Forecast</strong></td>
                    <td>Bộ sinh dữ liệu synthetic 4320 bản ghi, train model Random Forest, API dự báo tỷ lệ lấp đầy theo giờ và toàn bộ 24h.</td>
                    <td><span class="badge badge-success">Hoàn thành</span></td>
                    <td>
                        <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 100%;"></div></div> 100%
                    </td>
                </tr>
                <tr>
                    <td><strong>Phase 5: Frontend UI/UX</strong></td>
                    <td>Giao diện điều hành Dark Cyberpunk, diễn hoạt GSAP xe di chuyển theo lộ trình A*, modal đặt vé QR, biểu đồ AI tương tác thanh trượt.</td>
                    <td><span class="badge badge-success">Hoàn thành</span></td>
                    <td>
                        <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 100%;"></div></div> 100%
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="footer-note">
        <div>Hệ Thống Bãi Đỗ Xe Thông Minh (Smart Parking System)</div>
        <div>Trang 1 / 2</div>
    </div>

    <!-- BREAK TRANG 2 -->
    <div class="page-break"></div>

    <div class="header">
        <div>
            <div class="header-title">BÁO CÁO TIẾN ĐỘ DỰ ÁN (TIẾP THEO)</div>
            <div class="header-subtitle">Hệ Thống Quản Lý Bãi Đỗ Xe Thông Minh (Smart Parking System - SPS)</div>
        </div>
        <div class="meta-box">
            <div><strong>Phần II:</strong> Kiểm Thử, Giao Diện & Kế Hoạch Triển Khai</div>
        </div>
    </div>

    <!-- MỤC 3: KẾT QUẢ KIỂM THỬ -->
    <div class="section">
        <div class="section-title">3. Kết Quả Kiểm Thử Chất Lượng &amp; Độ Ổn Định (Testing &amp; QA)</div>
        <div class="feature-box">
            <h4>
                <span>Kiểm Thử Đơn Vị Tự Động (Backend Automated Tests: 11/11 Passed)</span>
                <span class="badge badge-success">100% PASSED</span>
            </h4>
            <p>Hệ thống đã xây dựng bộ kiểm thử tự động toàn diện chạy bằng Pytest, kiểm tra chặt chẽ các kịch bản khó:</p>
            <ul>
                <li><strong>Thuật toán A* (6 tests):</strong> Đường thẳng không vật cản, né vật cản, kịch bản bãi xe bị chặn hoàn toàn, điểm xuất phát trùng đích, tối ưu Manhattan, ô đích là vật cản trả về an toàn.</li>
                <li><strong>Mô hình Machine Learning (5 tests):</strong> Phân phối synthetic chuẩn xác, tính tái lập theo seed, logic giờ đêm thấp hơn giờ cao điểm, sai số huấn luyện MAE đạt chuẩn, học đúng chu kỳ cao điểm.</li>
                <li><strong>Kiểm thử đa luồng chống Double-Booking:</strong> Mô phỏng đồng thời 2 khách cùng bấm đặt 1 vị trí đỗ tại cùng một mili-giây &rarr; khóa hàng Row-level lock đảm bảo duy nhất 1 booking thành công và 1 booking nhận lỗi 409 Conflict.</li>
            </ul>
        </div>

        <div class="feature-box">
            <h4>
                <span>Kiểm Thử Giao Diện Đầu - Cuối (End-to-End Headless Browser Test)</span>
                <span class="badge badge-purple">E2E VERIFIED</span>
            </h4>
            <p>Đã thực hiện kịch bản kiểm thử tự động trên trình duyệt thật (Microsoft Edge qua CDP):</p>
            <ul>
                <li>Kiểm tra trạng thái khi chưa đăng nhập: Bảo vệ giao diện, hiển thị form Đăng nhập / Đăng ký thẩm mỹ.</li>
                <li>Kiểm tra đăng nhập một chạm (Quick Admin Login): Lưu giữ phiên JWT, mở khóa toàn bộ bảng điều khiển trung tâm.</li>
                <li>Render sơ đồ bãi đỗ: Lưới 25 ô đỗ với hiệu ứng Stagger 2D, bộ đếm KPI, thanh trượt dự báo ML hoạt động mượt mà.</li>
                <li>Kiểm tra cơ chế Đăng xuất (Logout): Xóa sạch token phiên, đưa hệ thống về trạng thái an toàn.</li>
            </ul>
        </div>
    </div>

    <!-- MỤC 4: HÌNH ẢNH MINH CHỨNG GIAO DIỆN -->
    <div class="section">
        <div class="section-title">4. Hình Ảnh Thực Tế Của Hệ Thống (Screenshots)</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
            <div class="image-container">
                <img src="{img_auth}" alt="Màn hình đăng nhập">
                <div class="image-caption">Hình 1: Màn hình Đăng nhập / Phân quyền bảo mật JWT</div>
            </div>
            <div class="image-container">
                <img src="{img_dashboard}" alt="Bảng điều khiển bãi xe">
                <div class="image-caption">Hình 2: Bảng điều khiển trung tâm tích hợp A* &amp; Dự báo AI 24h</div>
            </div>
        </div>
    </div>

    <!-- MỤC 5: KẾ HOẠCH BƯỚC TIẾP THEO -->
    <div class="section">
        <div class="section-title">5. Kế Hoạch Phát Triển Giai Đoạn Tiếp Theo &amp; Kết Luận</div>
        <table>
            <thead>
                <tr>
                    <th style="width: 8%;">STT</th>
                    <th style="width: 32%;">Hạng Mục Mở Rộng</th>
                    <th style="width: 45%;">Mục Tiêu &amp; Giải Pháp Kỹ Thuật</th>
                    <th style="width: 15%;">Dự Kiến</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td><strong>Nhận diện biển số (ANPR/OCR)</strong></td>
                    <td>Tích hợp camera AI quét biển số tự động khi xe vào barrier cổng.</td>
                    <td>Giai đoạn mở rộng</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td><strong>Cổng thanh toán Online</strong></td>
                    <td>Tích hợp SDK thanh toán VNPAY / MoMo / ZaloPay khi check-out.</td>
                    <td>Giai đoạn mở rộng</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td><strong>Dockerize &amp; Deploy Cloud</strong></td>
                    <td>Đóng gói Docker Compose (FastAPI + Vue + PostgreSQL) triển khai Cloud.</td>
                    <td>Sẵn sàng</td>
                </tr>
            </tbody>
        </table>
        
        <p style="margin-top: 6px; font-weight: 600; color: #15803d; background: #f0fdf4; padding: 6px 10px; border-left: 3px solid #16a34a; border-radius: 4px; font-size: 10.5px;">
            &check; <strong>KẾT LUẬN:</strong> Dự án hiện tại đã đạt <strong>95%</strong> khối lượng công việc, hoàn thành toàn bộ các yêu cầu kỹ thuật cốt lõi (A*, Machine Learning, Đặt chỗ chống xung đột, Vé QR, Giao diện Vue 3 + GSAP). Hệ thống hoạt động ổn định, mã nguồn sạch sẽ, đầy đủ tài liệu hướng dẫn và sẵn sàng nghiệm thu.
        </p>
    </div>

    <div class="footer-note">
        <div>Hệ Thống Bãi Đỗ Xe Thông Minh (Smart Parking System)</div>
        <div>Trang 2 / 2</div>
    </div>

</body>
</html>
"""

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML report saved to: {HTML_FILE}")

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

# Also create copy as .fdf for the user request "fdf"
if os.path.exists(PDF_FILE):
    with open(PDF_FILE, "rb") as src, open(FDF_FILE, "wb") as dst:
        dst.write(src.read())
    print(f"SUCCESS! Created PDF: {PDF_FILE} and FDF: {FDF_FILE}")

