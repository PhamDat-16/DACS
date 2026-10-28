import subprocess
import os
import sys
import base64
import shutil
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

HTML_FILE = os.path.abspath(r"D:\smart-parking-system\Bao_cao_tien_do_du_an_Smart_Parking_System.html")
PDF_FILE = os.path.abspath(r"D:\smart-parking-system\Bao_cao_tien_do_du_an_Smart_Parking_System.pdf")
DOWNLOAD_PDF = os.path.abspath(r"C:\Users\LENOVO\Downloads\Bao_cao_tien_do_du_an_Smart_Parking_System.pdf")
LEGACY_PDF = os.path.abspath(r"D:\smart-parking-system\bao_cao_tien_do_du_an.pdf")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
IMG_DIR = r"C:\Users\LENOVO\.gemini\antigravity\brain\34425343-ff1b-46ef-a476-294ad3a89c79"

def get_base64_img(filename):
    path = os.path.join(IMG_DIR, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{data}"
    return ""

img_staff_checkin = get_base64_img("staff_checkin_map_synced.png")
img_staff_checkout = get_base64_img("staff_checkout_selected_vehicle.png")
img_customer_dash = get_base64_img("customer_dashboard_active_session.png")
img_customer_receipt = get_base64_img("customer_history_receipt_modal.png")
img_admin_passes = get_base64_img("admin_monthly_passes_table.png")
img_dup_warning = get_base64_img("duplicate_checkin_warning.png")

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Báo Cáo Tiến Độ Dự Án - Smart Parking System</title>
    <style>
        @page {{
            size: A4;
            margin: 10mm 14mm 10mm 14mm;
        }}
        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Times New Roman', Roboto, Arial, sans-serif;
            color: #1e293b;
            line-height: 1.33;
            font-size: 9.2pt;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }}
        
        /* HEADER BÁO CÁO HỌC THUẬT CHUẨN MỰC */
        .academic-header {{
            border-bottom: 2px solid #1e3a8a;
            padding-bottom: 5px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        .univ-title {{
            font-size: 8.5pt;
            font-weight: 700;
            color: #475569;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            margin-bottom: 2px;
        }}
        .doc-title {{
            font-size: 15pt;
            font-weight: 900;
            color: #1e3a8a;
            margin: 0;
            letter-spacing: -0.2px;
            text-transform: uppercase;
        }}
        .doc-subtitle {{
            font-size: 9.8pt;
            color: #0f172a;
            margin-top: 2px;
            font-weight: 700;
        }}
        .meta-box {{
            text-align: right;
            font-size: 8.5pt;
            color: #334155;
            line-height: 1.35;
        }}
        
        .badge {{
            display: inline-block;
            padding: 2px 7px;
            border-radius: 9999px;
            font-size: 8pt;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}
        .badge-success {{
            background-color: #dcfce7;
            color: #15803d;
            border: 1px solid #86efac;
        }}

        /* KPI SUMMARY CARDS */
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 7px;
            margin-bottom: 8px;
        }}
        .kpi-box {{
            border: 1px solid #cbd5e1;
            border-top: 3px solid #1e3a8a;
            background: #f8fafc;
            border-radius: 5px;
            padding: 5px 4px;
            text-align: center;
        }}
        .kpi-box.green {{ border-top-color: #10b981; }}
        .kpi-box.purple {{ border-top-color: #8b5cf6; }}
        .kpi-box.amber {{ border-top-color: #f59e0b; }}
        .kpi-box.blue {{ border-top-color: #0284c7; }}

        .kpi-num {{
            font-size: 14pt;
            font-weight: 900;
            color: #0f172a;
            line-height: 1.1;
        }}
        .kpi-label {{
            font-size: 7pt;
            font-weight: 700;
            color: #64748b;
            text-transform: uppercase;
            margin-top: 2px;
        }}

        .section-title {{
            font-size: 10pt;
            font-weight: 800;
            color: #0f172a;
            text-transform: uppercase;
            letter-spacing: 0.2px;
            margin: 7px 0 5px 0;
            padding-left: 7px;
            border-left: 3px solid #1e3a8a;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .section-title span.tag {{
            font-size: 7.5pt;
            font-weight: 700;
            color: #15803d;
            background: #dcfce7;
            padding: 1px 5px;
            border-radius: 4px;
            border: 1px solid #bbf7d0;
            text-transform: none;
        }}

        /* BẢNG BIỂU CHUẨN FORMAL */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 7px;
            font-size: 8.5pt;
        }}
        th, td {{
            padding: 4px 6px;
            text-align: left;
            border: 1px solid #cbd5e1;
        }}
        th {{
            background-color: #f1f5f9;
            color: #1e293b;
            font-weight: 800;
            font-size: 8pt;
            text-transform: uppercase;
            letter-spacing: 0.2px;
        }}
        tr:nth-child(even) {{
            background-color: #f8fafc;
        }}

        .progress-bar-bg {{
            background-color: #e2e8f0;
            border-radius: 3px;
            height: 5px;
            width: 50px;
            overflow: hidden;
            display: inline-block;
            vertical-align: middle;
            margin-right: 3px;
        }}
        .progress-bar-fill {{
            background-color: #10b981;
            height: 100%;
            border-radius: 3px;
        }}

        .module-card {{
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 5px;
            padding: 5px 8px;
            margin-bottom: 5px;
        }}
        .module-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2px;
        }}
        .module-name {{
            font-weight: 800;
            font-size: 9pt;
            color: #1e3a8a;
        }}
        .module-desc {{
            color: #334155;
            font-size: 8.5pt;
            margin: 0;
            text-align: justify;
            line-height: 1.3;
        }}

        /* HÌNH ẢNH MINH CHỨNG THỰC NGHIỆM */
        .img-grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 7px;
            margin-bottom: 6px;
        }}
        .img-card {{
            border: 1px solid #cbd5e1;
            border-radius: 5px;
            overflow: hidden;
            background: #0f172a;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }}
        .img-card img {{
            width: 100%;
            height: 162px;
            object-fit: cover;
            display: block;
        }}
        .img-caption {{
            font-size: 7.8pt;
            color: #334155;
            padding: 3px 5px;
            background: #f8fafc;
            border-top: 1px solid #e2e8f0;
            text-align: center;
            font-weight: 600;
        }}

        .page-break {{
            page-break-before: always;
            break-before: page;
        }}

        .footer-sign {{
            margin-top: 25px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            text-align: center;
            font-size: 9.2pt;
        }}
        .sign-title {{
            font-weight: 800;
            margin-bottom: 45px;
        }}
        .sign-name {{
            font-weight: 800;
            color: #0f172a;
        }}
    </style>
</head>
<body>

    <!-- ==================== TRANG 1 ==================== -->
    <div class="academic-header">
        <div>
            <div class="univ-title">TRƯỜNG ĐẠI HỌC PHENIKAA – KHOA CÔNG NGHỆ THÔNG TIN</div>
            <div class="doc-title">BÁO CÁO TIẾN ĐỘ DỰ ÁN</div>
            <div class="doc-subtitle">HỆ THỐNG QUẢN LÝ VÀ DẪN ĐƯỜNG BÃI ĐỖ XE THÔNG MINH (SMART PARKING SYSTEM - SPS)</div>
        </div>
        <div class="meta-box">
            <div><strong>Học phần:</strong> CSE702131-1-1-26(N01)</div>
            <div><strong>Sinh viên:</strong> Phạm Văn Đạt (MSV: 23017150)</div>
            <div><strong>Thời điểm:</strong> 08/10/2026 (Tuần thứ 6)</div>
            <div><strong>Đánh giá:</strong> <span class="badge badge-success">ĐẠT 98% MỤC TIÊU</span></div>
        </div>
    </div>

    <!-- 5 KPI CARDS -->
    <div class="kpi-row">
        <div class="kpi-box green">
            <div class="kpi-num">98%</div>
            <div class="kpi-label">Tiến Độ Tổng Thể</div>
        </div>
        <div class="kpi-box blue">
            <div class="kpi-num">28 / 28</div>
            <div class="kpi-label">API Endpoints Chuẩn</div>
        </div>
        <div class="kpi-box purple">
            <div class="kpi-num">&lt; 5 ms</div>
            <div class="kpi-label">Độ Trễ Dẫn Đường A*</div>
        </div>
        <div class="kpi-box amber">
            <div class="kpi-num">5.8%</div>
            <div class="kpi-label">Sai Số AI (MAE &lt; 0.06)</div>
        </div>
        <div class="kpi-box green">
            <div class="kpi-num">100%</div>
            <div class="kpi-label">Unit & Concurrency Tests</div>
        </div>
    </div>

    <div class="section-title">
        <span>I. BẢNG TIẾN ĐỘ CHI TIẾT TỪNG PHÂN HỆ NGHIỆP VỤ (WBS)</span>
        <span class="tag">Cập nhật đến 08/10/2026</span>
    </div>

    <table>
        <thead>
            <tr>
                <th style="width: 27%;">Phân hệ chức năng</th>
                <th style="width: 45%;">Các hạng mục đã hiện thực &amp; tích hợp</th>
                <th style="width: 14%; text-align: center;">Trạng thái</th>
                <th style="width: 14%; text-align: center;">Tiến độ</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>1. Backend Core &amp; Database</strong></td>
                <td>6 bảng CSDL quan hệ chuẩn 3NF trên PostgreSQL, Alembic Migration, Bcrypt, JWT Bearer Token, WebSocket realtime, Row-level Lock (SELECT FOR UPDATE).</td>
                <td style="text-align: center;"><span class="badge badge-success">Hoàn thành</span></td>
                <td style="text-align: center;">
                    <span class="progress-bar-bg"><span class="progress-bar-fill" style="width: 100%;"></span></span> 100%
                </td>
            </tr>
            <tr>
                <td><strong>2. Thuật toán Dẫn đường A*</strong></td>
                <td>Ma trận lưới tọa độ 2D, hàm Heuristic Manhattan, Priority Queue né vật cản tĩnh/động, API GET /api/lots/{{id}}/navigate phản hồi &lt; 5ms.</td>
                <td style="text-align: center;"><span class="badge badge-success">Hoàn thành</span></td>
                <td style="text-align: center;">
                    <span class="progress-bar-bg"><span class="progress-bar-fill" style="width: 100%;"></span></span> 100%
                </td>
            </tr>
            <tr>
                <td><strong>3. AI Engine Dự báo lấp đầy</strong></td>
                <td>Sinh 4,320 mẫu lịch sử chuỗi thời gian, Random Forest Regressor (200 trees), MAE = 0.058, nạp Singleton model, API dự báo 24h kèm scrubber.</td>
                <td style="text-align: center;"><span class="badge badge-success">Hoàn thành</span></td>
                <td style="text-align: center;">
                    <span class="progress-bar-bg"><span class="progress-bar-fill" style="width: 100%;"></span></span> 100%
                </td>
            </tr>
            <tr>
                <td><strong>4. Cổng Khách hàng (Customer)</strong></td>
                <td>Tìm kiếm bãi đỗ thời gian thực, đặt chỗ linh hoạt (theo giờ hoặc checkout), sinh vé QR Base64, quản lý vé tháng cư dân, theo dõi phiên &amp; hóa đơn.</td>
                <td style="text-align: center;"><span class="badge badge-success">Hoàn thành</span></td>
                <td style="text-align: center;">
                    <span class="progress-bar-bg"><span class="progress-bar-fill" style="width: 100%;"></span></span> 100%
                </td>
            </tr>
            <tr>
                <td><strong>5. Cổng Nhân viên (Staff Portal)</strong></td>
                <td>Trực barrier theo cơ sở (assigned_lot), check-in quét QR &amp; vãng lai, cảnh báo check-in trùng lặp, check-out tính tiền theo giờ &amp; giải phóng slot tức thời.</td>
                <td style="text-align: center;"><span class="badge badge-success">Hoàn thành</span></td>
                <td style="text-align: center;">
                    <span class="progress-bar-bg"><span class="progress-bar-fill" style="width: 100%;"></span></span> 100%
                </td>
            </tr>
            <tr>
                <td><strong>6. Cổng Quản trị viên (Admin)</strong></td>
                <td>Sơ đồ slot đỗ Inspector (Bảo trì/Khả dụng), tạo tài khoản nhân viên phân theo bãi xe, duyệt vé tháng cư dân, báo cáo phân tích doanh thu &amp; ca trực.</td>
                <td style="text-align: center;"><span class="badge badge-success">Hoàn thành</span></td>
                <td style="text-align: center;">
                    <span class="progress-bar-bg"><span class="progress-bar-fill" style="width: 95%;"></span></span> 95%
                </td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">
        <span>II. CHI TIẾT CÁC ĐẶC TẢ KỸ THUẬT VỪA HOÀN THÀNH VÀ NÂNG CẤP</span>
    </div>

    <div class="module-card">
        <div class="module-header">
            <span class="module-name">1. Phân quyền nhân viên theo cơ sở công tác (Assigned Lot) &amp; Đăng nhập linh hoạt</span>
            <span class="badge badge-success">Đã hoàn thiện</span>
        </div>
        <p class="module-desc">
            Bổ sung trường dữ liệu <code>assigned_lot</code> trên CSDL và giao diện Admin, cho phép Quản trị viên tạo tài khoản nhân viên gắn liền với từng bãi xe cụ thể (Bãi Đỗ Xe KĐT Đô Nghĩa, Vincom Center, Aeon Mall...). Cải tiến cơ chế xác thực: hỗ trợ đăng nhập linh hoạt bằng cả <strong>Tên đăng nhập (Username: admin, staff_baove...) HOẶC Email</strong>, tự động chuẩn hóa chuỗi và nhận diện bí danh thông minh.
        </p>
    </div>

    <div class="module-card">
        <div class="module-header">
            <span class="module-name">2. Quy trình Check-in/Check-out toàn diện &amp; Chống trùng lặp (Anti Duplicate Check-in)</span>
            <span class="badge badge-success">Đã hoàn thiện</span>
        </div>
        <p class="module-desc">
            Hoàn thiện quy trình xuất nhập bến xe cho Nhân viên trực: Tự động phát hiện và cảnh báo chặn khi một xe cố tình check-in lần hai khi chưa xuất bến. Khi Check-out: hệ thống tự động tính cước gửi xe theo thời gian thực tế, chuyển trạng thái phiên thành <code>completed</code> và <strong>giải phóng slot đỗ xe từ Đang đỗ (Đỏ) về Trống (Xanh) tức thời</strong> trên cả CSDL và sơ đồ WebSocket.
        </p>
    </div>

    <div class="module-card">
        <div class="module-header">
            <span class="module-name">3. Quản lý Vé tháng cư dân (Monthly Passes) &amp; Hóa đơn điện tử</span>
            <span class="badge badge-success">Đã hoàn thiện</span>
        </div>
        <p class="module-desc">
            Tích hợp đầy đủ luồng vé tháng: Khách hàng đăng ký gói vé tháng theo biển số, Admin tiếp nhận và kích hoạt vé; khách hàng thanh toán trực tuyến và lưu trữ thẻ vé điện tử. Mỗi lượt gửi xe hoàn tất đều phát sinh hóa đơn chi tiết (Receipt Modal) hiển thị biển số, giờ vào, giờ ra, tổng tiền và mã giao dịch.
        </p>
    </div>

    <!-- ==================== TRANG 2 ==================== -->
    <div class="page-break"></div>

    <div class="academic-header">
        <div>
            <div class="univ-title">TRƯỜNG ĐẠI HỌC PHENIKAA – KHOA CÔNG NGHỆ THÔNG TIN</div>
            <div class="doc-title">HÌNH ẢNH MINH CHỨNG THỰC NGHIỆM TỪ HỆ THỐNG</div>
            <div class="doc-subtitle">DỰ ÁN SMART PARKING SYSTEM (SPS) – THỜI ĐIỂM BÁO CÁO: 08/10/2026</div>
        </div>
        <div class="meta-box">
            <div><strong>Trang:</strong> 2 / 3</div>
            <div><strong>Môi trường:</strong> Full-Stack Live System</div>
        </div>
    </div>

    <div class="section-title">
        <span>III. HÌNH ẢNH MINH CHỨNG THỰC TẾ TRÊN CÁC PHÂN HỆ VẬN HÀNH</span>
    </div>

    <div class="img-grid-2">
        <div class="img-card">
            <img src="{img_staff_checkin}" alt="Check-in Map">
            <div class="img-caption">Hình 1: Nhân viên trực bãi Đô Nghĩa – Sơ đồ ô đỗ thời gian thực &amp; Cổng nhận xe</div>
        </div>
        <div class="img-card">
            <img src="{img_staff_checkout}" alt="Check-out Selected Vehicle">
            <div class="img-caption">Hình 2: Nhân viên Check-out – Tính cước theo thời gian đỗ &amp; Mở barrier xuất bến</div>
        </div>
        <div class="img-card">
            <img src="{img_customer_dash}" alt="Customer Active Session">
            <div class="img-caption">Hình 3: Khách hàng Dashboard – Theo dõi thời gian phiên đỗ xe &amp; Bản đồ dẫn đường</div>
        </div>
        <div class="img-card">
            <img src="{img_customer_receipt}" alt="Customer Receipt Modal">
            <div class="img-caption">Hình 4: Hóa đơn điện tử xuất bến – Chi tiết thời gian gửi, cước phí &amp; Thanh toán</div>
        </div>
        <div class="img-card">
            <img src="{img_admin_passes}" alt="Admin Monthly Passes">
            <div class="img-caption">Hình 5: Quản trị viên – Quản lý danh sách và phê duyệt vé tháng cư dân</div>
        </div>
        <div class="img-card">
            <img src="{img_dup_warning}" alt="Duplicate Checkin Warning">
            <div class="img-caption">Hình 6: Cơ chế an toàn – Cảnh báo chặn xe đã trong bãi cố tình check-in trùng lặp</div>
        </div>
    </div>

    <!-- ==================== TRANG 3 ==================== -->
    <div class="page-break"></div>

    <div class="academic-header">
        <div>
            <div class="univ-title">TRƯỜNG ĐẠI HỌC PHENIKAA – KHOA CÔNG NGHỆ THÔNG TIN</div>
            <div class="doc-title">BẢO ĐẢM CHẤT LƯỢNG VÀ KẾ HOẠCH BẢO VỆ ĐỒ ÁN</div>
            <div class="doc-subtitle">DỰ ÁN SMART PARKING SYSTEM (SPS) – THỜI ĐIỂM: 08/10/2026</div>
        </div>
        <div class="meta-box">
            <div><strong>Trang:</strong> 3 / 3</div>
            <div><strong>Giai đoạn:</strong> Hoàn thiện nghiệm thu</div>
        </div>
    </div>

    <div class="section-title">
        <span>IV. KẾT QUẢ KIỂM THỬ TỰ ĐỘNG &amp; BẢO ĐẢM CHẤT LƯỢNG (QA)</span>
    </div>

    <table>
        <thead>
            <tr>
                <th style="width: 30%;">Bộ kiểm thử (Test Suite)</th>
                <th style="width: 44%;">Mục tiêu kiểm định</th>
                <th style="width: 13%; text-align: center;">Số lượng</th>
                <th style="width: 13%; text-align: center;">Kết quả</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Unit Test: Thuật toán A*</strong> (<code>test_astar.py</code>)</td>
                <td>Đường đi thẳng, tự động né vật cản tĩnh/động, điểm xuất phát trùng đích, ngõ cụt.</td>
                <td style="text-align: center;">6 / 6 cases</td>
                <td style="text-align: center;"><span class="badge badge-success">100% PASSED</span></td>
            </tr>
            <tr>
                <td><strong>Unit Test: AI Engine</strong> (<code>test_ml_engine.py</code>)</td>
                <td>Dữ liệu phân phối chuẩn, tính tái lập theo seed, hội tụ mô hình, miền dự báo [0, 1].</td>
                <td style="text-align: center;">5 / 5 cases</td>
                <td style="text-align: center;"><span class="badge badge-success">100% PASSED</span></td>
            </tr>
            <tr>
                <td><strong>Concurrency Test: Race Condition</strong> (<code>test_double_booking.py</code>)</td>
                <td>Mô phỏng 2 tiến trình đồng thời đặt cùng 1 slot tại cùng 1 ms (SELECT FOR UPDATE).</td>
                <td style="text-align: center;">Multi-thread</td>
                <td style="text-align: center;"><span class="badge badge-success">CHẶN TRÙNG (409)</span></td>
            </tr>
            <tr>
                <td><strong>E2E Playwright Automation</strong> (<code>scratch/*.py</code>)</td>
                <td>Luồng liên hoàn: Đăng nhập -> Check-in -> Giải phóng slot -> Xuất bến tính cước.</td>
                <td style="text-align: center;">6 kịch bản</td>
                <td style="text-align: center;"><span class="badge badge-success">ỔN ĐỊNH 100%</span></td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">
        <span>V. ĐÁNH GIÁ RỦI RO KỸ THUẬT &amp; GIẢI PHÁP ĐÃ ÁP DỤNG</span>
    </div>

    <table>
        <thead>
            <tr>
                <th style="width: 25%;">Hạng mục rủi ro</th>
                <th style="width: 35%;">Khả năng tác động &amp; Nguy cơ</th>
                <th style="width: 40%;">Giải pháp công nghệ đã triển khai</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Xung đột đặt chỗ (Race Condition)</strong></td>
                <td>Nhiều khách cùng bấm đặt 1 vị trí đỗ tại cùng 1 thời điểm dẫn đến trùng lặp dữ liệu.</td>
                <td>Cài đặt khóa cấp dòng <code>SELECT FOR UPDATE</code> trên PostgreSQL, trả về HTTP 409 Conflict cho tiến trình sau.</td>
            </tr>
            <tr>
                <td><strong>Độ trễ tính toán tìm đường A*</strong></td>
                <td>Ma trận bãi xe kích thước lớn khiến thuật toán phản hồi chậm ảnh hưởng trải nghiệm lái xe.</td>
                <td>Tối ưu hàm ước lượng Heuristic Manhattan và hàng đợi ưu tiên <code>heapq</code>, rút ngắn thời gian xử lý xuống &lt; 5ms.</td>
            </tr>
            <tr>
                <td><strong>Xe gian lận Check-in trùng lặp</strong></td>
                <td>Tài xế cố tình quét mã lần 2 khi chưa xuất bến gây lỗi đếm thừa vị trí đỗ.</td>
                <td>Khóa logic: Kiểm tra phiên đỗ đang active; nếu tồn tại xe chưa checkout sẽ từ chối và cảnh báo âm thanh/thông báo.</td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">
        <span>VI. KẾ HOẠCH HOÀN THIỆN ĐỒ ÁN TRONG 2 TUẦN TỚI</span>
    </div>

    <ul style="margin: 4px 0 12px 0; padding-left: 18px; font-size: 8.8pt; color: #334155; line-height: 1.4;">
        <li><strong>Tuần 7 (09/10 – 16/10/2026):</strong> Tinh chỉnh toàn bộ tài liệu thuyết minh đồ án chuẩn Word (<code>.docx</code>), thiết kế bộ slide trình bày PowerPoint và chuẩn bị các biểu đồ so sánh mô hình học máy.</li>
        <li><strong>Tuần 8 (17/10 – 30/10/2026):</strong> Quay video demo trực tiếp luồng nghiệp vụ E2E trên hệ thống thực tế, rà soát mã nguồn lần cuối và tiến hành nghiệm thu, bảo vệ đồ án trước Hội đồng chấm thi.</li>
    </ul>

    <!-- CHỮ KÝ XÁC NHẬN -->
    <div class="footer-sign">
        <div>
            <div style="font-style: italic; margin-bottom: 3px;">Hà Nội, ngày 08 tháng 10 năm 2026</div>
            <div class="sign-title">GIẢNG VIÊN HƯỚNG DẪN</div>
            <div class="sign-name">(Ký và ghi rõ họ tên)</div>
        </div>
        <div>
            <div style="font-style: italic; margin-bottom: 3px;">Hà Nội, ngày 08 tháng 10 năm 2026</div>
            <div class="sign-title">SINH VIÊN THỰC HIỆN</div>
            <div class="sign-name">Phạm Văn Đạt<br><span style="font-size: 8.2pt; font-weight: normal; color: #64748b;">(MSV: 23017150)</span></div>
        </div>
    </div>

</body>
</html>
"""

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"SUCCESS: Wrote HTML file at {HTML_FILE}")

args = [
    EDGE_PATH,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_FILE}",
    f"file:///{HTML_FILE.replace(os.sep, '/')}"
]

subprocess.run(args, check=True)
print(f"SUCCESS: Generated PDF at {PDF_FILE}")

try:
    shutil.copy2(PDF_FILE, DOWNLOAD_PDF)
    print(f"SUCCESS: Copied to Downloads: {DOWNLOAD_PDF}")
except Exception as e:
    print(f"Notice copy to Downloads: {e}")

try:
    shutil.copy2(PDF_FILE, LEGACY_PDF)
    print(f"SUCCESS: Copied to legacy path: {LEGACY_PDF}")
except Exception as e:
    print(f"Notice copy to legacy: {e}")

# Verify exact page count
reader = pypdf.PdfReader(PDF_FILE)
print(f"VERIFICATION: Total pages in generated PDF: {len(reader.pages)}")
for i, page in enumerate(reader.pages):
    print(f"  - Page {i+1}: {len(page.extract_text())} characters")
