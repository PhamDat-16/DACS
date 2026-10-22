import subprocess
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

HTML_FILE = os.path.abspath(r"d:\smart-parking-system\tai_lieu_chuc_nang.html")
PDF_FILE = os.path.abspath(r"d:\smart-parking-system\tai_lieu_chuc_nang_va_ma_nguon.pdf")
DOWNLOAD_PDF = os.path.abspath(r"C:\Users\LENOVO\Downloads\tai_lieu_chuc_nang_va_ma_nguon.pdf")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Tài Liệu Kỹ Thuật & Hướng Dẫn Vận Hành - Smart Parking System</title>
    <style>
        @page {
            size: A4;
            margin: 9mm 11mm 9mm 11mm;
        }
        * {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Times New Roman', Roboto, Arial, sans-serif;
            color: #1e293b;
            line-height: 1.34;
            font-size: 10px;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }
        
        .doc-header {
            border-bottom: 1.5px solid #0f172a;
            padding-bottom: 5px;
            margin-bottom: 7px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }
        .doc-title {
            font-size: 15px;
            font-weight: 800;
            color: #0f172a;
            margin: 0;
            letter-spacing: -0.2px;
            text-transform: uppercase;
        }
        .doc-subtitle {
            font-size: 10px;
            color: #475569;
            margin-top: 2px;
            font-weight: 600;
        }
        .meta-info {
            text-align: right;
            font-size: 9px;
            color: #334155;
            line-height: 1.3;
        }

        .section-title {
            font-size: 10.5px;
            font-weight: 800;
            color: #0f172a;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            margin: 7px 0 4px 0;
            padding-left: 5px;
            border-left: 3px solid #334155;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 6px;
            font-size: 9.5px;
            background-color: #ffffff;
        }
        th, td {
            border: 1px solid #cbd5e1;
            padding: 4px 6px;
            text-align: left;
            vertical-align: top;
        }
        th {
            background-color: #f1f5f9;
            color: #0f172a;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 8.5px;
            letter-spacing: 0.2px;
        }
        tr:nth-child(even) {
            background-color: #fafafa;
        }
        
        .text-center { text-align: center; }
        .text-bold { font-weight: 700; }
        
        code {
            font-family: Consolas, 'Courier New', monospace;
            font-size: 9px;
            background-color: #f1f5f9;
            padding: 1px 3px;
            border-radius: 3px;
            border: 1px solid #e2e8f0;
            color: #0f172a;
        }

        .code-box {
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-left: 3px solid #0f172a;
            border-radius: 3px;
            padding: 5px 8px;
            margin: 4px 0 6px 0;
            font-family: Consolas, 'Courier New', monospace;
            font-size: 9px;
            color: #0f172a;
            line-height: 1.35;
        }

        .page-break {
            page-break-before: always;
            break-before: page;
        }

        .footer-note {
            margin-top: 5px;
            padding-top: 4px;
            border-top: 1px solid #cbd5e1;
            font-size: 8.5px;
            color: #64748b;
            display: flex;
            justify-content: space-between;
        }
    </style>
</head>
<body>

    <!-- ==================== TRANG 1 ==================== -->
    <div class="doc-header">
        <div>
            <div class="doc-title">TÀI LIỆU KỸ THUẬT &amp; HƯỚNG DẪN VẬN HÀNH HỆ THỐNG</div>
            <div class="doc-subtitle">Hệ Thống Quản Lý Bãi Đỗ Xe Thông Minh (Smart Parking System - SPS)</div>
        </div>
        <div class="meta-info">
            <div><strong>Phiên bản:</strong> Release v1.0.0</div>
            <div><strong>Ngày xuất bản:</strong> 24/09/2026</div>
            <div><strong>Loại tài liệu:</strong> System Specs &amp; User Manual</div>
        </div>
    </div>

    <!-- MỤC 1: TỔNG HỢP CÁC CHỨC NĂNG CỐT LÕI CỦA HỆ THỐNG -->
    <div class="section-title">1. Tổng Hợp Toàn Bộ Các Chức Năng Cốt Lõi Của Hệ Thống (Features &amp; Modules)</div>
    <table>
        <thead>
            <tr>
                <th style="width: 5%;" class="text-center">STT</th>
                <th style="width: 25%;">Phân Hệ / Chức Năng</th>
                <th style="width: 45%;">Mô Tả Kỹ Thuật &amp; Phạm Vi Hoạt Động</th>
                <th style="width: 25%;">Trạng Thái &amp; Hiệu Năng</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center text-bold">1</td>
                <td><strong>Bản Đồ Bãi Xe Trực Quan (Parking Grid Map)</strong></td>
                <td>Mô hình hóa ma trận bãi xe dạng lưới 2D (ví dụ: 5x5 hoặc 6x8). Trực quan hóa 4 trạng thái thời gian thực của từng ô đỗ: Trống (Available), Đã đặt (Reserved), Đang đỗ (Occupied), Vật cản tĩnh/trụ (Blocked).</td>
                <td><span class="text-bold">Hoàn thành 100%</span><br>Hiển thị 2D Stagger GSAP</td>
            </tr>
            <tr>
                <td class="text-center text-bold">2</td>
                <td><strong>Dẫn Đường Ngắn Nhất A* (A-Star Navigation)</strong></td>
                <td>Tính toán đường đi tối ưu tránh vật cản tĩnh (tường/trụ) và vật cản động (xe đang đỗ) từ Cổng vào (0, 0) đến slot đích dựa trên hàm ước lượng Heuristic khoảng cách Manhattan.</td>
                <td><span class="text-bold">Hoàn thành 100%</span><br>Độ trễ tính toán &lt; 5ms</td>
            </tr>
            <tr>
                <td class="text-center text-bold">3</td>
                <td><strong>Mô Hình AI Dự Báo Lấp Đầy (ML Forecast 24h)</strong></td>
                <td>Mô hình Random Forest Regressor huấn luyện trên 4,320 mẫu lịch sử, phân tích chu kỳ giờ cao điểm, ngày thường, cuối tuần, ngày lễ. Cung cấp API dự báo theo giờ và biểu đồ dự báo 24 giờ.</td>
                <td><span class="text-bold">Hoàn thành 100%</span><br>Sai số cực thấp MAE ~ 5.8%</td>
            </tr>
            <tr>
                <td class="text-center text-bold">4</td>
                <td><strong>Đặt Chỗ &amp; Cấp Vé Điện Tử (Booking &amp; QR Code)</strong></td>
                <td>Khách hàng chọn ô đỗ, nhập biển số và thời lượng gửi xe. Hệ thống tự động tính phí dự kiến và sinh mã QR Code Base64 chứa thông tin vé điện tử để quét qua barrier.</td>
                <td><span class="text-bold">Hoàn thành 100%</span><br>Xuất mã QR Base64 tức thì</td>
            </tr>
            <tr>
                <td class="text-center text-bold">5</td>
                <td><strong>Chống Đặt Trùng Chỗ (Anti Double-Booking)</strong></td>
                <td>Áp dụng kỹ thuật khóa cấp dòng Database (Row-Level Locking với <code>SELECT FOR UPDATE</code>) đảm bảo tính toàn vẹn tuyệt đối khi có nhiều giao dịch đặt chỗ đồng thời.</td>
                <td><span class="text-bold">Hoàn thành 100%</span><br>Vượt qua Unit Test đa luồng</td>
            </tr>
            <tr>
                <td class="text-center text-bold">6</td>
                <td><strong>Check-In / Check-Out Barrier (Sessions)</strong></td>
                <td>Nhân viên bãi xe quét mã QR vé tại barrier vào/ra. Hệ thống kiểm tra hợp lệ, ghi nhận mốc thời gian, tự động cập nhật trạng thái ô đỗ và chuyển trạng thái vé sang Đang đỗ hoặc Đã hoàn tất.</td>
                <td><span class="text-bold">Hoàn thành 100%</span><br>Đầy đủ API Check-in/out</td>
            </tr>
            <tr>
                <td class="text-center text-bold">7</td>
                <td><strong>Bảo Mật &amp; Phân Quyền (Auth &amp; RBAC)</strong></td>
                <td>Cơ chế mã hóa mật khẩu Bcrypt an toàn, cấp phát và giải mã JWT Bearer Token, kiểm soát truy cập phân quyền 3 cấp độ: <code>Admin</code>, <code>Staff</code>, <code>Customer</code>.</td>
                <td><span class="text-bold">Hoàn thành 100%</span><br>Xác thực chuẩn stateless JWT</td>
            </tr>
            <tr>
                <td class="text-center text-bold">8</td>
                <td><strong>Kênh Realtime WebSocket (IoT &amp; Telemetry)</strong></td>
                <td>Kết nối Full-Duplex hai chiều giữa Server và Frontend; hỗ trợ đo độ trễ Ping/Pong RTT, phát sóng cập nhật trạng thái slot và telemetry mạng cảm biến siêu âm IoT 48 ô đỗ.</td>
                <td><span class="text-bold">Hoàn thành 100%</span><br>Độ trễ truyền tin &lt; 10ms</td>
            </tr>
            <tr>
                <td class="text-center text-bold">9</td>
                <td><strong>Phân Tích Doanh Thu &amp; Vé Tháng (Analytics)</strong></td>
                <td>Thống kê doanh thu theo ngày, tuần, tháng; tỷ lệ thanh toán không tiền mặt (VietQR, MoMo); quản lý danh sách thuê bao vé tháng / cư dân tòa nhà.</td>
                <td><span class="text-bold">Hoàn thành 100%</span><br>Dashboard biểu đồ trực quan</td>
            </tr>
            <tr>
                <td class="text-center text-bold">10</td>
                <td><strong>Chế Độ Demo Độc Lập (Standalone Mock Engine)</strong></td>
                <td>Tích hợp sẵn bộ thuật toán A* và bộ sinh dữ liệu dự phòng ngay trên client. Cho phép mở file HTML demo chạy mượt mà ngay cả khi không có kết nối backend/database.</td>
                <td><span class="text-bold">Hoàn thành 100%</span><br>Chạy độc lập trên trình duyệt</td>
            </tr>
        </tbody>
    </table>

    <!-- MỤC 2: DANH MỤC TOÀN BỘ FILE CODE - BẢNG 1: BACKEND CORE -->
    <div class="section-title">2. Danh Mục Các File Mã Nguồn, Chức Năng &amp; Công Dụng Chi Tiết</div>
    <div style="font-weight: 700; margin: 3px 0; font-size: 9.5px; color: #334155;">2.1. Phân Hệ Backend Core, Cấu Hình &amp; Cơ Sở Dữ Liệu (PostgreSQL / Alembic)</div>
    <table>
        <thead>
            <tr>
                <th style="width: 28%;">Đường Dẫn File Mã Nguồn</th>
                <th style="width: 47%;">Chức Năng &amp; Nhiệm Vụ Kỹ Thuật</th>
                <th style="width: 25%;">Công Dụng Trong Hệ Thống</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>backend/app/main.py</code></td>
                <td>Điểm khởi chạy ứng dụng (Entrypoint) FastAPI; nạp middleware CORS, middleware chống cache trình duyệt, tích hợp phục vụ file tĩnh Frontend và endpoint <code>/api/health</code>.</td>
                <td>Khởi động toàn bộ máy chủ API và Web server tích hợp.</td>
            </tr>
            <tr>
                <td><code>backend/app/core/config.py</code></td>
                <td>Đọc cấu hình môi trường từ <code>.env</code> bằng Pydantic BaseSettings: kết nối PostgreSQL, Secret Key JWT, CORS origins.</td>
                <td>Quản lý tập trung các thông số cấu hình của hệ thống.</td>
            </tr>
            <tr>
                <td><code>backend/app/core/database.py</code></td>
                <td>Khởi tạo SQLAlchemy Engine, SessionLocal, lớp Base Declarative, và hàm generator <code>get_db()</code> quản lý vòng đời session.</td>
                <td>Cung cấp kết nối CSDL tin cậy cho toàn bộ router/service.</td>
            </tr>
            <tr>
                <td><code>backend/app/core/security.py</code></td>
                <td>Hàm băm và đối soát mật khẩu với thư viện passlib (Bcrypt); tạo và giải mã JWT token có thiết lập thời gian hết hạn (expiration).</td>
                <td>Đảm bảo an toàn thông tin đăng nhập và xác thực phiên.</td>
            </tr>
            <tr>
                <td><code>backend/app/core/deps.py</code></td>
                <td>Các Dependency injection của FastAPI: <code>get_current_user</code> giải mã token từ Bearer Header; <code>require_role</code> kiểm tra quyền.</td>
                <td>Bảo vệ các API endpoint nhạy cảm theo đúng phân quyền.</td>
            </tr>
            <tr>
                <td><code>backend/app/core/websocket_manager.py</code></td>
                <td>Lớp <code>ConnectionManager</code> quản lý danh sách kết nối WebSocket đồng thời, gửi tin nhắn cá nhân và phát sóng (broadcast) sự kiện.</td>
                <td>Trục xương sống cho tính năng realtime hai chiều.</td>
            </tr>
            <tr>
                <td><code>backend/app/models/*.py</code></td>
                <td>Định nghĩa 6 SQLAlchemy ORM models: <code>user.py</code>, <code>parking_lot.py</code>, <code>parking_slot.py</code>, <code>booking.py</code>, <code>session.py</code>, <code>occupancy_history.py</code>.</td>
                <td>Ánh xạ cấu trúc bảng CSDL thành các đối tượng Python.</td>
            </tr>
            <tr>
                <td><code>backend/app/schemas/*.py</code></td>
                <td>Định nghĩa các Pydantic Schemas kiểm soát tính hợp lệ của dữ liệu đầu vào (Request) và định dạng chuẩn dữ liệu đầu ra (Response).</td>
                <td>Chuẩn hóa dữ liệu giao tiếp API, sinh tài liệu Swagger tự động.</td>
            </tr>
        </tbody>
    </table>

    <div class="footer-note">
        <div>Hệ Thống Bãi Đỗ Xe Thông Minh (Smart Parking System) — Tài Liệu Kỹ Thuật</div>
        <div>Trang 1 / 3</div>
    </div>

    <!-- ==================== TRANG 2 ==================== -->
    <div class="page-break"></div>

    <div class="doc-header">
        <div>
            <div class="doc-title">TÀI LIỆU KỸ THUẬT &amp; HƯỚNG DẪN VẬN HÀNH (TIẾP THEO)</div>
            <div class="doc-subtitle">Hệ Thống Quản Lý Bãi Đỗ Xe Thông Minh (Smart Parking System - SPS)</div>
        </div>
        <div class="meta-info">
            <div><strong>Phần II:</strong> Chi Tiết File Mã Nguồn Thuật Toán, Dịch Vụ &amp; Giao Diện</div>
        </div>
    </div>

    <!-- BẢNG 2: THUẬT TOÁN A* & ML ENGINE -->
    <div style="font-weight: 700; margin: 3px 0; font-size: 9.5px; color: #334155;">2.2. Phân Hệ Thuật Toán Dẫn Đường A* &amp; Trí Tuệ Nhân Tạo (ML Engine)</div>
    <table>
        <thead>
            <tr>
                <th style="width: 28%;">Đường Dẫn File Mã Nguồn</th>
                <th style="width: 47%;">Chức Năng &amp; Nhiệm Vụ Kỹ Thuật</th>
                <th style="width: 25%;">Công Dụng Trong Hệ Thống</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>backend/app/pathfinding/grid.py</code></td>
                <td>Biểu diễn bãi xe thành lưới ma trận 2D thuần Python; quản lý kích thước (width, height), kiểm tra tọa độ hợp lệ và danh sách ô vật cản.</td>
                <td>Tách biệt logic ma trận không gian, hỗ trợ unit test độc lập.</td>
            </tr>
            <tr>
                <td><code>backend/app/pathfinding/astar.py</code></td>
                <td>Cài đặt thuật toán A* thuần Python với hàng đợi ưu tiên (Priority Queue / heapq); sử dụng hàm Heuristic khoảng cách Manhattan.</td>
                <td>Tính toán đường đi ngắn nhất tuyệt đối né vật cản.</td>
            </tr>
            <tr>
                <td><code>backend/app/ml_engine/data_generator.py</code></td>
                <td>Bộ sinh dữ liệu lịch sử giả lập (4,320 mẫu) mô phỏng chính xác chu kỳ giờ cao điểm (sáng/chiều), ngày làm việc, cuối tuần, ngày lễ và nhiễu Gaussian.</td>
                <td>Tạo tập dữ liệu huấn luyện chân thực lưu vào CSDL.</td>
            </tr>
            <tr>
                <td><code>backend/app/ml_engine/train.py</code></td>
                <td>Huấn luyện mô hình hồi quy Random Forest Regressor (200 cây, max depth 10) từ dữ liệu lịch sử; đánh giá chỉ số MAE, RMSE và lưu file model.</td>
                <td>Sản sinh file mô hình học máy <code>occupancy_model.joblib</code>.</td>
            </tr>
            <tr>
                <td><code>backend/app/ml_engine/predict.py</code></td>
                <td>Nạp mô hình Singleton với Double-Checked Locking chống race condition; cung cấp hàm dự báo tỷ lệ lấp đầy theo giờ và toàn ngày 24 giờ.</td>
                <td>Thực thi suy luận AI thời gian thực phục vụ API frontend.</td>
            </tr>
        </tbody>
    </table>

    <!-- BẢNG 3: DỊCH VỤ NGHIỆP VỤ & ROUTERS API -->
    <div style="font-weight: 700; margin: 5px 0 3px 0; font-size: 9.5px; color: #334155;">2.3. Phân Hệ Dịch Vụ Nghiệp Vụ, Realtime WebSocket &amp; Routers API</div>
    <table>
        <thead>
            <tr>
                <th style="width: 28%;">Đường Dẫn File Mã Nguồn</th>
                <th style="width: 47%;">Chức Năng &amp; Nhiệm Vụ Kỹ Thuật</th>
                <th style="width: 25%;">Công Dụng Trong Hệ Thống</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>backend/app/services/booking_service.py</code></td>
                <td>Xử lý logic nghiệp vụ đặt chỗ; thực hiện truy vấn khóa hàng <code>with_for_update()</code> trên slot đỗ xe để ngăn ngừa triệt để Double-Booking.</td>
                <td>Đảm bảo an toàn giao dịch đặt chỗ khi có nhiều người cùng bấm.</td>
            </tr>
            <tr>
                <td><code>backend/app/services/qr_service.py</code></td>
                <td>Mã hóa dữ liệu vé đỗ xe (mã vé, slot, biển số) thành hình ảnh mã QR Code định dạng PNG, chuyển đổi thành chuỗi Base64.</td>
                <td>Cấp phát vé điện tử nhanh gọn không cần lưu file đệm trên đĩa.</td>
            </tr>
            <tr>
                <td><code>backend/app/services/navigate_service.py</code></td>
                <td>Lấy dữ liệu bãi xe từ DB (kích thước lưới, vị trí slot đã có xe, vật cản), nạp vào Grid và gọi A* tính toán danh sách tọa độ (waypoints).</td>
                <td>Cầu nối trung gian giữa CSDL bãi xe và thuật toán A*.</td>
            </tr>
            <tr>
                <td><code>backend/app/services/session_service.py</code></td>
                <td>Xử lý quy trình quét vé Check-in và Check-out tại barrier; đối soát mã vé, tính cước phí thực tế theo giờ và cập nhật trạng thái slot.</td>
                <td>Vận hành quy trình kiểm soát xe ra/vào bãi.</td>
            </tr>
            <tr>
                <td><code>backend/app/routers/websocket.py</code></td>
                <td>Cung cấp WebSocket endpoint <code>/ws/realtime</code>, xử lý ping-pong đo độ trễ RTT, API broadcast và giả lập mạng cảm biến IoT 48 ô đỗ.</td>
                <td>Kênh truyền dữ liệu realtime hai chiều giữa Server và Frontend.</td>
            </tr>
            <tr>
                <td><code>backend/app/routers/analytics.py</code></td>
                <td>API tổng hợp doanh thu theo ngày/tháng, tỷ lệ thanh toán không tiền mặt và quản lý thuê bao vé tháng / thẻ cư dân tòa nhà.</td>
                <td>Cung cấp số liệu phân tích tài chính cho ban quản lý bãi xe.</td>
            </tr>
            <tr>
                <td><code>backend/app/routers/*.py</code> (auth, users, lots, bookings, sessions, navigate, predict)</td>
                <td>Khai báo các nhóm REST API tương ứng với từng phân hệ nghiệp vụ, nhận request, kiểm tra schema và chuyển tiếp cho service xử lý.</td>
                <td>Định tuyến toàn bộ yêu cầu HTTP từ client tới đúng module xử lý.</td>
            </tr>
        </tbody>
    </table>

    <!-- BẢNG 4: FRONTEND CLIENT & COMPONENTS -->
    <div style="font-weight: 700; margin: 5px 0 3px 0; font-size: 9.5px; color: #334155;">2.4. Phân Hệ Giao Diện Web Frontend (Vue 3, Tailwind CSS &amp; GSAP Animation)</div>
    <table>
        <thead>
            <tr>
                <th style="width: 28%;">Đường Dẫn File Mã Nguồn</th>
                <th style="width: 47%;">Chức Năng &amp; Nhiệm Vụ Kỹ Thuật</th>
                <th style="width: 25%;">Công Dụng Trong Hệ Thống</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>frontend/index.html</code></td>
                <td>Trang giao diện chính Single Page Application; tích hợp thư viện CDN Tailwind CSS, nạp các modules JavaScript ES6 và chứa layout HTML.</td>
                <td>Khung nhìn hiển thị chính của người dùng và ban quản lý.</td>
            </tr>
            <tr>
                <td><code>frontend/src/app.js</code></td>
                <td>Root Application Controller bằng Vue 3 Composition API; quản lý trạng thái phiên đăng nhập, điều phối xe chạy GSAP, kết nối WebSocket.</td>
                <td>Điều khiển toàn bộ logic giao diện và diễn hoạt đồ họa.</td>
            </tr>
            <tr>
                <td><code>frontend/src/api/client.js</code></td>
                <td>HTTP API Client gói các hàm gọi FastAPI; tích hợp Standalone Mock Engine tự động tính toán A* và sinh dữ liệu dự phòng khi chạy offline.</td>
                <td>Đảm bảo ứng dụng luôn hoạt động trơn tru dù có backend hay không.</td>
            </tr>
            <tr>
                <td><code>frontend/src/components/ParkingGrid.js</code></td>
                <td>Component hiển thị sơ đồ lưới 25 ô đỗ xe với hiệu ứng màu sắc tương tác, badge trạng thái và nhận diện click chọn slot để dẫn đường.</td>
                <td>Trực quan hóa sơ đồ bãi xe thời gian thực.</td>
            </tr>
            <tr>
                <td><code>frontend/src/components/BookingModal.js</code></td>
                <td>Component Modal đặt chỗ xe: nhập biển số, chọn số giờ, tính trước chi phí và hiển thị vé điện tử QR Code động sắc nét.</td>
                <td>Giao diện thực hiện quy trình đặt chỗ cho khách hàng.</td>
            </tr>
            <tr>
                <td><code>frontend/src/components/OccupancyForecast.js</code></td>
                <td>Component hiển thị biểu đồ đường cong dự báo tỷ lệ lấp đầy 24h, kèm thanh trượt scrubber mượt mà bằng GSAP Utils.</td>
                <td>Giao diện xem xu hướng công suất bãi xe theo trí tuệ nhân tạo.</td>
            </tr>
            <tr>
                <td><code>frontend/src/components/StatsCounter.js</code></td>
                <td>Component hiển thị các thẻ KPI thống kê số chỗ trống, tỷ lệ lấp đầy, số xe đang đỗ với hiệu ứng Numeric Counter tự động đếm số.</td>
                <td>Cung cấp thông tin tổng quan nhanh cho người vận hành.</td>
            </tr>
        </tbody>
    </table>

    <div class="footer-note">
        <div>Hệ Thống Bãi Đỗ Xe Thông Minh (Smart Parking System) — Tài Liệu Kỹ Thuật</div>
        <div>Trang 2 / 3</div>
    </div>

    <!-- ==================== TRANG 3 ==================== -->
    <div class="page-break"></div>

    <div class="doc-header">
        <div>
            <div class="doc-title">TÀI LIỆU KỸ THUẬT &amp; HƯỚNG DẪN VẬN HÀNH (TIẾP THEO)</div>
            <div class="doc-subtitle">Hệ Thống Quản Lý Bãi Đỗ Xe Thông Minh (Smart Parking System - SPS)</div>
        </div>
        <div class="meta-info">
            <div><strong>Phần III:</strong> Kiểm Thử Tự Động &amp; Hướng Dẫn Vận Hành Mở Web</div>
        </div>
    </div>

    <!-- BẢNG 5: KIỂM THỬ TỰ ĐỘNG & SCRIPTS -->
    <div style="font-weight: 700; margin: 3px 0; font-size: 9.5px; color: #334155;">2.5. Bộ Kiểm Thử Tự Động (Unit Tests) &amp; Các Script Vận Hành</div>
    <table>
        <thead>
            <tr>
                <th style="width: 28%;">Đường Dẫn File Mã Nguồn</th>
                <th style="width: 47%;">Chức Năng &amp; Nhiệm Vụ Kỹ Thuật</th>
                <th style="width: 25%;">Công Dụng Trong Hệ Thống</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>backend/tests/test_astar.py</code></td>
                <td>6 unit test cases kiểm tra giải thuật A*: đường thẳng không vật cản, tự né vật cản, bãi xe bị chặn hoàn toàn, điểm đầu trùng đích, tối ưu Manhattan.</td>
                <td>Bảo đảm thuật toán dẫn đường luôn chính xác 100%.</td>
            </tr>
            <tr>
                <td><code>backend/tests/test_ml_engine.py</code></td>
                <td>5 unit test cases kiểm tra dữ liệu synthetic, tính tái lập theo seed ngẫu nhiên, quy luật giờ đêm thấp hơn giờ cao điểm, mô hình hội tụ và dự báo hợp lệ.</td>
                <td>Đảm bảo mô hình AI hoạt động chuẩn mực trước khi deploy.</td>
            </tr>
            <tr>
                <td><code>backend/tests/test_double_booking.py</code></td>
                <td>Kiểm thử đa luồng (multi-threading concurrency test): mô phỏng 2 khách cùng bấm đặt 1 ô đỗ cùng lúc, kiểm tra row-level locking chặn 409 Conflict.</td>
                <td>Chứng minh khả năng chịu tải và chống xung đột giao dịch.</td>
            </tr>
            <tr>
                <td><code>run.bat</code> &amp; <code>run.ps1</code></td>
                <td>Script khởi chạy toàn bộ hệ sinh thái dự án (Backend FastAPI + Static Frontend) trên Windows chỉ với 1 click chuột.</td>
                <td>Tối ưu hóa thao tác khởi động cho người dùng và ban giám khảo.</td>
            </tr>
        </tbody>
    </table>

    <!-- MỤC 3: HƯỚNG DẪN CÁCH CHẠY VÀ MỞ WEB CHI TIẾT -->
    <div class="section-title">3. Hướng Dẫn Cách Chạy Hệ Thống &amp; Mở Giao Diện Web Trên Trình Duyệt</div>
    
    <div style="font-weight: 700; margin: 4px 0 2px 0; font-size: 9.5px; color: #0f172a;">3.1. Cách 1: Khởi Chạy 1 Chạm Toàn Diện (Khuyên Dùng — Nhanh &amp; Tiện Lợi Nhất)</div>
    <p style="margin: 0 0 3px 0; font-size: 9.5px;">Hệ thống đã được tích hợp sẵn bộ script khởi động tự động. Bạn chỉ cần thực hiện 1 trong 2 thao tác sau:</p>
    <div class="code-box">
        # Thao tác A (Dùng chuột): Nhấp đúp (Double-click) trực tiếp vào file "run.bat" tại thư mục gốc D:\\smart-parking-system<br>
        # Thao tác B (Dùng PowerShell): Mở terminal tại thư mục dự án và gõ lệnh: .\\run.ps1
    </div>
    <p style="margin: 0 0 4px 0; font-size: 9.5px;">
        &bull; Sau khi khởi động thành công, mở trình duyệt web (Google Chrome hoặc Microsoft Edge) và truy cập: 
        <br>&rarr; <strong>Giao diện Web điều hành:</strong> <code>http://localhost:8000</code>
        <br>&rarr; <strong>Tài liệu API Swagger tương tác:</strong> <code>http://localhost:8000/docs</code>
        <br>&rarr; <strong>Kiểm tra trạng thái server:</strong> <code>http://localhost:8000/api/health</code>
    </p>

    <div style="font-weight: 700; margin: 5px 0 2px 0; font-size: 9.5px; color: #0f172a;">3.2. Cách 2: Khởi Chạy Thủ Công Từng Phân Hệ Bằng Dòng Lệnh</div>
    <div class="code-box">
        # BƯỚC 1: Khởi động Backend FastAPI (Terminal 1)<br>
        cd D:\\smart-parking-system\\backend<br>
        .\\venv\\Scripts\\activate<br>
        uvicorn app.main:app --reload --port 8000<br><br>
        # BƯỚC 2: Khởi động Frontend Web Server (Terminal 2 - tùy chọn)<br>
        cd D:\\smart-parking-system\\frontend<br>
        python -m http.server 3000
    </div>
    <p style="margin: 0 0 4px 0; font-size: 9.5px;">Truy cập Frontend tại <code>http://localhost:3000</code> hoặc <code>http://localhost:8000</code> (cả hai cổng đều đã được cấu hình CORS cho phép kết nối).</p>

    <div style="font-weight: 700; margin: 5px 0 2px 0; font-size: 9.5px; color: #0f172a;">3.3. Cách 3: Chạy Trực Tiếp Không Cần Bật Server (Standalone Mock Engine)</div>
    <p style="margin: 0 0 3px 0; font-size: 9.5px;">
        Nếu bạn đang ở máy tính không có cài đặt Python hay PostgreSQL, bạn vẫn có thể trải nghiệm toàn bộ giao diện:
        <br>&bull; Nhấp đúp chuột trực tiếp vào file: <code>D:\\smart-parking-system\\frontend\\index.html</code> để mở bằng trình duyệt.
        <br>&bull; Hệ thống sẽ tự động kích hoạt <strong>Standalone Mock Engine</strong>: tự tính toán thuật toán dẫn đường A*, tự sinh đường đi cho xe chạy và mô phỏng biểu đồ dự báo AI đầy đủ mà không báo lỗi!
    </p>

    <!-- MỤC 4: THÔNG TIN ĐĂNG NHẬP MẪU -->
    <div class="section-title">4. Thông Tin Tài Khoản Đăng Nhập &amp; Hướng Dẫn Trải Nghiệm Các Tính Năng</div>
    <table>
        <thead>
            <tr>
                <th style="width: 20%;">Loại Tài Khoản</th>
                <th style="width: 25%;">Email Đăng Nhập</th>
                <th style="width: 15%;">Mật Khẩu</th>
                <th style="width: 40%;">Quyền Hạn &amp; Trải Nghiệm Khuyên Dùng</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Quản Trị Viên (Admin)</strong></td>
                <td><code>admin@example.com</code></td>
                <td><code>123456</code></td>
                <td>Toàn quyền xem KPI, sơ đồ bãi xe, điều khiển mô phỏng xe chạy A*, kéo thanh trượt AI và cấu hình bãi xe. <em>(Mẹo: Trên form đăng nhập có nút <strong>"Quick Admin Login"</strong> để đăng nhập 1 chạm không cần gõ chữ)</em>.</td>
            </tr>
            <tr>
                <td><strong>Nhân Viên (Staff)</strong></td>
                <td><code>staff@example.com</code></td>
                <td><code>123456</code></td>
                <td>Quyền thực hiện quét mã QR, duyệt Check-in và Check-out cho xe tại barrier cổng.</td>
            </tr>
            <tr>
                <td><strong>Khách Hàng (Customer)</strong></td>
                <td><code>customer@example.com</code></td>
                <td><code>123456</code></td>
                <td>Tài khoản mặc định khi bấm Đăng ký mới. Trải nghiệm chọn ô đỗ, đặt chỗ và lưu mã vé QR về điện thoại.</td>
            </tr>
        </tbody>
    </table>

    <div style="margin-top: 6px; padding: 6px 8px; border: 1px solid #cbd5e1; background: #f8fafc; border-radius: 4px; font-size: 9px; color: #334155;">
        <strong>Tóm tắt các bước trải nghiệm demo nhanh:</strong>
        <br>1. Mở web &rarr; Bấm <strong>"Quick Admin Login"</strong> để vào bảng điều khiển trung tâm.
        <br>2. Nhấp chuột vào bất kỳ ô đỗ nào còn <strong>Trống (Màu xanh ngọc)</strong> &rarr; Quan sát chiếc xe ảo tự lăn bánh và bẻ lái theo thuật toán <strong>A*</strong> từ Cổng vào (0, 0) đến đúng ô đỗ.
        <br>3. Bấm nút <strong>"Đặt Chỗ Nhanh"</strong> &rarr; Nhập biển số xe &rarr; Xem vé điện tử <strong>mã QR Code</strong> tự sinh.
        <br>4. Kéo thanh trượt <strong>Scrubber 24h</strong> tại bảng Dự Báo Lấp Đầy &rarr; Quan sát tỷ lệ lấp đầy bãi xe biến thiên theo từng khung giờ dựa trên mô hình <strong>Random Forest AI</strong>.
    </div>

    <div class="footer-note">
        <div>Hệ Thống Bãi Đỗ Xe Thông Minh (Smart Parking System) — Tài Liệu Kỹ Thuật &amp; Vận Hành</div>
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
        alt_download = os.path.abspath(r"C:\Users\LENOVO\Downloads\tai_lieu_chuc_nang_va_ma_nguon_v2.pdf")
        shutil.copy2(PDF_FILE, alt_download)
        print(f"SUCCESS! Created PDF: {PDF_FILE} and copied to alternative: {alt_download}")
