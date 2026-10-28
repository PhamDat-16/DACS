# Smart Parking System — Backend API Specification & Documentation

> **Máy chủ Backend API hiệu năng cao cho Hệ thống Quản lý Bãi đỗ xe Thông minh** xây dựng trên nền tảng **FastAPI**, **SQLAlchemy ORM**, **PostgreSQL**, tích hợp Thuật toán tìm đường tối ưu **A\***, Mô hình Học máy **Random Forest Regressor** dự báo tỷ lệ lấp đầy, cơ chế thanh toán động **VietQR**, quản lý **Thuê bao Vé tháng VIP** và kiểm soát vào/ra qua barrier thời gian thực.

---

## 📌 MỤC LỤC

1. [Yêu Cầu Môi Trường](#1-yêu-cầu-môi-trường)
2. [Cài Đặt & Khởi Chạy](#2-cài-đặt--khởi-chạy)
3. [Kiến Trúc Tổng Thể Backend](#3-kiến-trúc-tổng-thể-backend)
4. [Các Giai Đoạn Phát Triển (Phase 1 — Phase 5)](#4-các-giai-đoạn-phát-triển)
   - [Phase 1: Database Schema & Authentication JWT](#phase-1-database-schema--authentication-jwt)
   - [Phase 2: Booking Engine & Chống Double-Booking](#phase-2-booking-engine--chống-double-booking-select-for-update)
   - [Phase 3: Thuật Toán Tìm Đường A\*](#phase-3-thuật-toán-tìm-đường-a-pathfinding)
   - [Phase 4: Mô Hình Học Máy Dự Báo Lấp Đầy (Random Forest)](#phase-4-mô-hình-học-máy-dự-báo-lấp-đầy)
   - [Phase 5: Kiểm Soát Cổng (Check-in/Check-out), Vé Tháng & VietQR](#phase-5-kiểm-soát-cổng-vé-tháng-vip--vietqr)
5. [Danh Sách API Endpoints (Swagger RESTful)](#5-danh-sách-api-endpoints)
6. [Bộ Kiểm Thử Tự Động (Unit & Integration Tests)](#6-bộ-kiểm-thử-tự-động)

---

## 1. Yêu cầu môi trường

- **Python**: 3.11+ (khuyến nghị 3.11 hoặc 3.12)
- **PostgreSQL**: 14+ (khuyến nghị PostgreSQL 15/16)
- **Hệ điều hành**: Windows 10/11, macOS hoặc Linux / Ubuntu

---

## 2. Cài đặt & Khởi chạy

### Bước 1: Tạo cơ sở dữ liệu PostgreSQL
Trong terminal `psql` hoặc công cụ pgAdmin:
```sql
CREATE DATABASE parking_system;
```

### Bước 2: Kích hoạt môi trường ảo & Cài đặt thư viện
Tại thư mục `backend/`:
```powershell
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Bước 3: Cấu hình biến môi trường (`.env`)
Tạo tệp `.env` từ `.env.example`:
```env
DATABASE_URL=postgresql://postgres:123456@localhost:5432/parking_system
SECRET_KEY=smart_parking_super_secret_jwt_key_2026_phenikaa
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ALGORITHM=HS256
```

### Bước 4: Thực thi Database Migration (Alembic)
```powershell
alembic upgrade head
```

### Bước 5: Khởi chạy máy chủ API
```powershell
uvicorn app.main:app --reload --port 8000
```
- **Tài liệu API tương tác (Swagger UI)**: `http://127.0.0.1:8000/docs`
- **ReDoc Technical Specification**: `http://127.0.0.1:8000/redoc`

---

## 3. Kiến trúc tổng thể Backend

Backend được quy hoạch theo mô hình phân tầng chuẩn mực (Layered Architecture):

```
backend/
├── app/
│   ├── main.py                  # Khởi tạo FastAPI, CORS, gắn Router & Mount Static SPA
│   ├── core/                    # Cấu hình lõi hệ thống
│   │   ├── config.py            # Đọc tệp .env bằng pydantic-settings
│   │   ├── database.py          # SQLAlchemy Engine, SessionLocal, Base ORM
│   │   ├── security.py          # Bcrypt hashing mật khẩu, encode/decode JWT
│   │   └── deps.py              # Dependencies: get_current_user, require_role
│   ├── models/                  # SQLAlchemy ORM Models (7 thực thể)
│   │   ├── user.py              # Model users (Customer, Staff, Admin)
│   │   ├── parking_lot.py       # Model parking_lots (Kích thước lưới, đơn giá)
│   │   ├── parking_slot.py      # Model parking_slots (Tọa độ, trạng thái)
│   │   ├── booking.py           # Model bookings (Vé đặt trước, QR Code)
│   │   ├── session.py           # Model sessions (Phiên gửi xe qua cổng)
│   │   └── occupancy_history.py # Model occupancy_history (Lịch sử tỷ lệ lấp đầy)
│   ├── schemas/                 # Pydantic v2 Schemas (Validation dữ liệu vào/ra)
│   ├── routers/                 # API Controllers
│   │   ├── auth.py              # Xác thực đăng nhập, đăng ký
│   │   ├── users.py             # Thông tin cá nhân, danh sách nhân viên
│   │   ├── lots.py              # Quản lý bãi xe, ô đỗ, tìm đường A*
│   │   ├── bookings.py          # Quản lý đơn đặt chỗ, sinh mã QR E-Ticket
│   │   ├── sessions.py          # Check-in, Check-out, tính cước xuất bến
│   │   ├── predict.py           # Dự báo tỷ lệ lấp đầy bằng Random Forest
│   │   └── analytics.py         # Thống kê doanh thu, quản lý Vé tháng VIP
│   ├── services/                # Business Logic Services
│   │   ├── booking_service.py   # Xử lý đặt chỗ với SELECT FOR UPDATE
│   │   ├── session_service.py   # Check-in, Check-out, đối soát vé tháng
│   │   └── qr_service.py        # Sinh ảnh QR Code dạng Base64
│   ├── pathfinding/             # Thuật toán tìm đường
│   │   ├── grid.py              # Ma trận không gian bãi đỗ 2D
│   │   └── astar.py             # Thuật toán A* thuần túy (Heuristic Manhattan)
│   └── ml_engine/               # Machine Learning Engine
│       ├── data_generator.py    # Sinh tập dữ liệu 4.320 mẫu chuẩn thực tế
│       ├── train.py             # Huấn luyện Random Forest Regressor (200 trees)
│       ├── predict.py           # Suy luận dự báo tỷ lệ lấp đầy (Singleton)
│       └── models/              # Nơi lưu file nhị phân occupancy_model.joblib
├── tests/                       # 24 bài kiểm thử tự động (Pytest)
├── requirements.txt             # Danh mục thư viện phụ thuộc
└── alembic.ini                  # Cấu hình Alembic migration
```

---

## 4. Các giai đoạn phát triển

### Phase 1: Database Schema & Authentication JWT
- Thiết kế cơ sở dữ liệu quan hệ chuẩn 3NF: `users`, `parking_lots`, `parking_slots`, `bookings`, `sessions`, `occupancy_history`.
- Xác thực 3 vai trò: `customer`, `staff`, `admin`.
- Mật khẩu mã hóa 1 chiều bằng thư viện `bcrypt`. Xác thực người dùng qua `Bearer JWT Token` với hạn dùng cấu hình linh hoạt.

### Phase 2: Booking Engine & Chống Double-Booking (`SELECT FOR UPDATE`)
- Khách hàng chọn vị trí ô đỗ trên lưới và khoảng thời gian cần gửi xe.
- Sử dụng cơ chế khóa mức dòng cơ sở dữ liệu:
  ```python
  slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).with_for_update().first()
  ```
- **Triệt tiêu hoàn toàn Race Condition**: Nếu 2 khách hàng bấm đặt cùng 1 ô tại cùng một thời điểm, chỉ đúng 1 giao dịch thành công (HTTP 201), giao dịch còn lại lập tức nhận lỗi xung đột (HTTP 409 Conflict).
- Tự động sinh mã `Booking Token` và ảnh **QR Code Base64** đóng vai trò là Vé xe điện tử (E-Ticket).

### Phase 3: Thuật toán tìm đường A\* (Pathfinding)
- Biểu diễn mặt bằng bãi xe thành đồ thị lưới 2D (`Grid`).
- Thuật toán **A\*** sử dụng hàm ước lượng khoảng cách Manhattan:
  $$f(n) = g(n) + h(n) = g(n) + (|x_n - x_{goal}| + |y_n - y_{goal}|)$$
- Tự động tìm đường đi ngắn nhất từ Cổng vào `(0, 0)` tới vị trí ô đỗ, tự động né chướng ngại vật và các xe đang đỗ.
- Tách biệt module `pathfinding/` độc lập để tăng tốc độ thực thi và dễ dàng unit test không cần kết nối Database.

### Phase 4: Mô hình Học máy dự báo lấp đầy
- Huấn luyện mô hình **Random Forest Regressor** (200 Decision Trees, `max_depth=10`, `random_state=42`) trên tập dữ liệu chuỗi thời gian 4.320 mẫu (180 ngày $\times$ 24 giờ).
- Kết quả đánh giá thực nghiệm:
  - **MAE**: $0.0580$ (sai số chỉ 5.8%)
  - **MSE**: $0.0062$
  - **RMSE**: $0.0787$
  - **$R^2$ Score**: $0.9120$ (giải thích 91.2% sự biến thiên)
  - **Thời gian suy luận (Inference Time)**: $3.8\text{ ms}$ ($< 5\text{ ms}$).
- Mô hình được đóng gói thành tệp nhị phân nén `occupancy_model.joblib` và tải vào RAM theo mẫu thiết kế **Singleton** khi máy chủ FastAPI khởi động.

### Phase 5: Kiểm soát cổng, Vé tháng VIP & VietQR
1. **Kiểm soát cổng Check-in**:
   - Quét mã QR đặt chỗ hoặc đối chiếu biển số xe.
   - Kiểm tra đặc quyền **Thuê bao Vé tháng VIP**: Nếu xe có vé tháng hợp lệ tại đúng bãi đỗ $\rightarrow$ Cho phép vào bãi với cước phí **0 VNĐ**.
   - Kiểm tra trùng lặp: Ngăn chặn phương tiện đang có phiên đỗ dở dang tiếp tục check-in thêm.
2. **Kiểm soát xuất bến Check-out**:
   - **Xử lý khách ra sớm hơn lịch đặt**: Tự động tính cước theo thời gian đỗ thực tế (30.000 VNĐ/h, tối thiểu 1 giờ), giải phóng ô đỗ lập tức sang màu xanh `TRỐNG / Sẵn sàng`.
   - **Thanh toán VietQR**: Tự động sinh mã VietQR động chuẩn Napas247 hiển thị số tiền chính xác và biển số xe.
   - Nhân viên bấm "Xác nhận đã thanh toán" $\rightarrow$ Mở Barie, kết thúc phiên đỗ và ghi nhận sổ cái doanh thu tức thì.

---

## 5. Danh sách API Endpoints

| Nhóm chức năng | Phương thức | Endpoint | Mô tả |
| :--- | :---: | :--- | :--- |
| **Authentication** | `POST` | `/api/auth/register` | Đăng ký tài khoản người dùng mới |
| | `POST` | `/api/auth/login` | Đăng nhập hệ thống, trả về JWT Access Token |
| **Users** | `GET` | `/api/users/me` | Lấy thông tin tài khoản hiện hành |
| | `GET` | `/api/users/staff` | Lấy danh sách nhân viên bảo vệ vận hành |
| | `POST` | `/api/users/staff` | Admin cấp tài khoản nhân viên mới |
| **Parking Lots** | `GET` | `/api/lots` | Lấy danh sách toàn bộ bãi đỗ xe |
| | `GET` | `/api/lots/{lot_id}` | Lấy chi tiết bãi đỗ xe kèm danh sách ô đỗ |
| | `GET` | `/api/lots/{lot_id}/navigate` | Tìm đường đi ngắn nhất A\* từ Cổng vào tới ô đỗ |
| **Bookings** | `POST` | `/api/bookings` | Đặt chỗ trước (Khóa dòng `SELECT FOR UPDATE`, trả ảnh QR) |
| | `GET` | `/api/bookings` | Lấy danh sách vé đặt chỗ (Customer/Staff/Admin) |
| **Sessions** | `POST` | `/api/sessions/check-in` | Đón xe qua cổng, kích hoạt phiên đỗ (QR / Biển số) |
| | `POST` | `/api/sessions/check-out` | Trả xe xuất bến, tính tiền thực tế, sinh VietQR |
| | `GET` | `/api/sessions` | Lấy danh sách các phiên gửi xe thời gian thực |
| **AI Predictions** | `GET` | `/api/predict-occupancy` | Dự báo tỷ lệ lấp đầy theo 1 giờ cụ thể |
| | `GET` | `/api/predict-occupancy/day` | Dự báo tỷ lệ lấp đầy toàn bộ 24 giờ trong ngày |
| **Analytics & Passes** | `GET` | `/api/analytics/revenue` | Báo cáo doanh thu theo ngày, tháng, tỷ trọng |
| | `GET` | `/api/analytics/monthly-passes` | Lấy danh sách thuê bao vé tháng VIP |
| | `POST` | `/api/analytics/monthly-passes` | Đăng ký vé tháng VIP mới (Trạng thái `pending_payment`) |
| | `POST` | `/api/analytics/monthly-passes/{id}/pay` | Thanh toán kích hoạt vé tháng (Bắt đầu tính thời hạn) |

---

## 6. Bộ kiểm thử tự động

Hệ thống tích hợp bộ kiểm thử tự động toàn diện bằng `pytest` với 24 test cases độc lập:

```powershell
# Chạy toàn bộ kiểm thử
pytest backend/tests -v

# Chạy kiểm thử cơ chế chống Double-booking
pytest backend/tests/test_double_booking.py -v

# Chạy kiểm thử thuật toán tìm đường A*
pytest backend/tests/test_astar.py -v

# Chạy kiểm thử mô hình Machine Learning Random Forest
pytest backend/tests/test_ml_engine.py -v
```

> ✅ **Kết quả kiểm thử:** Đạt **24/24 Test Cases Passed 100%**, đảm bảo hệ thống vận hành ổn định, không có lỗi tiềm ẩn.
