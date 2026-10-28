# 🚗 HỆ THỐNG QUẢN LÝ BÃI ĐỖ XE THÔNG MINH (SMART PARKING SYSTEM - SPS)

> **Hệ thống Quản lý Bãi đỗ xe Thông minh** tích hợp Thuật toán tìm đường tối ưu **A\*** (A-Star Navigation), Mô hình Học máy **Random Forest** (AI Occupancy Forecast), kiểm soát thời gian thực qua **WebSocket**, quét mã **QR Barrier** và chống xung đột đặt chỗ bằng kỹ thuật **SELECT FOR UPDATE**.

---

## 📌 MỤC LỤC

1. [Tính Năng Nổi Bật](#-tính-năng-nổi-bật)
2. [Thông Tin Tài Khoản Mặc Định](#-thông-tin-tài-khoản-mặc-định)
3. [Hướng Dẫn Khởi Chạy Web (Nhanh Nhất)](#-hướng-dẫn-khởi-chạy-web)
4. [Kiến Trúc & Công Nghệ Sử Dụng](#-kiến-trúc--công-nghệ-sử-dụng)
5. [Cơ Sở Dữ Liệu PostgreSQL](#-cơ-sở-dữ-liệu-postgresql)
6. [Tài Liệu Báo Cáo Đồ Án & Phụ Lục](#-tài-liệu-báo-cáo-đồ-án--phụ-lục)

---

## 🌟 TÍNH NĂNG NỔI BẬT

### 1. 👤 Khách Hàng (Customer Portal)

- **Bản đồ trực quan bãi xe**: Hiển thị trạng thái các ô đỗ theo thời gian thực (Trống, Đang đỗ, Đã đặt).
- **Điều hướng thông minh A\***: Tự động tính toán đường đi ngắn nhất từ Cổng vào `(0, 0)` tới vị trí ô đỗ, né tránh các vật cản và ô đã có xe với diễn hoạt hoạt họa xe chạy mượt mà bằng **GSAP 3**.
- **Đặt giữ chỗ trực tuyến (Booking)**: Khóa vị trí ô đỗ tức thời bằng kỹ thuật `SELECT FOR UPDATE`, triệt tiêu hoàn toàn rủi ro trùng lịch đặt (Race Condition / Double-booking).
- **Vé xe điện tử QR Code**: Tự động sinh mã QR động chứa thông tin biển số, mã đặt chỗ để quét mở barrier tại cổng.
- **Vé tháng (Monthly Pass)**: Hỗ trợ đăng ký và gia hạn vé tháng cho cư dân, nhân viên văn phòng.

### 2. 🛡️ Nhân Viên Vận Hành (Staff Portal)

- **Phân quyền theo nơi làm việc**: Mỗi nhân viên khi đăng nhập chỉ quản lý duy nhất bãi xe được phân công (`assigned_lot`).
- **Lưới giám sát ô đỗ thời gian thực**: Tự động đổi màu ô đỗ tức thì khi có xe vào/ra qua kết nối WebSocket 2 chiều.
- **Cửa sổ Barrier & Quét mã QR**: Quét mã QR của khách bằng camera hoặc nhập mã để đối chiếu và mở cần barrier tự động.
- **Tiếp nhận xe vãng lai (Walk-in)**: Cấp phát nhanh ô đỗ trống gần nhất cho phương tiện không đặt trước.
- **Check-out & Thu phí**: Tự động tính thời gian đỗ, áp biểu phí theo giờ và in hóa đơn thanh toán.

### 3. 👑 Quản Trị Viên (Admin Portal)

- **Quản trị người dùng & Nhân sự**: Cấp tài khoản nhân viên mới, chọn đơn vị bãi đỗ xe làm việc rõ ràng.
- **Quản lý danh mục bãi & Cấu hình ô đỗ**: Thiết lập kích thước lưới ma trận $Width \times Height$, đơn giá theo giờ.
- **Báo cáo doanh thu**: Biểu đồ thống kê doanh thu theo ngày, số lượt xe, giờ cao điểm.
- **Trí tuệ nhân tạo (AI Forecast)**: Dự báo tỷ lệ lấp đầy trong 24 giờ tới bằng mô hình **Random Forest Regressor** (200 trees, huấn luyện trên 4.320 mẫu, MAE = 0.058).

---

## 🔑 THÔNG TIN TÀI KHOẢN MẶC ĐỊNH

Hệ thống đã có sẵn các tài khoản mẫu trong cơ sở dữ liệu để đăng nhập và kiểm thử:

| Vai trò                     | Email đăng nhập          | Tên đăng nhập tắt | Mật khẩu mặc định | Đơn vị làm việc (`assigned_lot`) |
| :-------------------------- | :----------------------- | :---------------- | :---------------- | :------------------------------- |
| **Quản trị viên (Admin)**   | `admin@parking.vn`       | `admin`           | `admin123`        | Toàn quyền hệ thống              |
| **Nhân viên (Staff)**       | `staff@parking.vn`       | `staff`           | `1234567890`      | Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông) |
| **Nhân viên 2 (Staff)**     | `manh@gmail.com`         | `manh`            | `1234567890`      | Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông) |
| **Khách hàng (Customer)**   | `customer@parking.vn`    | `customer`        | `123456`          | Khách gửi xe cá nhân             |
| **Khách hàng 2 (Customer)** | `phvdat220805@gmail.com` | —                 | `1234567890`      | Khách gửi xe cá nhân             |

> 💡 **Mẹo:** Ở ô Email đăng nhập, bạn có thể gõ trực tiếp chữ `admin` hoặc `staff` kèm mật khẩu tương ứng, hệ thống sẽ tự động nhận diện alias thông minh!

---

## 🚀 HƯỚNG DẪN KHỞI CHẠY WEB

### Cách 1: Khởi động 1-Click tự động (Khuyên dùng)

Ngay tại thư mục gốc `D:\smart-parking-system\`:

1. Nhấp đúp chuột vào file: **`run_web.bat`**
2. Script sẽ tự động bật **Backend (Port 8000)**, **Frontend (Port 3000)** và tự động mở trình duyệt web.

### Cách 2: Khởi động thủ công bằng Terminal

#### Bước 1: Khởi động Backend FastAPI

Mở Terminal thứ nhất tại `D:\smart-parking-system\backend`:

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

- Backend chạy tại: `http://127.0.0.1:8000`
- Tài liệu Swagger API: `http://127.0.0.1:8000/docs`

#### Bước 2: Khởi động Frontend Web

Mở Terminal thứ hai tại `D:\smart-parking-system\frontend`:

```powershell
..\backend\venv\Scripts\python.exe -m http.server 3000
```

- Truy cập giao diện người dùng tại: **`http://localhost:3000`**

### Cách 3: Kiểm tra nhanh cơ sở dữ liệu

- Nhấp đúp chuột vào file: **`xem_database.bat`** để kiểm tra kết nối PostgreSQL và xem tổng số bản ghi trong 6 bảng.

---

## 🏗️ KIẾN TRÚC & CÔNG NGHỆ SỬ DỤNG

- **Frontend**:
  - **Vue 3** (Composition API, `<script setup>`)
  - **GSAP 3** (GreenSock Animation Platform) điều hướng xe chạy trên lưới 2D
  - **Tailwind CSS** (Dark Cyber Theme)
  - **HTML5 QR Code Scanner** (Quét mã vạch trực tiếp qua Webcam/Camera)
- **Backend**:
  - **FastAPI** (Python 3.11, ASGI Uvicorn)
  - **SQLAlchemy ORM** & **Pydantic v2**
  - **WebSocket Protocol** (Cập nhật trạng thái ô đỗ thời gian thực)
  - **Bcrypt** (Mã hóa mật khẩu 1 chiều) & **JWT** (JSON Web Token)
- **Machine Learning & Thuật Toán**:
  - **Thuật toán A\***: Tìm đường tối ưu với hàm Heuristic Manhattan và hàng đợi ưu tiên `heapq`.
  - **Random Forest Regressor**: 200 Decision Trees, nạp Singleton trong RAM, thời gian suy luận dưới 5ms.
- **Database**:
  - **PostgreSQL 15** (Lưu trữ quan hệ chuẩn 3NF, hỗ trợ `SELECT FOR UPDATE`).

---

## 🗄️ CƠ SỞ DỮ LIỆU POSTGRESQL

Hệ thống quản lý dữ liệu qua 6 bảng thực thể:

1. `users`: Tài khoản khách hàng, nhân viên, admin và trường `assigned_lot`.
2. `parking_lots`: Thông tin bãi đỗ xe, địa chỉ, kích thước lưới $Width \times Height$, đơn giá.
3. `parking_slots`: Danh mục từng vị trí ô đỗ, tọa độ $(x, y)$, loại xe, trạng thái.
4. `bookings`: Quản lý vé đặt chỗ, mã QR, thời gian giữ chỗ và phí đỗ.
5. `sessions`: Phiên đỗ xe thực tế khi phương tiện check-in/check-out qua barrier.
6. `occupancy_history`: Dữ liệu chuỗi thời gian phục vụ mô hình AI dự báo tỷ lệ lấp đầy.

---

## 📄 TÀI LIỆU BÁO CÁO ĐỒ ÁN & PHỤ LỤC

Trong thư mục dự án đã tạo sẵn các tài liệu nghiệm thu chuẩn quy cách Đại học Phenikaa:

- **Báo cáo đồ án đầy đủ (Word .docx)**: `D:\smart-parking-system\Bao_cao_do_an_Smart_Parking_System.docx` (và trong thư mục `Downloads`).
- **Bộ kiểm thử tự động Pytest**: Chạy `pytest backend/tests/ -v` (11/11 Test cases Passed).
