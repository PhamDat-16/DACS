import subprocess
import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

HTML_FILE = os.path.abspath(r"D:\smart-parking-system\Tuyen_tap_50_cau_hoi_bao_ve_do_an_Smart_Parking.html")
PDF_FILE = os.path.abspath(r"D:\smart-parking-system\Tuyen_tap_50_cau_hoi_bao_ve_do_an_Smart_Parking.pdf")
DOWNLOAD_PDF = os.path.abspath(r"C:\Users\LENOVO\Downloads\Tuyen_tap_50_cau_hoi_bao_ve_do_an_Smart_Parking.pdf")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

qa_data = [
    # PHẦN 1
    (
        "Phần I: Tổng Quan Đề Tài & Nghiệp Vụ Hệ Thống",
        [
            (
                "Đề tài của em giải quyết vấn đề gì trong thực tế? Tại sao cần xây dựng hệ thống này?",
                "Thưa cô, đề tài giải quyết vấn nạn ùn tắc giao thông tĩnh tại các đô thị lớn và trung tâm thương mại. Thực tế tài xế mất trung bình 15-25 phút đi lòng vòng tìm chỗ đỗ, gây lãng phí nhiên liệu, kẹt xe cục bộ và ức chế tâm lý. Đồng thời, ban quản lý bãi xe khó nắm bắt công suất thời gian thực và thất thoát doanh thu. Hệ thống Smart Parking System (SPS) của em giải quyết triệt để vấn đề này bằng cách số hóa toàn diện: cho phép khách tìm kiếm, đặt chỗ trước từ xa, dẫn đường ngắn nhất đến tận ô đỗ bằng thuật toán A*, và ứng dụng AI dự báo tỷ lệ lấp đầy trong 24 giờ tới."
            ),
            (
                "Điểm mới và nổi bật nhất của dự án so với các phần mềm quản lý bãi xe thông thường là gì?",
                "Điểm nổi bật nhất gồm 3 yếu tố cốt lõi: (1) Tích hợp thuật toán tìm đường A* trên lưới tọa độ 2D giúp dẫn đường thông minh né tránh cả vật cản tĩnh lẫn ô đã có xe đỗ; (2) Tích hợp AI Machine Learning dự báo tỷ lệ lấp đầy 24h giúp tài xế chủ động kế hoạch di chuyển; (3) Cơ chế kiểm soát đồng thời cấp database (SELECT FOR UPDATE) triệt tiêu hoàn toàn lỗi đặt trùng chỗ (Double-Booking) khi nhiều người cùng thao tác."
            ),
            (
                "Hệ thống của em gồm những đối tượng người dùng (roles) nào và phân quyền ra sao?",
                "Hệ thống phân quyền chặt chẽ thành 3 nhóm vai trò: (1) Customer (Khách hàng): Tìm kiếm bãi xe, đặt chỗ, xem bản đồ dẫn đường, mua vé tháng, theo dõi phiên đỗ và xem hóa đơn; (2) Staff (Nhân viên trực bãi): Trực barrier tại điểm đỗ được phân công, quét QR check-in/out, hỗ trợ xe vãng lai, xử lý sự cố; (3) Admin (Quản trị viên): Giám sát toàn hệ thống, cấu hình sơ đồ slot (bảo trì/vô hiệu hóa), phân quyền nhân viên theo bãi xe, duyệt vé tháng và xem báo cáo tài chính doanh thu."
            ),
            (
                "Trình bày luồng hoạt động chính của một khách hàng từ lúc tìm chỗ đến khi rời bãi?",
                "Quy trình gồm 5 bước: (1) Khách đăng nhập, tìm kiếm bãi xe gần nhất (như Đô Nghĩa, Vincom...); (2) Chọn ô đỗ mong muốn hoặc để hệ thống tự gợi ý, chọn thời lượng đỗ và bấm 'Đặt chỗ'; (3) Hệ thống sinh vé điện tử QR Code và vẽ lộ trình dẫn đường A* từ cổng vào; (4) Khi đến bãi, nhân viên quét mã QR tại barrier để check-in, barrier mở và slot chuyển sang màu Đỏ (Occupied); (5) Khi rời bãi, nhân viên check-out, hệ thống tính cước thực tế, mở barrier xuất bến, phát hành hóa đơn và tự động giải phóng slot về màu Xanh (Available)."
            ),
            (
                "Trình bày luồng nghiệp vụ của nhân viên trực bãi (Staff Portal)?",
                "Nhân viên đăng nhập vào cơ sở mình phụ trách (assigned_lot). Tại màn hình trực barrier: (1) Khi xe vào: Nhập biển số hoặc quét QR vé, hệ thống kiểm tra hợp lệ, gán slot và mở barrier; nếu xe đã có trong bãi cố tình quét lại thì hệ thống cảnh báo chặn; (2) Khi xe ra: Tìm kiếm biển số tại tab Check-out, hệ thống tự động tính thời gian đỗ thực tế và cước phí, nhân viên bấm xác nhận xuất bến, barrier mở và slot được giải phóng ngay lập tức."
            ),
            (
                "Khi khách đến gửi xe trực tiếp không qua đặt trước (xe vãng lai / Walk-in), hệ thống xử lý thế nào?",
                "Nhân viên sử dụng tính năng 'Khách vãng lai (Walk-in)': Chỉ cần nhập biển số xe và bấm 'Xác nhận vào bến'. Hệ thống tự động quét thuật toán tìm ô đỗ trống khả dụng gần cổng ra vào nhất (khoảng cách Manhattan nhỏ nhất), gán xe vào slot đó, tạo phiên đỗ mới (status = PARKING) và mở barrier mà không bắt buộc khách phải có tài khoản trước."
            ),
            (
                "Tính năng đặt chỗ trước (Booking) hoạt động như thế nào và sinh vé điện tử ra sao?",
                "Khi khách bấm đặt chỗ, API POST /api/bookings nhận slot_id, vehicle_id và thời gian đỗ. Hệ thống chạy transaction khóa dòng slot, chuyển trạng thái slot thành 'reserved' và tạo bản ghi Booking. Vé điện tử được sinh ngay dưới dạng mã Base64 QR Code chứa thông tin booking ID, biển số và thời gian, khách có thể lưu về máy hoặc mở trực tiếp trên app để nhân viên quét."
            ),
            (
                "Tính năng vé tháng cư dân (Monthly Pass) hoạt động như thế nào trong dự án?",
                "Khách hàng đăng ký gói vé tháng theo biển số xe tại cổng Customer. Yêu cầu sẽ xuất hiện tại bảng quản lý vé tháng của Admin với trạng thái Chờ duyệt (Pending). Sau khi Admin kiểm tra và duyệt, vé chuyển sang trạng thái Kích hoạt (Active), tài xế gửi xe không bị tính tiền theo giờ mà được miễn phí tự động trong suốt thời hạn hiệu lực của vé tháng."
            ),
            (
                "Cơ chế phân quyền nhân viên theo cơ sở công tác (Assigned Lot) giải quyết bài toán gì?",
                "Giải quyết bài toán quản lý chuỗi bãi xe đa chi nhánh. Admin khi tạo tài khoản nhân viên sẽ chọn bãi xe phân công (ví dụ: Bãi KĐT Đô Nghĩa, Vincom, Aeon Mall...). Khi nhân viên đó đăng nhập, hệ thống chỉ cho phép giám sát camera, điều khiển barrier và quản lý danh sách xe ra vào tại đúng cơ sở của mình, tránh việc nhân viên bãi này thao tác nhầm vào bãi khác."
            ),
            (
                "Tại sao hệ thống lại cần tính năng mô phỏng giờ ảo (Simulated Hour / Scrubber)?",
                "Vì trong môi trường kiểm thử và thuyết trình đồ án, ban giám khảo không thể chờ suốt 24 tiếng để thấy xe vào ca sáng, giờ cao điểm chiều hay ca đêm. Thanh trượt Simulated Hour cho phép mô phỏng tức thì hành vi bãi xe tại bất kỳ khung giờ nào trong ngày, giúp kiểm chứng trực quan ca trực của nhân viên và độ biến thiên của mô hình AI."
            )
        ]
    ),
    # PHẦN 2
    (
        "Phần II: Kiến Trúc Phần Mềm & Công Nghệ Backend",
        [
            (
                "Trình bày kiến trúc tổng thể (System Architecture) của dự án?",
                "Hệ thống xây dựng theo kiến trúc Client-Server hiện đại phân tầng rõ ràng: (1) Client Layer: Ứng dụng Web Single Page App (SPA) xây dựng bằng Vue 3, Tailwind CSS và GSAP Animation; (2) API & Business Layer: Xây dựng bằng Python FastAPI bất đồng bộ (Asynchronous), định tuyến RESTful API và quản lý kết nối WebSocket; (3) AI & Algorithmic Engine: Module A* Pathfinding và mô hình Machine Learning Random Forest; (4) Persistence Layer: Hệ quản trị CSDL quan hệ PostgreSQL kết nối qua SQLAlchemy ORM và Alembic."
            ),
            (
                "Tại sao em lại chọn FastAPI làm Backend framework mà không dùng Django hay Flask?",
                "FastAPI có 3 ưu điểm vượt trội cho dự án này: (1) Hiệu năng xử lý siêu cao (ngang ngửa Node.js và Go) nhờ nền tảng Starlette và Uvicorn ASGI; (2) Hỗ trợ Asynchronous (async/await) tự nhiên, rất phù hợp cho kết nối WebSocket thời gian thực; (3) Tự động kiểm thực dữ liệu (data validation) chặt chẽ bằng Pydantic và tự động sinh tài liệu Swagger UI chuẩn OpenAPI 3.0 mà không tốn công viết code thủ công."
            ),
            (
                "Cơ chế xác thực (Authentication) và bảo vệ API được thiết kế như thế nào?",
                "Hệ thống sử dụng cơ chế bảo mật Token-based Authentication chuẩn OAuth2 với JSON Web Token (JWT). Khi đăng nhập thành công, server cấp một chuỗi JWT Access Token đã được ký điện tử bằng thuật toán HS256 cùng khóa bí mật SECRET_KEY. Các request sau đó phải gửi kèm token trong HTTP Header `Authorization: Bearer <token>`. Tại backend, middleware `deps.get_current_user` sẽ giải mã và kiểm tra quyền truy cập."
            ),
            (
                "Cấu trúc của một JWT Token gồm những gì và tại sao dùng JWT thay vì Session Cookie?",
                "JWT gồm 3 phần phân tách bằng dấu chấm: Header (thuật toán mã hóa), Payload (chứa user_id, role, thời hạn hết hạn exp), và Signature (chữ ký số bí mật). Dùng JWT vì tính chất Stateless: server không cần tốn bộ nhớ RAM lưu session, dễ dàng mở rộng nhiều server (horizontal scaling), và hoàn toàn không bị tấn công CSRF như Cookie truyền thống."
            ),
            (
                "Mật khẩu người dùng được lưu trữ như thế nào trong cơ sở dữ liệu?",
                "Mật khẩu tuyệt đối không lưu dạng văn bản rõ (plaintext). Em sử dụng thư viện `passlib` với thuật toán băm Bcrypt kết hợp muối ngẫu nhiên (Salted Hash). Thuật toán này có tính năng làm chậm tính toán (cost factor / work factor), giúp chống lại các cuộc tấn công dò mật khẩu bằng Rainbow Table hoặc Brute-Force."
            ),
            (
                "WebSocket được sử dụng ở đâu trong dự án và cơ chế hoạt động ra sao?",
                "WebSocket được sử dụng để đồng bộ tức thời trạng thái bãi xe giữa các màn hình điều hành. Backend cài đặt lớp `ConnectionManager` quản lý danh sách các client đang kết nối. Bất cứ khi nào có sự kiện check-in, check-out hoặc cảm biến IoT thay đổi, server lập tức broadcast thông điệp JSON tới toàn bộ client để cập nhật màu sắc ô đỗ (Xanh/Đỏ/Vàng) mà trình duyệt không cần phải F5 hay gửi request thăm dò liên tục."
            ),
            (
                "Sự khác biệt giữa REST API và WebSocket trong hệ thống của em là gì?",
                "REST API hoạt động theo mô hình Request-Response một chiều qua giao thức HTTP không duy trì kết nối, phù hợp cho các thao tác CRUD dữ liệu tĩnh như đăng nhập, lấy danh sách bãi xe, đặt chỗ. Trong khi đó, WebSocket duy trì kết nối TCP song công (Full-duplex) liên tục, phù hợp cho luồng dữ liệu thời gian thực như phát sóng trạng thái ô đỗ và telemetry cảm biến."
            ),
            (
                "Em cấu hình CORS (Cross-Origin Resource Sharing) như thế nào trong FastAPI?",
                "Trong `main.py`, em tích hợp middleware `CORSMiddleware` cho phép các nguồn gốc (origins) từ cổng frontend như `http://localhost:3000`, `http://localhost:8000`, `127.0.0.1` được phép truy cập tài nguyên API, hỗ trợ đầy đủ các phương thức HTTP (GET, POST, PUT, DELETE) và gửi kèm thông tin định danh (credentials)."
            ),
            (
                "Cấu trúc thư mục của Backend được tổ chức theo chuẩn nào?",
                "Backend tổ chức theo kiến trúc module hóa phân tầng (Layered Architecture): `core/` (cấu hình, database, bảo mật), `models/` (các thực thể SQLAlchemy ORM), `schemas/` (Pydantic models kiểm thực dữ liệu), `routers/` (các API endpoints chia theo phân hệ auth, lots, bookings, sessions...), `services/` (nghiệp vụ logic), `pathfinding/` (thuật toán A*) và `ml_engine/` (huấn luyện và dự báo AI)."
            ),
            (
                "Hệ thống tích hợp tài liệu hóa API tự động như thế nào?",
                "FastAPI tự động sinh tài liệu chuẩn OpenAPI tại đường dẫn `/docs` (giao diện Swagger UI tương tác) và `/redoc` (giao diện ReDoc). Tại đây, mọi người có thể xem chi tiết từng endpoint, tham số đầu vào, cấu trúc phản hồi JSON và bấm nút 'Try it out' để test API trực tiếp ngay trên trình duyệt."
            )
        ]
    ),
    # PHẦN 3
    (
        "Phần III: Cơ Sở Dữ Liệu & Kiểm Soát Đồng Thời (Concurrency)",
        [
            (
                "Cơ sở dữ liệu của dự án sử dụng hệ quản trị nào? Tại sao lại chọn PostgreSQL?",
                "Dự án sử dụng PostgreSQL 18. Em chọn PostgreSQL vì đây là hệ quản trị CSDL quan hệ mã nguồn mở mạnh mẽ nhất hiện nay, hỗ trợ chuẩn ACID nghiêm ngặt, kiểu dữ liệu UUID gốc, các kiểu dữ liệu nâng cao (JSONB, Point), tốc độ truy vấn cao và đặc biệt là cơ chế khóa cấp dòng (Row-Level Locking) hoạt động cực kỳ tin cậy trong các bài toán giao dịch đồng thời."
            ),
            (
                "Trình bày các bảng chính trong CSDL và mối quan hệ giữa chúng (ERD)?",
                "CSDL gồm 6 bảng chính chuẩn 3NF: (1) `users`: Lưu tài khoản và vai trò; (2) `parking_lots`: Lưu thông tin bãi xe, tọa độ, kích thước lưới; (3) `parking_slots`: Lưu từng vị trí ô đỗ thuộc về 1 bãi xe (quan hệ 1-N với parking_lots); (4) `bookings`: Lưu thông tin đặt chỗ của user cho 1 slot; (5) `sessions`: Lưu phiên gửi xe thực tế khi check-in; (6) `occupancy_history`: Lưu lịch sử lấp đầy theo từng giờ phục vụ bài toán AI."
            ),
            (
                "Tại sao em sử dụng kiểu dữ liệu UUID làm khóa chính thay vì số nguyên Auto-increment (1, 2, 3...)?",
                "Sử dụng UUIDv4 có 3 lợi ích quan trọng: (1) Tính bảo mật: Kẻ xấu không thể đoán hoặc dò quét ID tuần tự (Insecure Direct Object References - IDOR) như ID số nguyên; (2) Tính phân tán: Tránh xung đột ID khi nhân rộng hệ thống ra nhiều cụm máy chủ hoặc đồng bộ nhiều chi nhánh; (3) Tương thích cao khi tích hợp dữ liệu với các hệ thống thanh toán và IoT bên thứ ba."
            ),
            (
                "Lỗi đặt chỗ trùng lặp (Double-Booking / Race Condition) là gì trong hệ thống bãi xe?",
                "Race Condition xảy ra khi có 2 hoặc nhiều khách hàng cùng bấm đặt 1 ô đỗ duy nhất tại cùng 1 tích tắc (mili-giây). Nếu chỉ dùng logic kiểm tra thông thường, cả 2 tiến trình đều thấy ô đỗ đang trống và cùng ghi nhận đặt chỗ thành công. Kết quả là 2 khách đến nơi nhưng chỉ có 1 chỗ đỗ, gây xung đột nghiêm trọng ngoài thực tế."
            ),
            (
                "Em giải quyết lỗi Double-Booking như thế nào ở tầng cơ sở dữ liệu?",
                "Em sử dụng kỹ thuật khóa bi quan (Pessimistic Locking) bằng câu lệnh `SELECT FOR UPDATE` của PostgreSQL trong SQLAlchemy transaction. Khi tiến trình A truy vấn ô đỗ, nó lập tức khóa dòng dữ liệu đó lại. Tiến trình B đến sau buộc phải chờ tiến trình A hoàn tất. Khi A đặt xong (đổi status thành 'reserved'), tiến trình B được mở khóa, thấy slot không còn trống nữa và lập tức bị từ chối với mã lỗi HTTP 409 Conflict."
            ),
            (
                "Tại sao lại dùng SELECT FOR UPDATE thay vì kiểm tra bằng câu lệnh if thông thường trong Python?",
                "Vì nếu chỉ dùng câu lệnh `if slot.status == 'available'` trong Python, giữa thời điểm đọc dữ liệu (Read) và thời điểm ghi dữ liệu (Write) luôn có một khoảng trễ thời gian (time gap). Trong môi trường đa luồng (multi-threading / multi-worker), cả 2 request đều nhảy qua câu lệnh `if` trước khi kịp cập nhật DB. Chỉ có khóa cấp dòng tại tầng Database mới đảm bảo tính nguyên tố (Atomicity) theo chuẩn ACID."
            ),
            (
                "Công cụ Alembic được dùng để làm gì trong dự án và lợi ích của nó?",
                "Alembic là công cụ Database Migration chuyên nghiệp đi kèm SQLAlchemy. Lợi ích là giúp quản lý lịch sử thay đổi cấu trúc bảng (schema versions) tương tự như Git. Khi thêm cột mới (như cột `assigned_lot`), ta chỉ cần chạy migration script, Alembic sẽ tự động cập nhật cấu trúc database trên môi trường thực tế mà không làm mất dữ liệu cũ."
            ),
            (
                "Trong bảng sessions, vòng đời trạng thái của một phiên gửi xe diễn ra như thế nào?",
                "Vòng đời gồm các trạng thái: Khi xe vào bến check-in thành công, session được tạo với trạng thái `PARKING` (xe đang đỗ trong bãi); khi xe ra bến và thanh toán cước phí đầy đủ, session chuyển sang `COMPLETED` (phiên hoàn tất và ghi nhận check_out_time, total_fee); nếu phát sinh hủy phiên thì chuyển thành `CANCELLED`."
            )
        ]
    ),
    # PHẦN 4
    (
        "Phần IV: Thuật Toán Dẫn Đường Ngắn Nhất A* (Pathfinding)",
        [
            (
                "Thuật toán A* là gì? Tại sao em chọn thuật toán A* cho bài toán dẫn đường bãi xe?",
                "A* (A-Star) là giải thuật tìm đường thông minh trên đồ thị/lưới dựa trên kỹ thuật Heuristic Search. Em chọn A* vì bãi xe có thể mô hình hóa thành lưới 2D với các lối đi và chướng ngại vật cố định. A* luôn đảm bảo tìm ra đường đi ngắn nhất (Optimal) với tốc độ nhanh hơn nhiều so với duyệt toàn bộ không gian nhờ hàm ước lượng hướng đích, thời gian phản hồi thực tế của thuật toán trên hệ thống đạt dưới 5ms."
            ),
            (
                "Công thức hàm đánh giá của thuật toán A* là gì? Ý nghĩa của từng thành phần?",
                "Công thức đánh giá tại mỗi nút n là: f(n) = g(n) + h(n). Trong đó: g(n) là chi phí thực tế đã đi từ điểm xuất phát (cổng vào) đến nút hiện tại n; h(n) là hàm Heuristic ước lượng chi phí còn lại từ nút n đến đích (ô đỗ được chọn); f(n) là tổng chi phí ước lượng nhỏ nhất để đi qua nút n đến đích. Thuật toán luôn ưu tiên mở rộng nút có f(n) nhỏ nhất thông qua hàng đợi ưu tiên (Priority Queue)."
            ),
            (
                "Em chọn hàm Heuristic h(n) nào trong bài toán này? Tại sao chọn Manhattan thay vì Euclidean?",
                "Em sử dụng hàm khoảng cách Manhattan: h(n) = |x_n - x_target| + |y_n - y_target|. Em chọn Manhattan vì trong bãi đỗ xe trong nhà, các luồng giao thông được chia thành các hàng và cột vuông góc (xe chỉ di chuyển 4 hướng: tiến, lùi, rẽ trái, rẽ phải theo góc 90 độ), không thể chạy chéo cắt qua các góc cột bê tông. Do đó Manhattan phản ánh chính xác 100% hình học thực tế của bãi xe."
            ),
            (
                "Em mô hình hóa không gian bãi đỗ xe thành cấu trúc dữ liệu gì để A* xử lý?",
                "Em mô hình hóa không gian thành ma trận lưới 2D (Grid Matrix kích thước W x H) trong `grid.py`. Mỗi ô tọa độ (x, y) là một nút: ô giá trị 0 là đường đi thông thoáng (walkable/drivable), ô giá trị 1 là vật cản tĩnh (tường, cột trụ), ô giá trị 2 là ô đỗ đang có xe hoặc đã đặt chỗ (vật cản động)."
            ),
            (
                "Thuật toán A* của em xử lý vật cản tĩnh và vật cản động như thế nào?",
                "Vật cản tĩnh (cột, tường) được nạp cố định vào bản đồ. Vật cản động (các ô slot đang đỗ hoặc đã đặt chỗ) được hệ thống cập nhật tự động vào ma trận cấm đi. Riêng duy nhất ô slot đích mà khách đã chọn sẽ được tạm thời mở khóa để A* có thể dẫn xe tiến vào đúng vị trí đỗ. Nếu một lối đi bị chặn hoàn toàn, thuật toán tự động rẽ sang luồng đường khác để tiếp cận ô đỗ."
            ),
            (
                "So sánh thuật toán A* với thuật toán Dijkstra và BFS/DFS?",
                "BFS chỉ phù hợp đồ thị không trọng số và duyệt loang rộng lãng phí; Dijkstra tìm đường ngắn nhất nhưng duyệt mù theo mọi hướng (h(n) = 0) nên tốn tài nguyên; còn A* kết hợp điểm mạnh của Dijkstra (độ chính xác g(n)) và tham lam Greedy Best-First Search (định hướng đích h(n)). Nhờ đó A* chỉ duyệt các nút hướng về phía đích, tiết kiệm bộ nhớ và nhanh gấp nhiều lần."
            ),
            (
                "Độ phức tạp thời gian và không gian của thuật toán A* trong dự án là bao nhiêu?",
                "Độ phức tạp thời gian trong trường hợp xấu nhất là O(b^d) với b là hệ số rẽ nhánh (branching factor ~ 4 hướng) và d là độ dài đường đi. Tuy nhiên nhờ hàm Heuristic Manhattan chấp nhận được (admissible), không gian tìm kiếm được thu hẹp tối đa. Với lưới bãi xe thông thường (50x50), thuật toán chỉ mất trung bình 2 đến 5 mili-giây và tiêu tốn dưới 1MB RAM."
            ),
            (
                "Làm sao để hiển thị xe ảo lăn bánh bám theo lộ trình đường đi A* trên web?",
                "API trả về danh sách các điểm tọa độ waypoints [(0,0), (0,1), (1,1)...]. Ở frontend, em sử dụng thư viện hoạt họa GSAP 3 (GreenSock Animation Platform) để diễn hoạt chiếc xe ảo di chuyển mượt mà qua từng tọa độ. Đồng thời dựa trên vector hướng di chuyển (dx, dy), code tự động tính góc xoay để đầu xe rẽ 90 độ theo đúng góc cua thực tế."
            )
        ]
    ),
    # PHẦN 5
    (
        "Phần V: Trí Tuệ Nhân Tạo & Học Máy (Machine Learning)",
        [
            (
                "Bài toán Machine Learning trong dự án của em là bài toán gì?",
                "Đây là bài toán Hồi quy chuỗi thời gian (Time-series Regression) nhằm dự báo tỷ lệ lấp đầy (Occupancy Rate) của bãi đỗ xe theo từng khung giờ trong ngày, nhận đầu vào là các yếu tố thời gian và trả về một giá trị thực liên tục từ 0.0 đến 1.0 (tương ứng 0% đến 100% công suất bãi xe)."
            ),
            (
                "Dataset dùng để huấn luyện mô hình được lấy từ đâu?",
                "Dataset được tạo bởi mô-đun sinh dữ liệu mô phỏng có quy luật thực tế (`data_generator.py`). Lý do không lấy dataset công khai nước ngoài vì giao thông Việt Nam có đặc thù riêng và các bãi xe thương mại không chia sẻ dữ liệu nội bộ. Mô-đun của em mô phỏng chính xác các chu kỳ cao điểm sáng/chiều, ngày thường, cuối tuần, ngày lễ và bổ sung nhiễu Gaussian để mô hình học được quy luật thực tế. Đồng thời CSDL đã có sẵn cơ chế ghi nhận dữ liệu thật vào bảng `occupancy_history` để tái huấn luyện sau này."
            ),
            (
                "Dataset của em có bao nhiêu bản ghi và gồm những đặc trưng (features) nào?",
                "Dataset gồm 4.320 bản ghi (tương ứng 180 ngày lịch sử, mỗi ngày 24 bản ghi đại diện cho 24 giờ). Gồm 4 đặc trưng đầu vào (X): `hour_of_day` (0-23h), `day_of_week` (0-6), `is_weekend` (0 hoặc 1), `is_holiday` (0 hoặc 1); và 1 biến mục tiêu đầu ra (y): `occupancy_rate` (tỷ lệ lấp đầy từ 0.0 đến 1.0)."
            ),
            (
                "Quy luật mô phỏng dữ liệu (Data Generation Rules) dựa trên cơ sở thực tế nào?",
                "Quy luật dựa trên thói quen giao thông đô thị: (1) Đêm muộn (0h-5h): tỷ lệ lấp đầy thấp nhất ~10%; (2) Giờ cao điểm sáng (7h-9h): tăng vọt lên 80-90% do người dân đi làm; (3) Giữa trưa (11h-14h): giữ mức ổn định 55%; (4) Cao điểm chiều (17h-19h): đạt đỉnh 85-95% do giờ tan tầm; (5) Cuối tuần & lễ: đường cong phẳng hơn, không có đỉnh nhọn đi làm mà dàn đều ~50%; (6) Nhiễu phân phối chuẩn Gaussian (độ lệch chuẩn 0.06) mô phỏng các biến động ngẫu nhiên."
            ),
            (
                "Tại sao em lại chọn mô hình Random Forest Regressor mà không dùng Linear Regression hay LSTM?",
                "Mô hình Linear Regression quá đơn giản, không học được các mối quan hệ phi tuyến tính phức tạp (như đỉnh nhọn giờ cao điểm); còn LSTM hay mạng nơ-ron sâu đòi hỏi dữ liệu khổng lồ và chi phí tính toán phần cứng cao. Random Forest Regressor (200 cây quyết định, max_depth 10) là giải pháp tối ưu nhất: bắt trọn các quy luật phi tuyến, chống hiện tượng Overfitting (nhờ kỹ thuật Bagging), huấn luyện siêu nhanh và kích thước file mô hình chỉ vài Megabyte."
            ),
            (
                "Em đánh giá độ chính xác của mô hình bằng những chỉ số nào? Kết quả đạt được ra sao?",
                "Em chia tập dữ liệu 80% Train và 20% Test, đánh giá bằng 2 chỉ số chuẩn: (1) Sai số tuyệt đối trung bình MAE (Mean Absolute Error) đạt mức rất thấp: 0.058 (khoảng 5.8% dung lượng bãi xe); (2) Căn bậc hai sai số toàn phương trung bình RMSE đạt 0.076. Điều này chứng minh mô hình dự báo rất chuẩn xác xu hướng lấp đầy của bãi xe."
            ),
            (
                "Mô hình AI sau khi huấn luyện được triển khai (deployment) như thế nào trên FastAPI?",
                "Mô hình sau khi huấn luyện được serialize và đóng gói thành file nhị phân `occupancy_model.joblib`. Tại backend, file được nạp vào bộ nhớ RAM theo mẫu thiết kế Singleton (chỉ nạp 1 lần duy nhất khi server khởi động). Khi client gọi API GET `/api/predict`, server gọi hàm `model.predict()` tức thời mà không phải huấn luyện lại, thời gian trả kết quả dưới 2 mili-giây."
            ),
            (
                "Biểu đồ dự báo công suất 24h trên giao diện web hoạt động như thế nào?",
                "Frontend gọi API GET `/api/predict/24h` truyền vào ngày cần xem. Server trả về danh sách 24 điểm dự báo cho 24 giờ. Giao diện hiển thị biểu đồ đường SVG mượt mà kèm thanh trượt tương tác (scrubber). Khi người dùng kéo thanh trượt đến giờ nào, hệ thống hiển thị chính xác tỷ lệ lấp đầy dự kiến tại giờ đó, kèm khuyến nghị nên đến đỗ hay nên chọn bãi khác."
            )
        ]
    ),
    # PHẦN 6
    (
        "Phần VI: Kiểm Thử, An Toàn, Vận Hành & Hướng Phát Triển",
        [
            (
                "Em đã kiểm thử hệ thống bằng những công cụ và phương pháp nào?",
                "Hệ thống được kiểm thử toàn diện qua 3 tầng: (1) Unit Testing: Dùng thư viện Pytest với 11 test cases kiểm tra độc lập giải thuật A* (6 cases) và pipeline Machine Learning (5 cases); (2) Concurrency Testing: Dùng script mô phỏng đa luồng Python giả lập 2 tiến trình cùng đặt 1 chỗ tại 1 mili-giây để kiểm chứng khóa SELECT FOR UPDATE; (3) E2E Automation Testing: Dùng Playwright tự động hóa trình duyệt Microsoft Edge để kiểm thử luồng liên hoàn từ đăng nhập, check-in, check-out đến phát hành hóa đơn."
            ),
            (
                "Trình bày chi tiết kịch bản kiểm thử đa luồng (Concurrency Test) chống Race Condition?",
                "Kịch bản sử dụng `concurrent.futures.ThreadPoolExecutor` khởi tạo 2 luồng gửi đồng thời 2 request HTTP POST đặt cùng 1 slot ID. Kết quả kiểm thử: Đúng 1 tiến trình được cấp quyền và nhận mã HTTP 201 Created; tiến trình còn lại bị khóa database chặn lại và nhận mã HTTP 409 Conflict với thông báo 'Slot này vừa được người khác đặt'. Điều này chứng minh hệ thống an toàn 100% trước lỗi Race Condition."
            ),
            (
                "Khi có sự cố mất mạng hoặc mất điện, hệ thống xử lý dữ liệu và phiên đỗ xe như thế nào?",
                "Nhờ cơ chế lưu trữ bền vững trên PostgreSQL theo chuẩn ACID: Tất cả giao dịch đã commit (check-in, check-out) đều được ghi vào Write-Ahead Logging (WAL) trên ổ cứng, đảm bảo không bao giờ mất dữ liệu. Khi có điện lại, hệ thống tự động phục hồi trạng thái phiên. Ở phía client, giao diện web có tích hợp Standalone Mock Engine cho phép nhân viên tạm thời ghi nhận offline và đồng bộ lại khi có mạng."
            ),
            (
                "Nếu bãi đỗ xe mở rộng lên hàng nghìn slot hoặc mở rộng nhiều cơ sở, hệ thống có mở rộng được không (Scalability)?",
                "Hệ thống hoàn toàn đáp ứng tốt nhờ thiết kế Stateless của Backend FastAPI và kiến trúc REST/JWT. Để mở rộng: (1) Backend có thể triển khai nhiều instance sau bộ cân bằng tải Nginx (Load Balancer); (2) Database PostgreSQL có thể cấu hình Connection Pooling (PgBouncer) và phân cụm Read-Replica; (3) Thuật toán A* có thể chia nhỏ bãi xe thành các khu vực (Sub-grids/Hierarchical A*) để giảm số nút tính toán."
            ),
            (
                "Trong tương lai khi triển khai thực tế, dự án có thể tích hợp phần cứng như thế nào?",
                "Hệ thống thiết kế kiến trúc mở sẵn sàng tích hợp: (1) Camera AI nhận diện biển số (ANPR/YOLOv8) tại cổng barrier để tự động điền biển số xe thay vì nhập tay; (2) Cảm biến siêu âm hoặc camera gắn trần tại từng ô đỗ kết nối qua giao thức MQTT/WebSocket để tự động đổi màu slot khi có xe đỗ vào; (3) Mạch vi điều khiển ESP32/Raspberry Pi kích hoạt rơ-le nâng hạ thanh chắn barrier tự động."
            ),
            (
                "Nếu có thêm thời gian phát triển, em sẽ nâng cấp thêm những tính năng gì cho dự án?",
                "Em sẽ phát triển thêm 3 tính năng nâng cao: (1) Tích hợp cổng thanh toán trực tuyến tự động qua mã VietQR động / MoMo / VNPay; (2) Phát triển ứng dụng di động hoàn chỉnh bằng Flutter cho tài xế kèm định vị GPS ngoài trời chỉ đường từ vị trí hiện tại đến cổng bãi xe; (3) Áp dụng thuật toán định giá động (Dynamic Pricing) tự động điều chỉnh giá gửi xe theo cung cầu giờ cao điểm và dự báo AI."
            )
        ]
    )
]

# XÂY DỰNG HTML
html_sections = []
question_count = 0

for part_title, qa_list in qa_data:
    part_html = f"""
    <div class="part-header">{part_title}</div>
    """
    for q, a in qa_list:
        question_count += 1
        part_html += f"""
        <div class="qa-item">
            <div class="q-title"><span class="q-badge">Câu {question_count:02d}</span> {q}</div>
            <div class="a-content"><strong>Trả lời:</strong> {a}</div>
        </div>
        """
    html_sections.append(part_html)

full_sections_html = "\n".join(html_sections)

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Tuyển Tập 50 Câu Hỏi & Câu Trả Lời Bảo Vệ Đồ Án - Smart Parking System</title>
    <style>
        @page {{
            size: A4;
            margin: 14mm 16mm 14mm 16mm;
            @bottom-right {{
                content: "Trang " counter(page);
                font-size: 8pt;
                color: #64748b;
            }}
        }}
        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Times New Roman', Roboto, Arial, sans-serif;
            color: #0f172a;
            line-height: 1.42;
            font-size: 9.6pt;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }}
        
        .header {{
            border-bottom: 2.5px solid #1e3a8a;
            padding-bottom: 8px;
            margin-bottom: 12px;
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
            margin-bottom: 3px;
        }}
        .doc-title {{
            font-size: 15.5pt;
            font-weight: 900;
            color: #1e3a8a;
            margin: 0;
            letter-spacing: -0.2px;
            text-transform: uppercase;
        }}
        .doc-subtitle {{
            font-size: 10pt;
            color: #0f172a;
            margin-top: 3px;
            font-weight: 700;
        }}
        .meta-box {{
            text-align: right;
            font-size: 8.5pt;
            color: #334155;
            line-height: 1.4;
        }}
        .badge {{
            display: inline-block;
            padding: 2px 7px;
            border-radius: 9999px;
            font-size: 8pt;
            font-weight: 800;
            text-transform: uppercase;
            background-color: #dbeafe;
            color: #1e40af;
            border: 1px solid #93c5fd;
        }}

        .intro-box {{
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-left: 4px solid #1e3a8a;
            border-radius: 4px;
            padding: 8px 12px;
            margin-bottom: 14px;
            font-size: 8.8pt;
            color: #334155;
            line-height: 1.4;
        }}

        .part-header {{
            background: #1e3a8a;
            color: #ffffff;
            font-size: 10.5pt;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            padding: 5px 10px;
            border-radius: 4px;
            margin-top: 14px;
            margin-bottom: 8px;
            page-break-after: avoid;
        }}

        .qa-item {{
            margin-bottom: 9px;
            padding-bottom: 7px;
            border-bottom: 1px dashed #e2e8f0;
            page-break-inside: avoid;
        }}
        .q-title {{
            font-weight: 800;
            font-size: 9.8pt;
            color: #1e3a8a;
            margin-bottom: 3px;
            display: flex;
            align-items: baseline;
            gap: 6px;
        }}
        .q-badge {{
            background: #e0e7ff;
            color: #3730a3;
            font-size: 7.8pt;
            font-weight: 800;
            padding: 1.5px 5px;
            border-radius: 3px;
            border: 1px solid #c7d2fe;
            white-space: nowrap;
        }}
        .a-content {{
            font-size: 9.2pt;
            color: #1e293b;
            text-align: justify;
            padding-left: 2px;
        }}
        .a-content strong {{
            color: #0f172a;
        }}
    </style>
</head>
<body>

    <div class="header">
        <div>
            <div class="univ-title">TRƯỜNG ĐẠI HỌC PHENIKAA – KHOA CÔNG NGHỆ THÔNG TIN</div>
            <div class="doc-title">BỘ 50 CÂU HỎI & CÂU TRẢ LỜI BẢO VỆ ĐỒ ÁN</div>
            <div class="doc-subtitle">HỆ THỐNG QUẢN LÝ VÀ DẪN ĐƯỜNG BÃI ĐỖ XE THÔNG MINH (SMART PARKING SYSTEM - SPS)</div>
        </div>
        <div class="meta-box">
            <div><strong>Học phần:</strong> CSE702131-1-1-26(N01)</div>
            <div><strong>Sinh viên:</strong> Phạm Văn Đạt (MSV: 23017150)</div>
            <div><strong>Quy mô:</strong> <span class="badge">50 CÂU HỎI TRỌNG TÂM</span></div>
        </div>
    </div>

    <div class="intro-box">
        <strong>Tài liệu ôn tập &amp; phản biện đồ án:</strong> Tuyển tập 50 câu hỏi kèm đáp án chuẩn xác về mặt kỹ thuật, sát với mã nguồn thực tế của dự án. Bao quát toàn diện 6 chuyên đề then chốt: Nghiệp vụ bãi xe, Kiến trúc FastAPI &amp; WebSocket, Cơ sở dữ liệu PostgreSQL &amp; Chống Double-booking, Thuật toán tìm đường ngắn nhất A*, Mô hình Machine Learning Random Forest dự báo 24h, và Quy trình Kiểm thử tự động (Unit, Concurrency, E2E).
    </div>

    {full_sections_html}

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

