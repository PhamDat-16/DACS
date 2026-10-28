import os
from thesis_generator.style_helper import (
    add_chapter_heading, add_section_heading, add_subsection_heading,
    add_body_paragraph, add_bullet_item, add_image_figure, add_table_data,
    add_code_snippet
)

def add_chapter_4(doc):
    """
    CHƯƠNG 4: HIỆN THỰC HÓA VÀ XÂY DỰNG HỆ THỐNG
    Trình bày chi tiết Backend FastAPI, bảng 28 REST endpoints, WebSocket event-driven,
    Frontend Vue 3 + Tailwind CSS, 3 Cổng Customer, Staff, Admin, Barrier, Vé QR, Hóa đơn.
    """
    add_chapter_heading(doc, "CHƯƠNG 4: HIỆN THỰC HÓA VÀ XÂY DỰNG HỆ THỐNG")

    add_section_heading(doc, "4.1. Hiện thực hóa Backend với FastAPI và SQLAlchemy")
    add_body_paragraph(doc, "Tầng Backend đóng vai trò bộ não điều phối của toàn bộ hệ thống Smart Parking System, được xây dựng hoàn toàn bằng ngôn ngữ Python 3.11 trên nền tảng framework FastAPI. FastAPI cung cấp tốc độ thực thi bất đồng bộ (Asynchronous) tương đương NodeJS và Go nhờ thừa hưởng nền tảng Starlette và Pydantic.")

    add_subsection_heading(doc, "4.1.1. Cấu trúc mã nguồn Backend module hóa")
    add_body_paragraph(doc, "Mã nguồn Backend được tổ chức khoa học theo mô hình phân tầng trách nhiệm cao:")
    add_bullet_item(doc, "Chứa các cấu hình toàn cục (`config.py`), kết nối cơ sở dữ liệu và quản lý phiên (`database.py`), thuật toán băm mật khẩu và giải mã JWT (`security.py`).", bold_prefix="Tầng app/core/: ")
    add_bullet_item(doc, "Định nghĩa các lớp thực thể ánh xạ trực tiếp với bảng PostgreSQL bằng cú pháp Declarative Base của SQLAlchemy (`user.py`, `parking.py`, `booking.py`, `monthly_pass.py`).", bold_prefix="Tầng app/models/: ")
    add_bullet_item(doc, "Chứa các lớp Pydantic định nghĩa cấu trúc dữ liệu đầu vào (Request Validation) và chuẩn dữ liệu đầu ra (Response Serialization), đảm bảo tính toàn vẹn kiểu dữ liệu tĩnh.", bold_prefix="Tầng app/schemas/: ")
    add_bullet_item(doc, "Các bộ điều khiển định tuyến RESTful API phân tách theo từng miền nghiệp vụ (`auth.py`, `lots.py`, `slots.py`, `bookings.py`, `passes.py`, `ai.py`, `staff.py`).", bold_prefix="Tầng app/api/endpoints/: ")
    add_bullet_item(doc, "Chứa logic nghiệp vụ phức tạp tách biệt khỏi Controller: Thuật toán tìm đường A* (`astar.py`), bộ điều phối kết nối WebSocket thời gian thực (`websocket_manager.py`), dịch vụ sinh và xác thực mã QR (`qr_service.py`).", bold_prefix="Tầng app/services/: ")

    add_subsection_heading(doc, "4.1.2. Danh mục 28 REST API Endpoints của hệ thống")
    add_body_paragraph(doc, "Hệ thống cung cấp một bộ giao diện lập trình ứng dụng RESTful hoàn chỉnh bao gồm 28 endpoints chính, phục vụ đầy đủ mọi tương tác từ ứng dụng web của khách hàng, nhân viên và người quản trị:")

    api_headers = ["STT", "Phương thức", "Đường dẫn API", "Quyền hạn", "Mô tả chức năng nghiệp vụ"]
    api_rows = [
        ["1", "POST", "/api/v1/auth/register", "Public", "Đăng ký tài khoản khách hàng mới"],
        ["2", "POST", "/api/v1/auth/login", "Public", "Đăng nhập hệ thống, cấp phát Access Token JWT"],
        ["3", "GET", "/api/v1/auth/me", "Authenticated", "Lấy thông tin tài khoản đang đăng nhập"],
        ["4", "PUT", "/api/v1/auth/me", "Authenticated", "Cập nhật thông tin cá nhân của người dùng"],
        ["5", "GET", "/api/v1/lots/", "Public", "Lấy danh sách tất cả các bãi đỗ xe và số slot trống"],
        ["6", "GET", "/api/v1/lots/{lot_id}", "Public", "Lấy thông tin chi tiết một bãi đỗ cụ thể"],
        ["7", "POST", "/api/v1/lots/", "Admin", "Thêm mới một bãi đỗ xe vào hệ sinh thái"],
        ["8", "PUT", "/api/v1/lots/{lot_id}", "Admin", "Cập nhật thông tin, kích thước ma trận lưới bãi xe"],
        ["9", "DELETE", "/api/v1/lots/{lot_id}", "Admin", "Xóa bãi đỗ xe khỏi hệ thống"],
        ["10", "GET", "/api/v1/lots/{lot_id}/slots", "Public", "Lấy ma trận danh sách tất cả các ô đỗ của bãi"],
        ["11", "POST", "/api/v1/slots/", "Admin", "Thêm mới một vị trí ô đỗ cụ thể vào bãi"],
        ["12", "PUT", "/api/v1/slots/{slot_id}", "Admin, Staff", "Cập nhật trạng thái hoặc tọa độ ô đỗ"],
        ["13", "POST", "/api/v1/bookings/", "Customer", "Đặt giữ chỗ ô đỗ xe (khóa SELECT FOR UPDATE)"],
        ["14", "GET", "/api/v1/bookings/my", "Customer", "Xem danh sách các đơn đặt chỗ của cá nhân"],
        ["15", "GET", "/api/v1/bookings/{booking_id}", "Customer, Staff", "Lấy chi tiết đơn đặt chỗ và mã vé QR"],
        ["16", "POST", "/api/v1/bookings/{id}/cancel", "Customer", "Hủy đơn đặt chỗ khi chưa check-in vào bãi"],
        ["17", "POST", "/api/v1/staff/check-in", "Staff", "Quét QR hoặc nhập biển số để check-in mở barrier"],
        ["18", "POST", "/api/v1/staff/check-out", "Staff", "Quét QR check-out, tính phí và đóng barrier"],
        ["19", "POST", "/api/v1/staff/walk-in", "Staff", "Cấp phát ô đỗ nhanh cho phương tiện vãng lai"],
        ["20", "GET", "/api/v1/staff/live-status", "Staff", "Giám sát trạng thái thời gian thực bãi được phân công"],
        ["21", "POST", "/api/v1/navigation/find-path", "Customer", "Tính toán đường đi tối ưu A* từ cổng tới ô đỗ"],
        ["22", "GET", "/api/v1/passes/my", "Customer", "Xem danh sách vé tháng đang sở hữu"],
        ["23", "POST", "/api/v1/passes/subscribe", "Customer", "Đăng ký mua gói vé tháng mới"],
        ["24", "GET", "/api/v1/ai/forecast", "Admin", "Lấy dữ liệu dự báo tỷ lệ lấp đầy từ Random Forest"],
        ["25", "GET", "/api/v1/admin/analytics", "Admin", "Lấy dữ liệu thống kê doanh thu, lưu lượng xe"],
        ["26", "GET", "/api/v1/admin/users", "Admin", "Danh sách toàn bộ người dùng trong hệ thống"],
        ["27", "POST", "/api/v1/admin/staff", "Admin", "Tạo tài khoản nhân viên kèm bãi làm việc (assigned_lot)"],
        ["28", "PUT", "/api/v1/admin/users/{id}/role", "Admin", "Phân quyền vai trò người dùng trong hệ thống"]
    ]
    add_table_data(doc, "Bảng 4.1", "Danh mục tổng hợp 28 RESTful API Endpoints của Hệ thống Smart Parking System", api_headers, api_rows, col_widths=[1.0, 1.8, 5.0, 2.5, 5.2])

    add_subsection_heading(doc, "4.1.3. Cơ chế giao tiếp thời gian thực hai chiều WebSocket")
    add_body_paragraph(doc, "Để đảm bảo màn hình nhân viên bảo vệ và ứng dụng khách hàng luôn cập nhật tức thời màu sắc trạng thái ô đỗ (Trống -> Đỏ khi có xe vào) mà không cần phải thực hiện thao tác tải lại trang (F5) hay gửi yêu cầu Polling liên tục làm quá tải máy chủ, hệ thống triển khai giao thức WebSocket hai chiều thông qua lớp `ConnectionManager`:")

    ws_code = """# Trích đoạn ConnectionManager tại app/services/websocket_manager.py
class ConnectionManager:
    def __init__(self):
        # Lưu trữ danh sách WebSocket đang mở theo từng bãi đỗ lot_id
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, lot_id: int):
        await websocket.accept()
        if lot_id not in self.active_connections:
            self.active_connections[lot_id] = []
        self.active_connections[lot_id].append(websocket)

    def disconnect(self, websocket: WebSocket, lot_id: int):
        if lot_id in self.active_connections:
            self.active_connections[lot_id].remove(websocket)

    async def broadcast_slot_update(self, lot_id: int, slot_id: int, new_status: str):
        # Phát thông báo Broadcast tới toàn bộ Client đang quan sát bãi xe lot_id
        message = {"type": "SLOT_UPDATE", "slot_id": slot_id, "status": new_status}
        if lot_id in self.active_connections:
            for connection in self.active_connections[lot_id]:
                await connection.send_json(message)"""
    add_code_snippet(doc, "Lớp ConnectionManager điều phối thông điệp WebSocket thời gian thực", ws_code)

    add_section_heading(doc, "4.2. Hiện thực hóa Frontend với Vue 3 và Tailwind CSS")
    add_body_paragraph(doc, "Giao diện người dùng của hệ thống được xây dựng theo kiến trúc Single Page Application (SPA) hiện đại với bộ công cụ Vue.js 3 (Composition API với cú pháp `<script setup>`), Vite build tool siêu tốc, Tailwind CSS hỗ trợ thiết kế giao diện linh hoạt theo phong cách Utility-first và Pinia đóng vai trò trung tâm quản lý trạng thái phiên làm việc.")

    add_subsection_heading(doc, "4.2.1. Cổng giao diện dành cho Khách hàng (Customer Portal)")
    add_body_paragraph(doc, "Cổng giao diện khách hàng được thiết kế tối ưu hóa trải nghiệm trên màn hình di động thông minh (Mobile First):")
    add_bullet_item(doc, "Hiển thị danh sách các bãi đỗ với bộ lọc theo khoảng cách, mức giá và số ô trống còn lại. Bản đồ ma trận lưới trực quan cho phép người dùng chạm để chọn ô đỗ mong muốn.", bold_prefix="Trang khám phá bãi đỗ xe và đặt chỗ: ")
    add_bullet_item(doc, "Khi người dùng chọn một ô đỗ bất kỳ, hệ thống vẽ một đường nét đứt phát sáng màu xanh chỉ đường từ cổng barrier vào tận ô đỗ, đi kèm mô phỏng xe chạy từng bước.", bold_prefix="Trang điều hướng chỉ đường A*: ")
    add_bullet_item(doc, "Sau khi đặt chỗ thành công, hệ thống kết xuất một vé điện tử chứa mã QR động kèm thông tin: Biển số xe, vị trí ô đỗ, mã đơn, giờ hết hạn. Khách hàng chỉ cần đưa màn hình điện thoại trước camera cổng barrier để vào bãi.", bold_prefix="Trang chi tiết vé điện tử QR Code: ")
    add_bullet_item(doc, "Cung cấp các gói thuê bao vé tháng (30 ngày, 90 ngày) giúp cư dân chung cư hoặc nhân viên văn phòng gửi xe cố định với mức giá ưu đãi và thủ tục gia hạn trực tuyến.", bold_prefix="Trang quản lý thẻ tháng (Monthly Passes): ")

    add_image_figure(
        doc,
        fig_id="Hình 4.1",
        fig_title="Giao diện Cổng khách hàng: Bản đồ đặt chỗ và Vé điện tử chứa mã QR",
        image_path=os.path.join(os.getcwd(), "screenshots", "qr_booking_modal.png"),
        note_instructions="Ảnh chụp màn hình thực tế Cổng khách hàng với Modal đặt chỗ và Vé điện tử có mã QR."
    )

    add_subsection_heading(doc, "4.2.2. Cổng giao diện dành cho Nhân viên vận hành (Staff Portal)")
    add_body_paragraph(doc, "Cổng nhân viên được thiết kế riêng biệt để phục vụ công tác giám sát tại chòi bảo vệ với tốc độ phản hồi tức thời:")
    add_bullet_item(doc, "Nhân viên khi đăng nhập sẽ chỉ nhìn thấy duy nhất bãi xe được quản trị viên phân công (`assigned_lot`). Giao diện hiển thị tổng số xe đang gửi, số ô trống, doanh thu ca trực và danh sách cảnh báo.", bold_prefix="Bảng điều khiển bãi xe trực: ")
    add_bullet_item(doc, "Hiển thị ma trận toàn bộ các ô đỗ của bãi. Các ô đỗ được gán màu tự động theo thời gian thực (Xanh lá: Trống; Đỏ: Có xe; Vàng: Đã đặt trước; Xám: Hỏng bảo trì) nhờ kết nối WebSocket.", bold_prefix="Lưới giám sát ô đỗ thời gian thực: ")
    add_bullet_item(doc, "Tích hợp thư viện quét mã vạch qua webcam/camera thiết bị (`html5-qrcode`). Khi khách hàng xuất trình mã QR, hệ thống tự động giải mã, kiểm tra tính hợp lệ của vé và phát hiệu ứng mở cần barrier trên màn hình.", bold_prefix="Trình quét mã QR và Điều khiển Barrier: ")
    add_bullet_item(doc, "Đối với các khách hàng lớn tuổi hoặc phương tiện không đặt trước, nhân viên có thể bấm nút Check-in vãng lai, hệ thống tự động tìm và gán ô trống gần cổng nhất chỉ trong 1 cú nhấp chuột.", bold_prefix="Tiếp nhận xe vãng lai (Walk-in Check-in): ")

    add_image_figure(
        doc,
        fig_id="Hình 4.2",
        fig_title="Giao diện Cổng nhân viên: Lưới giám sát ô đỗ thời gian thực và Cửa sổ quét QR Barrier",
        image_path=os.path.join(os.getcwd(), "screenshots", "shift_handover_verified.png"),
        note_instructions="Ảnh chụp màn hình thực tế Bảng điều khiển nhân viên trực bãi và giao diện mở Barrier khi quét QR."
    )

    add_subsection_heading(doc, "4.2.3. Cổng giao diện dành cho Quản trị viên (Admin Portal)")
    add_body_paragraph(doc, "Cổng quản trị viên là trung tâm điều hành toàn diện của chuỗi bãi đỗ xe thông minh:")
    add_bullet_item(doc, "Trình quản lý trực quan cho phép thêm mới bãi đỗ xe, xác định địa chỉ chính xác, cấu hình kích thước ma trận $Width \\times Height$ và biểu phí gửi xe theo giờ.", bold_prefix="Quản lý danh mục bãi đỗ và cấu hình ma trận: ")
    add_bullet_item(doc, "Quản trị viên có thể tạo mới tài khoản cho nhân viên bảo vệ, đặc biệt có mục lựa chọn địa chỉ/bãi đỗ xe cụ thể nơi nhân viên làm việc (`assigned_lot`), đảm bảo tính chặt chẽ trong phân quyền quản lý.", bold_prefix="Quản lý tài khoản nhân viên (Staff Management): ")
    add_bullet_item(doc, "Tích hợp biểu đồ Chart.js trực quan hóa doanh thu theo ngày, tỷ lệ lấp đầy theo khung giờ và sản lượng phương tiện ra vào theo từng loại xe.", bold_prefix="Báo cáo phân tích doanh thu & vận hành: ")
    add_bullet_item(doc, "Trang AI Analytics hiển thị biểu đồ dự báo tỷ lệ lấp đầy trong 24 giờ tiếp theo do mô hình Random Forest Regressor tính toán, đưa ra các cảnh báo khung giờ cao điểm sắp diễn ra để ban quản lý chủ động điều tiết.", bold_prefix="Bảng điều khiển Trí tuệ nhân tạo (AI Forecast): ")

    add_image_figure(
        doc,
        fig_id="Hình 4.3",
        fig_title="Giao diện Cổng quản trị viên: Dashboard doanh thu và Quản trị hệ thống",
        image_path=os.path.join(os.getcwd(), "screenshots", "authenticated_dashboard.png"),
        note_instructions="Ảnh chụp màn hình thực tế Admin Dashboard quản trị bãi đỗ, phân tích doanh thu và quản lý tài khoản nhân viên."
    )

