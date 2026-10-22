import os
from thesis_generator.style_helper import (
    add_chapter_heading, add_section_heading, add_subsection_heading,
    add_body_paragraph, add_bullet_item, add_image_figure, add_table_data,
    add_code_snippet
)

def add_chapter_2(doc):
    """
    CHƯƠNG 2: PHÂN TÍCH YÊU CẦU VÀ THIẾT KẾ HỆ THỐNG
    Đặc tả chi tiết các tác nhân, Use Case, Kiến trúc 3 tầng, CSDL ERD 6 bảng,
    Kiểm soát đồng thời SELECT FOR UPDATE và bảo mật phân quyền.
    """
    add_chapter_heading(doc, "CHƯƠNG 2: PHÂN TÍCH YÊU CẦU VÀ THIẾT KẾ HỆ THỐNG")

    add_section_heading(doc, "2.1. Phân tích yêu cầu hệ thống")
    add_body_paragraph(doc, "Để xây dựng một hệ thống phần mềm quản lý bãi đỗ xe thông minh hoạt động ổn định, chính xác và thân thiện với người sử dụng, việc xác định đầy đủ các yêu cầu chức năng (Functional Requirements) và yêu cầu phi chức năng (Non-functional Requirements) đóng vai trò quyết định sống còn đối với sự thành bại của dự án.")

    add_subsection_heading(doc, "2.1.1. Yêu cầu chức năng (Functional Requirements)")
    add_body_paragraph(doc, "Hệ thống Smart Parking System phục vụ 3 nhóm đối tượng người dùng (Actors) chính với các quyền hạn và vai trò tách biệt rõ rệt:")

    add_bullet_item(doc, "Đăng ký tài khoản, đăng nhập hệ thống an toàn bằng mật khẩu mã hóa Bcrypt.", bold_prefix="Khách hàng (Customer): ")
    add_bullet_item(doc, "Xem danh sách và bản đồ trực quan các bãi đỗ xe trong mạng lưới; xem số lượng vị trí đỗ còn trống theo thời gian thực (Live Slot Count).", bold_prefix="Khách hàng (Customer): ")
    add_bullet_item(doc, "Đặt giữ chỗ đỗ xe trước (Booking Reservation) với cơ chế khóa chỗ tức thời, chọn thời gian bắt đầu và kết thúc dự kiến.", bold_prefix="Khách hàng (Customer): ")
    add_bullet_item(doc, "Tra cứu lộ trình dẫn đường tối ưu 2D từ cổng vào bãi tới đúng ô đỗ đã đặt thông qua thuật toán A*.", bold_prefix="Khách hàng (Customer): ")
    add_bullet_item(doc, "Xem và xuất vé đỗ xe điện tử có chứa mã QR Code động để xác thực tại cổng ra/vào.", bold_prefix="Khách hàng (Customer): ")
    add_bullet_item(doc, "Đăng ký vé tháng (Monthly Pass Subscription) cho phương tiện thường xuyên lưu trú để nhận mức giá ưu đãi.", bold_prefix="Khách hàng (Customer): ")
    add_bullet_item(doc, "Quản lý danh sách phương tiện cá nhân (biển số, loại xe) và xem lịch sử các lượt gửi xe kèm hóa đơn thanh toán điện tử.", bold_prefix="Khách hàng (Customer): ")

    add_bullet_item(doc, "Đăng nhập cổng nghiệp vụ bãi xe, hệ thống tự động khóa phạm vi quản lý theo điểm đỗ được phân công (assigned_lot).", bold_prefix="Nhân viên vận hành (Staff / Operator): ")
    add_bullet_item(doc, "Giám sát bảng điều khiển trực quan (Parking Lot Grid View) hiển thị trạng thái từng ô đỗ: Trống (Green), Đang có xe (Red), Đã đặt trước (Yellow), Đang bảo trì (Gray).", bold_prefix="Nhân viên vận hành (Staff / Operator): ")
    add_bullet_item(doc, "Vận hành cổng Barrier vào/ra: Quét mã QR của khách hàng, đối chiếu thông tin biển số xe, kích hoạt sự kiện mở barrier.", bold_prefix="Nhân viên vận hành (Staff / Operator): ")
    add_bullet_item(doc, "Tiếp nhận xe vãng lai (Check-in thủ công trực tiếp): Cấp phát nhanh ô đỗ trống gần nhất cho khách không đặt trước qua app.", bold_prefix="Nhân viên vận hành (Staff / Operator): ")
    add_bullet_item(doc, "Xử lý check-out và thu phí: Tính toán tổng thời lượng đỗ thực tế, áp dụng bảng giá tương ứng và in hóa đơn điện tử.", bold_prefix="Nhân viên vận hành (Staff / Operator): ")

    add_bullet_item(doc, "Quản lý toàn bộ danh mục bãi đỗ xe trong hệ thống (Thêm, sửa, xóa thông tin bãi, cấu hình ma trận lưới layout tọa độ $X \\times Y$).", bold_prefix="Quản trị viên (Admin): ")
    add_bullet_item(doc, "Quản lý danh mục từng vị trí đỗ (Parking Slots): Định danh mã ô đỗ, tọa độ $(x, y)$, phân loại xe (ô tô, xe máy, xe điện sạc).", bold_prefix="Quản trị viên (Admin): ")
    add_bullet_item(doc, "Quản trị người dùng và nhân sự: Cấp tài khoản cho nhân viên bãi, gán quyền làm việc tại bãi đỗ cụ thể (địa chỉ nơi làm việc rõ ràng).", bold_prefix="Quản trị viên (Admin): ")
    add_bullet_item(doc, "Bảng biểu thống kê Dashboard tài chính: Biểu đồ doanh thu theo ngày/tháng/năm, tỷ lệ lấp đầy (Occupancy Rate) trung bình.", bold_prefix="Quản trị viên (Admin): ")
    add_bullet_item(doc, "Vận hành mô hình Trí tuệ nhân tạo (AI): Xem biểu đồ dự báo nhu cầu đỗ xe trong 24 giờ tới được tạo ra bởi mô hình Random Forest Regressor.", bold_prefix="Quản trị viên (Admin): ")

    add_subsection_heading(doc, "2.1.2. Yêu cầu phi chức năng (Non-functional Requirements)")
    add_bullet_item(doc, "Thời gian phản hồi (Response Time) của các API nghiệp vụ thông thường phải dưới 200ms; API tính toán đường đi A* dưới 100ms; cập nhật trạng thái WebSocket tức thì dưới 50ms.", bold_prefix="Hiệu năng (Performance): ")
    add_bullet_item(doc, "Mật khẩu người dùng bắt buộc mã hóa salt hashing bằng Bcrypt trước khi lưu trữ vào CSDL; xác thực phiên làm việc thông qua JWT (JSON Web Token) có thời hạn sống (Expires Time) chặt chẽ; phân quyền dựa trên vai trò (Role-Based Access Control - RBAC).", bold_prefix="Bảo mật (Security): ")
    add_bullet_item(doc, "Đảm bảo tính toàn vẹn dữ liệu trong môi trường đa luồng; ngăn chặn triệt để tình trạng hai khách hàng cùng đặt thành công một vị trí đỗ tại cùng một thời điểm (Race Condition / Double-booking).", bold_prefix="Tính nhất quán và toàn vẹn (Data Consistency): ")
    add_bullet_item(doc, "Kiến trúc Backend dạng Stateless RESTful cho phép dễ dàng mở rộng chiều ngang (Horizontal Scaling); cơ sở dữ liệu PostgreSQL chuẩn hóa đáp ứng hàng trăm ngàn lượt giao dịch mỗi ngày.", bold_prefix="Khả năng mở rộng (Scalability): ")
    add_bullet_item(doc, "Giao diện người dùng được thiết kế chuẩn Responsive Design (tương thích máy tính để bàn, máy tính bảng và điện thoại di động thông minh), giao diện sáng tạo, thông báo lỗi trực quan.", bold_prefix="Tính khả dụng (Usability): ")

    add_section_heading(doc, "2.2. Mô hình hóa chức năng hệ thống (UML Use Case)")
    add_body_paragraph(doc, "Sơ đồ Use Case tổng quát giúp phân định ranh giới hệ thống, các tác nhân bên ngoài và các nhóm ca sử dụng chính trong hệ thống quản lý bãi đỗ xe thông minh.")

    add_image_figure(
        doc,
        fig_id="Hình 2.1",
        fig_title="Sơ đồ Use Case tổng quát của Hệ thống Smart Parking System",
        image_path=os.path.join(os.getcwd(), "report_images", "fig2_1_usecase.png"),
        note_instructions="Sơ đồ Use Case tổng thể mô tả 3 Actor: Customer, Staff, Admin và các chức năng then chốt của hệ thống."
    )

    add_body_paragraph(doc, "Chi tiết các ca sử dụng then chốt của từng tác nhân được đặc tả trong bảng phân rã chức năng dưới đây:")

    uc_headers = ["Mã UC", "Tên ca sử dụng", "Tác nhân chính", "Mô tả vắn tắt chức năng"]
    uc_rows = [
        ["UC-01", "Đăng ký / Đăng nhập", "Khách hàng, Nhân viên, Admin", "Xác thực danh tính qua JWT Token, phân luồng quyền hạn tương ứng"],
        ["UC-02", "Tra cứu bãi & Xem slot", "Khách hàng", "Hiển thị danh sách bãi đỗ và tình trạng slot trống theo thời gian thực"],
        ["UC-03", "Đặt giữ chỗ đỗ xe", "Khách hàng", "Chọn vị trí đỗ, khóa ô đỗ (SELECT FOR UPDATE) và khởi tạo đơn đặt chỗ"],
        ["UC-04", "Dẫn đường chỉ lối A*", "Khách hàng", "Hiển thị bản đồ 2D và đường đi tối ưu từ cổng bãi tới ô đỗ đã chọn"],
        ["UC-05", "Xem vé điện tử QR", "Khách hàng", "Tạo và hiển thị mã QR Code chứa mã vé để quét tại cổng kiểm soát"],
        ["UC-06", "Đăng ký vé tháng", "Khách hàng", "Mua gói vé tháng cho phương tiện cá nhân để hưởng ưu đãi theo định kỳ"],
        ["UC-07", "Giám sát lưới bãi đỗ", "Nhân viên, Admin", "Xem bản đồ trạng thái thời gian thực của toàn bộ ô đỗ tại bãi trực"],
        ["UC-08", "Quét QR Check-in/out", "Nhân viên", "Quét mã QR của phương tiện, đối chiếu dữ liệu và kích hoạt đóng mở barrier"],
        ["UC-09", "Check-in xe vãng lai", "Nhân viên", "Cấp phát nhanh ô đỗ trống trực tiếp cho khách hàng không đặt trước"],
        ["UC-10", "Thu phí & Xuất hóa đơn", "Nhân viên", "Tính toán phí đỗ thực tế theo biểu giá, cập nhật trạng thái đã thanh toán"],
        ["UC-11", "Quản lý bãi & Cấu hình Slot", "Admin", "Thêm, cập nhật kích thước lưới ma trận bãi đỗ và danh mục ô đỗ chi tiết"],
        ["UC-12", "Quản lý tài khoản Staff", "Admin", "Cấp tài khoản nhân viên, cấu hình địa chỉ bãi đỗ xe làm việc (assigned_lot)"],
        ["UC-13", "Dự báo nhu cầu AI", "Admin", "Hiển thị kết quả dự báo tỷ lệ lấp đầy trong tương lai từ mô hình Random Forest"]
    ]
    add_table_data(doc, "Bảng 2.1", "Danh mục đặc tả các ca sử dụng (Use Cases) chính trong hệ thống", uc_headers, uc_rows, col_widths=[2.0, 4.2, 4.0, 5.8])

    add_section_heading(doc, "2.3. Thiết kế kiến trúc hệ thống (System Architecture)")
    add_body_paragraph(doc, "Hệ thống Smart Parking System được thiết kế theo mô hình Kiến trúc 3 tầng (Three-Tier Architecture) hiện đại kết hợp với cơ chế truyền thông thời gian thực Event-driven thông qua WebSocket:")

    add_bullet_item(doc, "Xây dựng dưới dạng Single Page Application (SPA) bằng Vue.js 3 (Composition API), Vite, Tailwind CSS và công cụ quản lý trạng thái tập trung Pinia. Tầng giao diện chịu trách nhiệm kết xuất đồ họa ma trận bãi xe, hiển thị hoạt ảnh chuyển động xe bằng GreenSock GSAP 3, quét mã QR và tương tác thân thiện với người dùng.", bold_prefix="1. Tầng Giao diện người dùng (Presentation Tier - Frontend): ")
    add_bullet_item(doc, "Được xây dựng trên nền tảng FastAPI (Python 3.11) chạy trên máy chủ ASGI Uvicorn. Tầng này chịu trách nhiệm tiếp nhận yêu cầu HTTP/REST, xác thực JWT, thực thi logic nghiệp vụ (thuật toán tìm đường A*, kiểm tra tính khả dụng của ô đỗ, tính toán chi phí), duy trì kết nối WebSocket để phát thông báo đa điểm (Broadcast) khi trạng thái ô đỗ thay đổi, đồng thời nạp mô hình học máy Random Forest Regressor đã được đóng gói (.joblib) vào bộ nhớ Singleton để phản hồi dự báo tức thời.", bold_prefix="2. Tầng Logic nghiệp vụ (Application / Business Logic Tier - Backend): ")
    add_bullet_item(doc, "Sử dụng Hệ quản trị cơ sở dữ liệu quan hệ PostgreSQL mạnh mẽ. Tương tác với CSDL thông qua SQLAlchemy ORM và tầng kết nối Asyncpg / Psycopg2. Đảm bảo tính toàn vẹn dữ liệu ACID và hỗ trợ kỹ thuật khóa bản ghi chống xung đột dữ liệu.", bold_prefix="3. Tầng Dữ liệu (Data Tier - Database): ")

    add_image_figure(
        doc,
        fig_id="Hình 2.2",
        fig_title="Kiến trúc tổng thể 3 tầng và luồng dữ liệu của Hệ thống Smart Parking System",
        image_path=os.path.join(os.getcwd(), "report_images", "fig2_2_arch.png"),
        note_instructions="Sơ đồ kiến trúc 3 tầng: Tầng Trình diễn (Vue 3/Tailwind/GSAP), Tầng Logic (FastAPI/WebSocket/A*/Random Forest) và Tầng Dữ liệu (PostgreSQL/SQLAlchemy)."
    )

    add_section_heading(doc, "2.4. Thiết kế cơ sở dữ liệu quan hệ (Database Design)")
    add_body_paragraph(doc, "Cơ sở dữ liệu của dự án được chuẩn hóa theo dạng chuẩn 3NF (Third Normal Form) nhằm loại bỏ trùng lặp dữ liệu, đảm bảo toàn vẹn tham chiếu và tối ưu hóa tốc độ truy vấn. Cơ sở dữ liệu bao gồm 6 bảng thực thể cốt lõi gắn kết chặt chẽ với nhau:")

    add_image_figure(
        doc,
        fig_id="Hình 2.3",
        fig_title="Sơ đồ thực thể liên kết (Entity Relationship Diagram - ERD) của hệ thống",
        image_path=os.path.join(os.getcwd(), "report_images", "fig2_3_erd.png"),
        note_instructions="Sơ đồ ERD 6 bảng dữ liệu thực tế của hệ thống: users, parking_lots, parking_slots, bookings, sessions và occupancy_history."
    )

    add_subsection_heading(doc, "2.4.1. Chi tiết cấu trúc các bảng dữ liệu trong CSDL")

    # Bảng 1: users
    users_headers = ["Tên trường", "Kiểu dữ liệu", "Ràng buộc", "Mô tả ý nghĩa"]
    users_rows = [
        ["id", "INTEGER", "PK, Auto Increment", "Mã định danh duy nhất của tài khoản"],
        ["email", "VARCHAR(255)", "UNIQUE, NOT NULL", "Địa chỉ email dùng để đăng nhập hệ thống"],
        ["password_hash", "VARCHAR(255)", "NOT NULL", "Mật khẩu người dùng đã băm an toàn bằng Bcrypt"],
        ["full_name", "VARCHAR(255)", "NOT NULL", "Họ và tên đầy đủ của người dùng"],
        ["phone_number", "VARCHAR(20)", "NULLABLE", "Số điện thoại liên hệ"],
        ["role", "VARCHAR(20)", "NOT NULL, DEFAULT 'customer'", "Vai trò hệ thống: 'customer', 'staff', 'admin'"],
        ["assigned_lot_id", "INTEGER", "FK -> parking_lots(id), NULLABLE", "Bãi đỗ xe nhân viên được phân công làm việc (nơi làm việc)"],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Thời điểm tạo tài khoản"]
    ]
    add_table_data(doc, "Bảng 2.2", "Cấu trúc chi tiết bảng lưu trữ thông tin người dùng (users)", users_headers, users_rows, col_widths=[2.5, 3.2, 3.8, 6.5])

    # Bảng 2: parking_lots
    lots_headers = ["Tên trường", "Kiểu dữ liệu", "Ràng buộc", "Mô tả ý nghĩa"]
    lots_rows = [
        ["id", "INTEGER", "PK, Auto Increment", "Mã định danh duy nhất của bãi đỗ xe"],
        ["name", "VARCHAR(255)", "NOT NULL", "Tên bãi đỗ (Ví dụ: Bãi đỗ xe Đô Nghĩa - Tòa A)"],
        ["address", "VARCHAR(500)", "NOT NULL", "Địa chỉ chi tiết nơi đặt bãi đỗ"],
        ["total_slots", "INTEGER", "NOT NULL, DEFAULT 0", "Tổng số lượng ô đỗ được thiết kế tại bãi"],
        ["hourly_rate", "DECIMAL(10, 2)", "NOT NULL, DEFAULT 15000", "Đơn giá gửi xe theo giờ (VNĐ/giờ)"],
        ["grid_width", "INTEGER", "NOT NULL, DEFAULT 10", "Chiều rộng ma trận bản đồ bãi xe (số cột X)"],
        ["grid_height", "INTEGER", "NOT NULL, DEFAULT 8", "Chiều cao ma trận bản đồ bãi xe (số hàng Y)"],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Thời điểm bãi đỗ được khởi tạo trên hệ thống"]
    ]
    add_table_data(doc, "Bảng 2.3", "Cấu trúc chi tiết bảng thông tin bãi đỗ xe (parking_lots)", lots_headers, lots_rows, col_widths=[2.5, 3.2, 3.8, 6.5])

    # Bảng 3: parking_slots
    slots_headers = ["Tên trường", "Kiểu dữ liệu", "Ràng buộc", "Mô tả ý nghĩa"]
    slots_rows = [
        ["id", "INTEGER", "PK, Auto Increment", "Mã định danh ô đỗ xe"],
        ["lot_id", "INTEGER", "FK -> parking_lots(id), NOT NULL", "Tham chiếu đến bãi đỗ xe sở hữu"],
        ["slot_number", "VARCHAR(50)", "NOT NULL", "Mã ký hiệu ô đỗ (Ví dụ: 'A-01', 'B-12')"],
        ["pos_x", "INTEGER", "NOT NULL", "Tọa độ cột trên ma trận bản đồ 2D"],
        ["pos_y", "INTEGER", "NOT NULL", "Tọa độ hàng trên ma trận bản đồ 2D"],
        ["status", "VARCHAR(20)", "NOT NULL, DEFAULT 'available'", "Trạng thái: 'available', 'occupied', 'reserved', 'maintenance'"],
        ["vehicle_type", "VARCHAR(20)", "NOT NULL, DEFAULT 'car'", "Phân loại xe tương thích: 'car', 'bike'"],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Thời điểm khởi tạo vị trí ô đỗ"]
    ]
    add_table_data(doc, "Bảng 2.4", "Cấu trúc chi tiết bảng danh mục ô đỗ (parking_slots)", slots_headers, slots_rows, col_widths=[2.5, 3.2, 3.8, 6.5])

    # Bảng 4: bookings
    bookings_headers = ["Tên trường", "Kiểu dữ liệu", "Ràng buộc", "Mô tả ý nghĩa"]
    bookings_rows = [
        ["id", "INTEGER", "PK, Auto Increment", "Mã định danh giao dịch đặt chỗ / gửi xe"],
        ["booking_code", "VARCHAR(64)", "UNIQUE, NOT NULL", "Mã đơn đặt vé duy nhất dùng để tạo mã QR Code"],
        ["user_id", "INTEGER", "FK -> users(id), NOT NULL", "Khách hàng thực hiện đơn đặt chỗ"],
        ["slot_id", "INTEGER", "FK -> parking_slots(id), NOT NULL", "Vị trí ô đỗ được phân bổ"],
        ["license_plate", "VARCHAR(30)", "NOT NULL", "Biển số xe đăng ký vào bãi"],
        ["start_time", "TIMESTAMP", "NOT NULL", "Thời gian bắt đầu đặt hoặc check-in thực tế"],
        ["end_time", "TIMESTAMP", "NULLABLE", "Thời gian kết thúc đặt dự kiến hoặc check-out thực tế"],
        ["status", "VARCHAR(30)", "NOT NULL, DEFAULT 'confirmed'", "Trạng thái: 'confirmed', 'checked_in', 'completed', 'cancelled'"],
        ["total_amount", "DECIMAL(12, 2)", "NOT NULL, DEFAULT 0.0", "Tổng số tiền phí gửi xe cần thanh toán"],
        ["payment_status", "VARCHAR(20)", "NOT NULL, DEFAULT 'pending'", "Trạng thái thanh toán: 'pending', 'paid', 'refunded'"],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Thời điểm tạo đơn đặt chỗ"]
    ]
    add_table_data(doc, "Bảng 2.5", "Cấu trúc chi tiết bảng quản lý đặt chỗ và lịch sử gửi xe (bookings)", bookings_headers, bookings_rows, col_widths=[2.5, 3.2, 3.8, 6.5])

    # Bảng 5: monthly_passes
    mp_headers = ["Tên trường", "Kiểu dữ liệu", "Ràng buộc", "Mô tả ý nghĩa"]
    mp_rows = [
        ["id", "INTEGER", "PK, Auto Increment", "Mã định danh vé tháng"],
        ["pass_code", "VARCHAR(64)", "UNIQUE, NOT NULL", "Mã vé tháng duy nhất tạo mã QR thẻ định kỳ"],
        ["user_id", "INTEGER", "FK -> users(id), NOT NULL", "Chủ sở hữu vé tháng"],
        ["lot_id", "INTEGER", "FK -> parking_lots(id), NOT NULL", "Bãi đỗ xe áp dụng vé tháng"],
        ["license_plate", "VARCHAR(30)", "NOT NULL", "Biển số xe đăng ký vé tháng cố định"],
        ["start_date", "DATE", "NOT NULL", "Ngày bắt đầu có hiệu lực của vé tháng"],
        ["end_date", "DATE", "NOT NULL", "Ngày hết hạn hiệu lực của vé tháng"],
        ["price", "DECIMAL(12, 2)", "NOT NULL", "Mức phí thuê vé tháng theo gói"],
        ["is_active", "BOOLEAN", "NOT NULL, DEFAULT TRUE", "Trạng thái thẻ còn hiệu lực hay đã khóa"],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Thời điểm kích hoạt vé tháng"]
    ]
    add_table_data(doc, "Bảng 2.6", "Cấu trúc chi tiết bảng đăng ký vé tháng (monthly_passes)", mp_headers, mp_rows, col_widths=[2.5, 3.2, 3.8, 6.5])

    # Bảng 6: ai_occupancy_logs
    ai_headers = ["Tên trường", "Kiểu dữ liệu", "Ràng buộc", "Mô tả ý nghĩa"]
    ai_rows = [
        ["id", "INTEGER", "PK, Auto Increment", "Mã định danh bản ghi lưu vết dữ liệu AI"],
        ["lot_id", "INTEGER", "FK -> parking_lots(id), NOT NULL", "Bãi đỗ xe được theo dõi tỷ lệ đỗ"],
        ["timestamp", "TIMESTAMP", "NOT NULL", "Thời điểm ghi nhận mẫu số liệu thực tế"],
        ["occupied_slots", "INTEGER", "NOT NULL", "Số lượng ô đỗ đang có xe thực tế tại thời điểm đó"],
        ["total_slots", "INTEGER", "NOT NULL", "Tổng số ô đỗ của bãi tại thời điểm đó"],
        ["occupancy_rate", "FLOAT", "NOT NULL", "Tỷ lệ lấp đầy tính theo phần trăm (0.0 - 1.0)"],
        ["predicted_rate", "FLOAT", "NULLABLE", "Tỷ lệ dự báo từ mô hình Random Forest đối chứng"]
    ]
    add_table_data(doc, "Bảng 2.7", "Cấu trúc chi tiết bảng nhật ký dự báo AI (ai_occupancy_logs)", ai_headers, ai_rows, col_widths=[2.5, 3.2, 3.8, 6.5])

    add_section_heading(doc, "2.5. Giải pháp kiểm soát đồng thời chống xung đột đặt chỗ (Race Condition)")
    add_body_paragraph(doc, "Trong các hệ thống phân tán và ứng dụng web có lượng truy cập đồng thời cao, bài toán tương tranh (Concurrency) khi hai người dùng cùng bấm nút đặt một vị trí đỗ tại cùng một mili-giây (Double-booking problem) là một thách thức kỹ thuật sống còn.")
    add_body_paragraph(doc, "Nếu chỉ sử dụng câu lệnh kiểm tra thông thường dạng 'SELECT status FROM parking_slots WHERE id = X' sau đó cập nhật 'UPDATE parking_slots SET status = reserved', thì giữa thời điểm đọc và ghi sẽ tồn tại một khoảng trễ thời gian (Race Condition Window). Cả hai phiên làm việc độc lập của hai người dùng đều thấy ô đỗ đang trống ('available') và cùng thực hiện cập nhật thành công, dẫn đến tình trạng hai vé xe được cấp cho cùng một vị trí.")
    add_body_paragraph(doc, "Hệ thống Smart Parking System giải quyết triệt để vấn đề này bằng cách kết hợp cơ chế Khóa bi quan (Pessimistic Locking) cấp độ dòng dữ liệu của PostgreSQL thông qua mệnh đề SELECT FOR UPDATE bên trong một Transaction nguyên tử của SQLAlchemy:")

    code_lock = """# Trích đoạn mã nguồn xử lý đặt chỗ chống xung đột tại app/api/endpoints/bookings.py
with db.begin():
    # Thực thi khóa cấp độ bản ghi (Row-level Locking)
    slot = db.query(ParkingSlot).filter(
        ParkingSlot.id == booking_in.slot_id
    ).with_for_update().first()

    if not slot or slot.status != SlotStatus.AVAILABLE:
        raise HTTPException(
            status_code=400, 
            detail="Vị trí đỗ xe này vừa có khách hàng khác đặt giữ chỗ!"
        )

    # Chuyển trạng thái ô đỗ thành RESERVED an toàn tuyệt đối
    slot.status = SlotStatus.RESERVED
    
    # Khởi tạo bản ghi đặt chỗ Booking mới
    new_booking = Booking(
        booking_code=generate_unique_code(),
        user_id=current_user.id,
        slot_id=slot.id,
        license_plate=booking_in.license_plate,
        start_time=booking_in.start_time,
        status=BookingStatus.CONFIRMED
    )
    db.add(new_booking)
    # Transaction tự động commit và giải phóng khóa bản ghi"""
    add_code_snippet(doc, "Kỹ thuật SELECT FOR UPDATE ngăn chặn xung đột Double-Booking", code_lock)

    add_body_paragraph(doc, "Khi phiên làm việc đầu tiên thực hiện câu lệnh với `with_for_update()`, PostgreSQL sẽ đặt một Exclusive Lock lên dòng dữ liệu của ô đỗ đó. Phiên làm việc thứ hai dù gửi yêu cầu tới cùng lúc cũng bắt buộc phải xếp hàng chờ cho đến khi Transaction đầu tiên hoàn tất (Commit) và cập nhật trạng thái ô đỗ thành `RESERVED`. Lúc này, phiên thứ hai đọc lại dữ liệu sẽ lập tức phát hiện ô đỗ không còn khả dụng và trả về thông báo lỗi chính xác, ngăn chặn 100% tình trạng trùng lặp vé.")

    add_section_heading(doc, "2.6. Cơ chế xác thực, bảo mật và phân quyền vai trò (RBAC)")
    add_body_paragraph(doc, "Hệ thống bảo vệ dữ liệu người dùng và phân luồng nghiệp vụ dựa trên chuẩn công nghiệp hiện đại:")
    add_bullet_item(doc, "Sử dụng giải pháp băm mật khẩu một chiều có muối (Salted Hash) với thuật toán Bcrypt. Mật khẩu gốc của người dùng không bao giờ được lưu trữ dưới dạng văn bản thuần (Plaintext), đảm bảo an toàn ngay cả trong trường hợp cơ sở dữ liệu bị rò rỉ.", bold_prefix="Mã hóa mật khẩu Bcrypt: ")
    add_bullet_item(doc, "Sau khi người dùng đăng nhập thành công với email và mật khẩu hợp lệ, Backend sẽ sinh ra một chuỗi JWT có chữ ký điện tử HMAC-SHA256 bí mật (`SECRET_KEY`). Token chứa payload bao gồm định danh người dùng (`sub`), vai trò (`role`) và thời gian hết hạn (`exp`). Khách hàng gửi token này trong tiêu đề HTTP `Authorization: Bearer <token>` ở mọi yêu cầu API tiếp theo.", bold_prefix="Xác thực không trạng thái JWT (JSON Web Token): ")
    add_bullet_item(doc, "FastAPI Dependency Injection (`get_current_active_user`, `require_admin`, `require_staff`) đóng vai trò như các cổng gác bảo vệ API. Mọi yêu cầu truy cập trái quyền (ví dụ khách hàng thường gọi API tạo tài khoản nhân viên hoặc xem doanh thu) sẽ bị chặn đứng tại tầng Controller với mã lỗi HTTP 403 Forbidden.", bold_prefix="Phân quyền vai trò (Role-Based Access Control): ")
    add_bullet_item(doc, "Đặc biệt, hệ thống triển khai kiểm soát quyền địa hạt cho Nhân viên (Staff). Mỗi nhân viên khi được tạo tài khoản đều được gắn liền với một bãi đỗ cụ thể (`assigned_lot_id`). Nhân viên chỉ có thẩm quyền thao tác đóng mở barrier, check-in, check-out và xem dữ liệu trên bãi xe được phân công, không được can thiệp vào các bãi đỗ xe khác trong chuỗi.", bold_prefix="Kiểm soát phạm vi bãi làm việc của Staff: ")

