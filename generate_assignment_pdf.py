import subprocess
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

HTML_FILE = os.path.abspath(r"d:\smart-parking-system\phan_cong_nhiem_vu.html")
PDF_FILE = os.path.abspath(r"d:\smart-parking-system\phan_cong_nhiem_vu_nhom.pdf")
DOWNLOAD_PDF = os.path.abspath(r"C:\Users\LENOVO\Downloads\phan_cong_nhiem_vu_nhom.pdf")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Bảng Phân Công Nhiệm Vụ Dự Án - Smart Parking System</title>
    <style>
        @page {
            size: A4;
            margin: 10mm 12mm 10mm 12mm;
        }
        * {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Times New Roman', Roboto, Arial, sans-serif;
            color: #1e293b;
            line-height: 1.35;
            font-size: 10.5px;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }
        
        /* HEADER TRANG TRỌNG, THANH LỊCH */
        .doc-header {
            border-bottom: 1.5px solid #0f172a;
            padding-bottom: 6px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }
        .doc-title {
            font-size: 16px;
            font-weight: 800;
            color: #0f172a;
            margin: 0;
            letter-spacing: -0.2px;
            text-transform: uppercase;
        }
        .doc-subtitle {
            font-size: 10.5px;
            color: #475569;
            margin-top: 2px;
            font-weight: 600;
        }
        .meta-info {
            text-align: right;
            font-size: 9.5px;
            color: #334155;
            line-height: 1.35;
        }

        .section-title {
            font-size: 11px;
            font-weight: 800;
            color: #0f172a;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            margin: 8px 0 5px 0;
            padding-left: 6px;
            border-left: 3px solid #334155;
        }

        /* BẢNG BIỂU CHUẨN MỰC, TỐI GIẢN */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 8px;
            font-size: 10px;
            background-color: #ffffff;
        }
        th, td {
            border: 1px solid #cbd5e1;
            padding: 5px 7px;
            text-align: left;
            vertical-align: top;
        }
        th {
            background-color: #f1f5f9;
            color: #0f172a;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 9px;
            letter-spacing: 0.2px;
        }
        .text-center { text-align: center; }
        .text-bold { font-weight: 700; }
        
        .tag {
            display: inline-block;
            padding: 1px 5px;
            border-radius: 3px;
            font-size: 9px;
            font-weight: 600;
            border: 1px solid #94a3b8;
            background: #f8fafc;
            color: #0f172a;
        }
        .tag-main {
            background: #e2e8f0;
            font-weight: 700;
            border-color: #64748b;
        }

        .page-break {
            page-break-before: always;
            break-before: page;
        }

        .footer-note {
            margin-top: 6px;
            padding-top: 5px;
            border-top: 1px solid #cbd5e1;
            font-size: 9px;
            color: #64748b;
            display: flex;
            justify-content: space-between;
        }

        /* KHUNG CHỮ KÝ */
        .sign-table {
            width: 100%;
            border-collapse: collapse;
            border: none;
            margin-top: 8px;
        }
        .sign-table td {
            border: none;
            text-align: center;
            vertical-align: top;
            padding: 4px;
            width: 33.33%;
        }
        .sign-box {
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            padding: 8px 6px;
            background: #fafafa;
        }
        .sign-role {
            font-size: 9.5px;
            font-weight: 700;
            color: #1e293b;
            text-transform: uppercase;
        }
        .sign-space {
            height: 34px;
        }
        .sign-name {
            font-size: 10.5px;
            font-weight: 800;
            color: #0f172a;
        }
    </style>
</head>
<body>

    <!-- ==================== TRANG 1 ==================== -->
    <div class="doc-header">
        <div>
            <div class="doc-title">BẢNG PHÂN CÔNG NHIỆM VỤ DỰ ÁN</div>
            <div class="doc-subtitle">Hệ Thống Quản Lý Bãi Đỗ Xe Thông Minh (Smart Parking System - SPS)</div>
        </div>
        <div class="meta-info">
            <div><strong>Nhóm sinh viên:</strong> 03 thành viên</div>
            <div><strong>Ngày thiết lập:</strong> 24/09/2026</div>
            <div><strong>Trạng thái:</strong> Đã thống nhất 100%</div>
        </div>
    </div>

    <!-- MỤC 1: TỔNG HỢP VAI TRÒ VÀ TỶ LỆ ĐÓNG GÓP -->
    <div class="section-title">1. Bảng Tổng Hợp Vai Trò &amp; Tỷ Lệ Đóng Góp Dự Án</div>
    <table>
        <thead>
            <tr>
                <th style="width: 5%;" class="text-center">STT</th>
                <th style="width: 20%;">Họ và Tên</th>
                <th style="width: 25%;">Vai Trò Đảm Nhiệm</th>
                <th style="width: 38%;">Phạm Vi Trách Nhiệm Chính</th>
                <th style="width: 12%;" class="text-center">Tỷ Lệ</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center text-bold">1</td>
                <td><strong>Phạm Văn Đạt</strong></td>
                <td><strong>Trưởng Nhóm / Backend &amp; Hệ Thống</strong></td>
                <td>Kiến trúc FastAPI, CSDL PostgreSQL, Auth JWT, Quản lý bãi xe, Đặt chỗ &amp; Chống Double-booking, WebSocket Server.</td>
                <td class="text-center text-bold">35%</td>
            </tr>
            <tr>
                <td class="text-center text-bold">2</td>
                <td><strong>Nguyễn Duy Bảo</strong></td>
                <td><strong>Kỹ Sư Giao Diện (Frontend &amp; UI/UX)</strong></td>
                <td>Giao diện Vue 3 + Tailwind Dark Cyber, Sơ đồ lưới bãi đỗ 2D, Diễn hoạt GSAP xe chạy, Biểu đồ AI tương tác &amp; WebSocket Client.</td>
                <td class="text-center text-bold">33%</td>
            </tr>
            <tr>
                <td class="text-center text-bold">3</td>
                <td><strong>Trần Tuấn Anh</strong></td>
                <td><strong>Kỹ Sư Thuật Toán &amp; AI (AI / ML Engineer)</strong></td>
                <td>Thuật toán tìm đường ngắn nhất A*, Mô hình hồi quy Random Forest dự báo công suất 24h, Sinh dữ liệu giả lập &amp; Unit test thuật toán.</td>
                <td class="text-center text-bold">32%</td>
            </tr>
        </tbody>
    </table>

    <!-- MỤC 2: MA TRẬN TRÁCH NHIỆM (RACI MATRIX) -->
    <div class="section-title">2. Ma Trận Phân Chia Trách Nhiệm Chi Tiết (RACI Matrix)</div>
    <table>
        <thead>
            <tr>
                <th style="width: 4%;" class="text-center">STT</th>
                <th style="width: 36%;">Phân Hệ / Hạng Mục Kỹ Thuật</th>
                <th style="width: 20%;" class="text-center">Phạm Văn Đạt</th>
                <th style="width: 20%;" class="text-center">Nguyễn Duy Bảo</th>
                <th style="width: 20%;" class="text-center">Trần Tuấn Anh</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center">1</td>
                <td>Thiết kế Kiến trúc Backend, ERD PostgreSQL &amp; Alembic</td>
                <td class="text-center"><span class="tag tag-main">Chịu trách nhiệm (R/A)</span></td>
                <td class="text-center"><span class="tag">Tham vấn (C)</span></td>
                <td class="text-center"><span class="tag">Tham vấn (C)</span></td>
            </tr>
            <tr>
                <td class="text-center">2</td>
                <td>Hệ thống Bảo mật, Băm Bcrypt &amp; Xác thực Token JWT</td>
                <td class="text-center"><span class="tag tag-main">Chịu trách nhiệm (R/A)</span></td>
                <td class="text-center"><span class="tag">Phối hợp UI (S)</span></td>
                <td class="text-center"><span class="tag">Theo dõi (I)</span></td>
            </tr>
            <tr>
                <td class="text-center">3</td>
                <td>Nghiệp vụ Đặt chỗ, Vé QR &amp; Khóa hàng chống Double-Booking</td>
                <td class="text-center"><span class="tag tag-main">Chịu trách nhiệm (R/A)</span></td>
                <td class="text-center"><span class="tag">Modal đặt vé (S)</span></td>
                <td class="text-center"><span class="tag">Tham vấn logic (C)</span></td>
            </tr>
            <tr>
                <td class="text-center">4</td>
                <td>Thuật toán tìm đường dẫn tối ưu A* (Pathfinding)</td>
                <td class="text-center"><span class="tag">Tích hợp API (S)</span></td>
                <td class="text-center"><span class="tag">Diễn hoạt vẽ path (S)</span></td>
                <td class="text-center"><span class="tag tag-main">Chịu trách nhiệm (R/A)</span></td>
            </tr>
            <tr>
                <td class="text-center">5</td>
                <td>Mô hình Machine Learning (Random Forest) dự báo lấp đầy 24h</td>
                <td class="text-center"><span class="tag">Lưu DB lịch sử (S)</span></td>
                <td class="text-center"><span class="tag">Vẽ biểu đồ (S)</span></td>
                <td class="text-center"><span class="tag tag-main">Chịu trách nhiệm (R/A)</span></td>
            </tr>
            <tr>
                <td class="text-center">6</td>
                <td>Thiết kế Giao diện Web SPA (Vue 3, Tailwind CSS)</td>
                <td class="text-center"><span class="tag">Cung cấp API (S)</span></td>
                <td class="text-center"><span class="tag tag-main">Chịu trách nhiệm (R/A)</span></td>
                <td class="text-center"><span class="tag">Góp ý UI (C)</span></td>
            </tr>
            <tr>
                <td class="text-center">7</td>
                <td>Lập trình hiệu ứng chuyển động GSAP 3 (Xe chạy, Stagger, Counter)</td>
                <td class="text-center"><span class="tag">Cung cấp tọa độ (S)</span></td>
                <td class="text-center"><span class="tag tag-main">Chịu trách nhiệm (R/A)</span></td>
                <td class="text-center"><span class="tag">Kiểm thử tọa độ (S)</span></td>
            </tr>
            <tr>
                <td class="text-center">8</td>
                <td>Kênh Realtime WebSocket truyền nhận trạng thái bãi xe</td>
                <td class="text-center"><span class="tag tag-main">Phía Server (R)</span></td>
                <td class="text-center"><span class="tag tag-main">Phía Client (R)</span></td>
                <td class="text-center"><span class="tag">Theo dõi (I)</span></td>
            </tr>
            <tr>
                <td class="text-center">9</td>
                <td>Kiểm thử tự động &amp; Xây dựng tài liệu đồ án</td>
                <td class="text-center"><span class="tag">Backend Tests</span></td>
                <td class="text-center"><span class="tag">Frontend E2E QA</span></td>
                <td class="text-center"><span class="tag">A* &amp; ML Tests</span></td>
            </tr>
        </tbody>
    </table>
    <div style="font-size: 8.5px; color: #64748b; margin-top: -4px;">
        * Định nghĩa RACI: <strong>R (Responsible)</strong>: Trực tiếp triển khai | <strong>A (Accountable)</strong>: Phụ trách chịu trách nhiệm | <strong>C (Consulted)</strong>: Đóng góp ý kiến chuyên môn | <strong>S (Support)</strong>: Hỗ trợ kỹ thuật | <strong>I (Informed)</strong>: Cập nhật thông tin.
    </div>

    <!-- MỤC 3: CHI TIẾT ĐẦU VIỆC THÀNH VIÊN 1 (PHẠM VĂN ĐẠT) -->
    <div class="section-title">3. Bảng Chi Tiết Đầu Việc &amp; Sản Phẩm Bàn Giao (Thành Viên 1: Phạm Văn Đạt)</div>
    <table>
        <thead>
            <tr>
                <th style="width: 5%;" class="text-center">STT</th>
                <th style="width: 25%;">Hạng Mục Công Việc</th>
                <th style="width: 45%;">Mô Tả Kỹ Thuật Chi Tiết</th>
                <th style="width: 25%;">Sản Phẩm Đầu Ra / Mã Nguồn</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center">1.1</td>
                <td>Khung Backend &amp; Khởi Chạy</td>
                <td>Xây dựng FastAPI server, pydantic-settings, CORS, middleware no-cache và script chạy tích hợp.</td>
                <td><code>app/main.py</code>, <code>run.bat</code>, <code>run.ps1</code></td>
            </tr>
            <tr>
                <td class="text-center">1.2</td>
                <td>Cơ Sở Dữ Liệu &amp; Migration</td>
                <td>Thiết kế 6 bảng quan hệ (Users, Lots, Slots, Bookings, Sessions, History), quản lý migration Alembic.</td>
                <td><code>app/models/*</code>, <code>alembic/*</code></td>
            </tr>
            <tr>
                <td class="text-center">1.3</td>
                <td>Bảo Mật &amp; Phân Quyền RBAC</td>
                <td>Mã hóa bcrypt, cấp phát JWT Bearer, phân quyền Admin, Staff và Customer cho toàn bộ API.</td>
                <td><code>app/core/security.py</code>, <code>app/routers/auth.py</code></td>
            </tr>
            <tr>
                <td class="text-center">1.4</td>
                <td>Đặt Chỗ &amp; Sinh Vé QR</td>
                <td>Xây dựng API đặt chỗ, tự động sinh mã QR Base64 vé điện tử, xử lý Check-in / Check-out tại bãi.</td>
                <td><code>app/services/booking_service.py</code>, <code>qr_service.py</code></td>
            </tr>
            <tr>
                <td class="text-center">1.5</td>
                <td>Chống Double-Booking</td>
                <td>Áp dụng Row-Level Locking (<code>SELECT FOR UPDATE</code>) đảm bảo tuyệt đối không xung đột đặt trùng ô đỗ.</td>
                <td><code>tests/test_double_booking.py</code></td>
            </tr>
            <tr>
                <td class="text-center">1.6</td>
                <td>Kênh Realtime WebSocket</td>
                <td>Xây dựng <code>ConnectionManager</code> phát sóng cập nhật trạng thái bãi xe tới toàn bộ clients theo thời gian thực.</td>
                <td><code>app/core/websocket_manager.py</code></td>
            </tr>
        </tbody>
    </table>

    <div class="footer-note">
        <div>Hệ Thống Bãi Đỗ Xe Thông Minh (Smart Parking System) — Phân Công Nhiệm Vụ</div>
        <div>Trang 1 / 2</div>
    </div>

    <!-- ==================== TRANG 2 ==================== -->
    <div class="page-break"></div>

    <div class="doc-header">
        <div>
            <div class="doc-title">BẢNG PHÂN CÔNG NHIỆM VỤ DỰ ÁN (TIẾP THEO)</div>
            <div class="doc-subtitle">Hệ Thống Quản Lý Bãi Đỗ Xe Thông Minh (Smart Parking System - SPS)</div>
        </div>
        <div class="meta-info">
            <div><strong>Phần II:</strong> Chi Tiết Phân Công, Quy Trình &amp; Xác Nhận</div>
        </div>
    </div>

    <!-- TIẾP MỤC 3: THÀNH VIÊN 2 (NGUYỄN DUY BẢO) -->
    <div class="section-title">3. Bảng Chi Tiết Đầu Việc &amp; Sản Phẩm Bàn Giao (Thành Viên 2: Nguyễn Duy Bảo - Frontend)</div>
    <table>
        <thead>
            <tr>
                <th style="width: 5%;" class="text-center">STT</th>
                <th style="width: 25%;">Hạng Mục Công Việc</th>
                <th style="width: 45%;">Mô Tả Kỹ Thuật Chi Tiết</th>
                <th style="width: 25%;">Sản Phẩm Đầu Ra / Mã Nguồn</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center">2.1</td>
                <td>Giao Diện Web SPA Điều Hành</td>
                <td>Xây dựng Single Page App phong cách Dark Cyberpunk bằng Vue 3 (Composition API) &amp; Tailwind CSS.</td>
                <td><code>frontend/index.html</code>, <code>frontend/src/app.js</code></td>
            </tr>
            <tr>
                <td class="text-center">2.2</td>
                <td>Sơ Đồ Lưới Bãi Đỗ Xe 2D</td>
                <td>Trực quan hóa ma trận 25 ô đỗ với 4 trạng thái: Trống (Xanh), Đã đặt (Vàng), Đang đỗ (Đỏ), Vật cản (Xám).</td>
                <td><code>frontend/src/components/ParkingGrid.js</code></td>
            </tr>
            <tr>
                <td class="text-center">2.3</td>
                <td>Diễn Hoạt GSAP Xe Di Chuyển</td>
                <td>Lập trình xe ảo lăn bánh bám sát tọa độ A*, tự động tính góc xoay đầu xe; dọn rác bộ nhớ bằng <code>gsap.context()</code>.</td>
                <td><code>frontend/src/app.js</code>, <code>gsap.min.js</code></td>
            </tr>
            <tr>
                <td class="text-center">2.4</td>
                <td>Biểu Đồ Dự Báo AI 24h &amp; Slider</td>
                <td>Vẽ đường cong tỷ lệ lấp đầy theo 24 giờ, tích hợp thanh trượt scrubber mượt mà bằng <code>gsap.utils.mapRange</code>.</td>
                <td><code>frontend/src/components/OccupancyForecast.js</code></td>
            </tr>
            <tr>
                <td class="text-center">2.5</td>
                <td>Modal Nghiệp Vụ &amp; Quét Vé QR</td>
                <td>Xây dựng Modal Đăng nhập/Đăng ký JWT, Modal Đặt chỗ kèm xem ảnh mã QR vé xe động, bộ đếm KPI thời gian thực.</td>
                <td><code>frontend/src/components/BookingModal.js</code></td>
            </tr>
            <tr>
                <td class="text-center">2.6</td>
                <td>Kết Nối API &amp; Standalone Mock</td>
                <td>Xây dựng API Client kết nối FastAPI, lắng nghe WebSocket và bộ giải thuật A* dự phòng chạy offline trên trình duyệt.</td>
                <td><code>frontend/src/api/client.js</code></td>
            </tr>
        </tbody>
    </table>

    <!-- TIẾP MỤC 3: THÀNH VIÊN 3 (TRẦN TUẤN ANH) -->
    <div class="section-title">3. Bảng Chi Tiết Đầu Việc &amp; Sản Phẩm Bàn Giao (Thành Viên 3: Trần Tuấn Anh - AI &amp; Thuật Toán)</div>
    <table>
        <thead>
            <tr>
                <th style="width: 5%;" class="text-center">STT</th>
                <th style="width: 25%;">Hạng Mục Công Việc</th>
                <th style="width: 45%;">Mô Tả Kỹ Thuật Chi Tiết</th>
                <th style="width: 25%;">Sản Phẩm Đầu Ra / Mã Nguồn</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center">3.1</td>
                <td>Mô Hình Hóa Lưới Tọa Độ 2D</td>
                <td>Biểu diễn bãi xe thành lưới ma trận 2D độc lập thuần Python, phân loại vật cản tĩnh và động.</td>
                <td><code>backend/app/pathfinding/grid.py</code></td>
            </tr>
            <tr>
                <td class="text-center">3.2</td>
                <td>Thuật Toán Tìm Đường A*</td>
                <td>Cài đặt giải thuật A* tìm đường ngắn nhất né vật cản từ Cổng vào (0, 0) đến ô đỗ mục tiêu theo khoảng cách Manhattan.</td>
                <td><code>backend/app/pathfinding/astar.py</code></td>
            </tr>
            <tr>
                <td class="text-center">3.3</td>
                <td>Dịch Vụ Định Tuyến Navigation</td>
                <td>Xây dựng navigation service và endpoint <code>GET /api/lots/{lot_id}/navigate</code> xuất chuỗi tọa độ (waypoints).</td>
                <td><code>app/services/navigate_service.py</code>, <code>routers/navigate.py</code></td>
            </tr>
            <tr>
                <td class="text-center">3.4</td>
                <td>Bộ Sinh Dữ Liệu Lịch Sử AI</td>
                <td>Sinh 4,320 bản ghi dữ liệu lịch sử chuẩn xác có quy luật giờ cao điểm, ngày thường, cuối tuần, ngày lễ và độ nhiễu.</td>
                <td><code>backend/app/ml_engine/data_generator.py</code></td>
            </tr>
            <tr>
                <td class="text-center">3.5</td>
                <td>Huấn Luyện Model Random Forest</td>
                <td>Huấn luyện mô hình hồi quy Random Forest Regressor với Scikit-learn, đạt sai số MAE rất thấp (&lt; 0.06 ~ 5.8%).</td>
                <td><code>backend/app/ml_engine/train.py</code>, <code>models/*.joblib</code></td>
            </tr>
            <tr>
                <td class="text-center">3.6</td>
                <td>API Dự Báo &amp; Unit Tests Tự Động</td>
                <td>Xây dựng API dự báo tỷ lệ lấp đầy theo giờ và toàn ngày 24h; viết trọn bộ 11 tests (6 A* + 5 ML) bằng Pytest.</td>
                <td><code>app/routers/predict.py</code>, <code>tests/test_*.py</code></td>
            </tr>
        </tbody>
    </table>

    <!-- MỤC 4: QUY TRÌNH PHỐI HỢP & MỐC BÀN GIAO -->
    <div class="section-title">4. Kế Hoạch Phối Hợp Kỹ Thuật Giữa 3 Thành Viên</div>
    <table>
        <thead>
            <tr>
                <th style="width: 15%;">Giai Đoạn</th>
                <th style="width: 28%;">Phạm Văn Đạt (Backend)</th>
                <th style="width: 28%;">Nguyễn Duy Bảo (Frontend)</th>
                <th style="width: 29%;">Trần Tuấn Anh (AI / A*)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>1. Chuẩn bị</strong></td>
                <td>Định nghĩa cấu trúc DB, Schemas Pydantic.</td>
                <td>Dựng wireframe giao diện, layout Cyberpunk.</td>
                <td>Xác lập quy cách ma trận lưới tọa độ 2D.</td>
            </tr>
            <tr>
                <td><strong>2. Phát triển lõi</strong></td>
                <td>Hoàn thiện API Auth, Booking, DB lock.</td>
                <td>Dựng Parking Grid 2D, tích hợp GSAP.</td>
                <td>Hoàn thành giải thuật A*, train model ML RF.</td>
            </tr>
            <tr>
                <td><strong>3. Tích hợp</strong></td>
                <td>Gắn router navigate, predict, WebSocket Server.</td>
                <td>Kết nối API Client, lắng nghe WebSocket.</td>
                <td>Verify độ chính xác API A* &lt; 5ms và API ML 24h.</td>
            </tr>
            <tr>
                <td><strong>4. Nghiệm thu</strong></td>
                <td>Đóng gói kịch bản chạy (<code>run.bat</code>, <code>run.ps1</code>).</td>
                <td>Kiểm thử giao diện E2E, ghi hình demo.</td>
                <td>Chạy bộ 11 automated unit tests Pytest.</td>
            </tr>
        </tbody>
    </table>

    <!-- MỤC 5: CAM KẾT & CHỮ KÝ XÁC NHẬN -->
    <div class="section-title">5. Cam Kết Tiến Độ &amp; Chữ Ký Xác Nhận Của Các Thành Viên</div>
    <table class="sign-table">
        <tr>
            <td>
                <div class="sign-box">
                    <div class="sign-role">Trưởng Nhóm / Backend Core</div>
                    <div style="font-size: 8.5px; color: #64748b;">(Ký và ghi rõ họ tên)</div>
                    <div class="sign-space"></div>
                    <div class="sign-name">Phạm Văn Đạt</div>
                </div>
            </td>
            <td>
                <div class="sign-box">
                    <div class="sign-role">Kỹ Sư Giao Diện (Frontend)</div>
                    <div style="font-size: 8.5px; color: #64748b;">(Ký và ghi rõ họ tên)</div>
                    <div class="sign-space"></div>
                    <div class="sign-name">Nguyễn Duy Bảo</div>
                </div>
            </td>
            <td>
                <div class="sign-box">
                    <div class="sign-role">Kỹ Sư Thuật Toán &amp; AI (AI/ML)</div>
                    <div style="font-size: 8.5px; color: #64748b;">(Ký và ghi rõ họ tên)</div>
                    <div class="sign-space"></div>
                    <div class="sign-name">Trần Tuấn Anh</div>
                </div>
            </td>
        </tr>
    </table>

    <div class="footer-note">
        <div>Hệ Thống Bãi Đỗ Xe Thông Minh (Smart Parking System) — Phân Công Nhiệm Vụ</div>
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

if os.path.exists(PDF_FILE):
    import shutil
    try:
        shutil.copy2(PDF_FILE, DOWNLOAD_PDF)
        print(f"SUCCESS! Created PDF: {PDF_FILE} and copied to Downloads: {DOWNLOAD_PDF}")
    except PermissionError:
        alt_download = os.path.abspath(r"C:\Users\LENOVO\Downloads\phan_cong_nhiem_vu_nhom_v2.pdf")
        shutil.copy2(PDF_FILE, alt_download)
        print(f"SUCCESS! Created PDF: {PDF_FILE} and copied to alternative: {alt_download}")
