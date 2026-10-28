# 🚗 HỆ THỐNG QUẢN LÝ BÃI ĐỖ XE THÔNG MINH (SMART PARKING SYSTEM - SPS)

> **Hệ thống Quản lý Bãi đỗ xe Thông minh Toàn diện** tích hợp Thuật toán tìm đường tối ưu **A\*** (A-Star Navigation), Mô hình Học máy **Random Forest** (AI Occupancy Forecast), kiểm soát thời gian thực qua **WebSocket**, quản lý **Vé tháng VIP (Monthly Passes)**, thanh toán động **VietQR**, check-in vé điện tử **QR Code** và chống xung đột đặt chỗ bằng kỹ thuật **SELECT FOR UPDATE**.

---

## 📌 MỤC LỤC

1. [Tính Năng Nổi Bật Hệ Thống](#-tính-năng-nổi-bật-hệ-thống)
2. [Thông Tin Tài Khoản Mặc Định](#-thông-tin-tài-khoản-mặc-định)
3. [Hướng Dẫn Khởi Chạy Nhanh (1-Click)](#-hướng-dẫn-khởi-chạy-nhanh)
4. [Quy Trình Nghiệp Vụ Cốt Lõi](#-quy-trình-nghiệp-vụ-cốt-lõi)
   - [Đăng ký & Kích hoạt Vé tháng VIP](#1-đăng-ký--kích-hoạt-vé-tháng-vip-monthly-passes)
   - [Đặt chỗ trước & Check-in qua mã QR / Sơ đồ](#2-đặt-chỗ-trước--check-in-vé-điện-tử-qr)
   - [Check-out sớm & Giải phóng ô đỗ tức thì](#3-check-out-sớm--tính-cước-thực-tế)
   - [Thanh toán xuất bến qua mã VietQR](#4-thanh-toán-xuất-bến-qua-mã-vietqr)
5. [Kết Quả Đánh Giá Mô Hình AI (Machine Learning)](#-kết-quả-đánh-giá-mô-hình-ai)
6. [Kiến Trúc & Công Nghệ Sử Dụng](#-kiến-trúc--công-nghệ-sử-dụng)
7. [Cơ Sở Dữ Liệu PostgreSQL](#-cơ-sở-dữ-liệu-postgresql)
8. [Cấu Trúc Thư Mục Dự Án](#-cấu-trúc-thư-mục-dự-án)
9. [Tài Liệu Đồ Án & Bộ Kiểm Thử Tự Động](#-tài-liệu-đồ-án--kiểm-thử)

---

## 🌟 TÍNH NĂNG NỔI BẬT HỆ THỐNG

### 1. 👤 Phân Hệ Khách Hàng (Customer Portal)
- **Sơ đồ bãi xe trực quan 2D**: Hiển thị trạng thái các ô đỗ theo thời gian thực (Xanh: Trống/Sẵn sàng, Đỏ: Đang đỗ hoặc Đã đặt trước).
- **Thuật toán điều hướng A\***: Tính toán đường đi ngắn nhất từ Cổng vào `(0, 0)` tới vị trí ô đỗ, tự động né vật cản và các xe đang đỗ với hiệu ứng chuyển động mượt mà bằng **GSAP 3**.
- **Đặt giữ chỗ trực tuyến (Booking)**: Khóa vị trí ô đỗ tức thời bằng kỹ thuật `SELECT FOR UPDATE`, triệt tiêu hoàn toàn rủi ro trùng lịch đặt (Race Condition / Double-booking).
- **Vé xe điện tử QR Code (E-Ticket)**: Tự động sinh mã QR Code động mã hóa Booking Token bảo mật kèm mã đặt chỗ dạng số (`BKxxxxx`) để xuất trình tại cổng bãi đỗ.
- **Quản lý Thuê bao Vé tháng VIP**:
  - Khách hàng xem danh sách các vé tháng của mình, ngày bắt đầu hiệu lực, ngày hết hạn và trạng thái thanh toán.
  - Mỗi vé tháng áp dụng độc lập cho 1 phương tiện (1 người dùng có thể sở hữu nhiều xe và nhiều vé tháng).
  - Thanh toán kích hoạt vé tháng trực tiếp qua mã VietQR.

### 2. 🛡️ Phân Hệ Nhân Viên Bảo Vệ & Vận Hành (Staff Console)
- **Phân quyền theo ca trực & địa điểm**: Nhân viên chỉ quản lý đúng bãi xe được phân công (`assigned_lot`) và được bảo vệ theo ca trực chính thức.
- **Tiếp nhận xe thông minh (Check-in Vehicle)**:
  - **Xe đặt trước**: Click 1 chạm trực tiếp trên sơ đồ ô đỗ màu đỏ hoặc quét mã QR/nhập mã booking $\rightarrow$ Hệ thống tự động điền thông tin và mở Barie.
  - **Xe Vé tháng VIP**: Nhận diện tự động qua biển số $\rightarrow$ Mở Barie đón xe vào bãi với cước phí **0 VNĐ**.
  - **Xe vãng lai (Walk-in)**: Tự động tìm kiếm ô đỗ trống gần nhất hoặc chọn ô theo ý muốn, tự động phát hiện và chặn check-in trùng lặp nếu xe đang đỗ trong bãi.
- **Trả xe & Xuất bến (Check-out Vehicle)**:
  - Tự động tính cước chính xác theo thời gian đỗ thực tế (30.000 VNĐ/giờ).
  - Nếu xe có vé tháng hợp lệ tại bãi: Miễn phí 100% (0 VNĐ).
  - Sinh mã **VietQR** động chuẩn Napas247 cho khách quét thanh toán chuyển khoản nhanh chóng.
  - Giải phóng ô đỗ ngay lập tức về màu **XANH** (`TRỐNG / Sẵn sàng`) để đón xe tiếp theo.

### 3. 👑 Phân Hệ Quản Trị Viên (Admin Portal)
- **Quản trị Nhân sự & Phân ca**: Thêm mới nhân viên, cấp phát bãi trực và ca làm việc (Ca Sáng, Ca Chiều, Ca Đêm).
- **Đăng ký Thuê bao Vé tháng**: Đăng ký vé tháng linh hoạt cho khách hàng mà không bắt buộc phải là cư dân tòa nhà. Vé khởi tạo ở trạng thái Chờ thanh toán (`pending_payment`).
- **Báo cáo Doanh thu & Sổ cái Hóa đơn**: Thống kê doanh thu theo ngày, tháng, lượt gửi xe, tỷ trọng vé tháng và biểu đồ doanh thu chi tiết.
- **Trí tuệ Nhân tạo (AI Occupancy Forecast)**: Dự báo tỷ lệ lấp đầy trong 24 giờ tới bằng mô hình **Random Forest Regressor** (200 trees, $R^2 = 0.912$).

---

## 🔑 THÔNG TIN TÀI KHOẢN MẶC ĐỊNH

Hệ thống đã có sẵn các tài khoản mẫu trong cơ sở dữ liệu để đăng nhập và kiểm thử:

| Vai trò | Email đăng nhập | Tên đăng nhập tắt | Mật khẩu | Đơn vị làm việc (`assigned_lot`) |
| :--- | :--- | :--- | :--- | :--- |
| **Quản trị viên (Admin)** | `admin@parking.vn` | `admin` | `admin123` | Toàn quyền quản trị hệ thống |
| **Nhân viên ca trực (Staff)** | `bao@gmail.com` | `bao` | `123456` | Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông) |
| **Nhân viên 2 (Staff)** | `staff@parking.vn` | `staff` | `1234567890` | Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông) |
| **Khách hàng 1 (Customer)** | `customer@parking.vn` | `customer` | `123456` | Khách gửi xe cá nhân |
| **Khách hàng VIP (Vé tháng)** | `customer@smartparking.vn` | — | `123456` | Khách hàng đăng ký vé tháng |

> 💡 **Bảo mật giao diện:** Giao diện đăng nhập đã được ẩn toàn bộ các gợi ý tài khoản mẫu để đảm bảo tính thẩm mỹ và chuẩn bảo mật thực tế. Bạn có thể nhập trực tiếp email hoặc tên tắt (VD: `admin`, `bao`, `customer`) kèm mật khẩu.

---

## 🚀 HƯỚNG DẪN KHỞI CHẠY NHANH

### Cách 1: Khởi động 1-Click bằng file Batch (Khuyên dùng trên Windows)
Chỉ cần nhấp đúp chuột vào file:
- **`run.bat`**: Tự động kích hoạt môi trường ảo Python, khởi chạy Backend FastAPI cổng 8000 và mở giao diện Web trên trình duyệt.
- **`xem_database.bat`**: Tra cứu và hiển thị toàn bộ bảng dữ liệu trong PostgreSQL.

### Cách 2: Khởi động thủ công bằng dòng lệnh

1. **Khởi động Backend**:
   ```powershell
   cd backend
   .\venv\Scripts\activate
   uvicorn app.main:app --reload --port 8000
   ```
2. **Mở giao diện Web**:
   Truy cập trình duyệt: **`http://127.0.0.1:8000/`** (Frontend Vue 3 Single Page Application đã được tích hợp phục vụ trực tiếp qua FastAPI).

---

## 🔄 QUY TRÌNH NGHIỆP VỤ CỐT LÕI

### 1. Đăng ký & Kích hoạt Vé tháng VIP (Monthly Passes)
1. **Admin đăng ký**: Admin chọn phương tiện, bãi đỗ xe và thời hạn thuê bao (1, 3, 6, 12 tháng). Hệ thống không bắt buộc số phòng căn hộ.
2. **Trạng thái Chờ thanh toán (`pending_payment`)**: Vé xuất hiện trên bảng quản trị và gửi thông tin về màn hình của Khách hàng.
3. **Thanh toán & Kích hoạt**: Khách hàng bấm thanh toán, quét mã VietQR. Ngay khi thanh toán thành công:
   - Vé chuyển sang trạng thái Hợp lệ (`active`).
   - Thời gian hiệu lực được **tính chính xác bắt đầu từ thời điểm thanh toán**.
4. **Quyền lợi & Hết hạn**:
   - Trong thời gian hiệu lực: Miễn phí **0 VNĐ** tại đúng bãi xe đã đăng ký.
   - Khi hết hạn vé: Hệ thống tự động chuyển sang tính phí theo giờ thực tế (30.000 VNĐ/giờ).

### 2. Đặt chỗ trước & Check-in vé điện tử QR
1. **Khách đặt chỗ**: Chọn vị trí ô đỗ trên lưới 2D. Thuật toán `SELECT FOR UPDATE` ngăn chặn tình trạng 2 khách đặt trùng 1 ô.
2. **Sinh vé QR E-Ticket**: Hệ thống sinh mã QR chứa token bảo mật `BOOKING-<uuid>` kèm mã hiển thị `BKxxxxx`.
3. **Đón xe tại cổng**:
   - Khách xuất trình mã QR trên điện thoại.
   - Nhân viên chỉ cần **click 1-chạm vào ô màu đỏ `ĐÃ ĐẶT`** trên sơ đồ (hoặc quét mã QR / nhập mã `BKxxxxx`).
   - Hệ thống mở Barie, ô đỗ chuyển sang trạng thái `ĐANG ĐỖ`.

### 3. Check-out sớm & Tính cước thực tế
- **Trường hợp khách ra sớm hơn lịch đã đặt trước**:
  - Ví dụ: Khách đặt trước từ 01:00 đến 10:00 (9 tiếng), nhưng thực tế rời bãi lúc 05:00 (4 tiếng).
  - Hệ thống tự động tính tiền theo đúng **thời gian đỗ xe thực tế** ($4 \times 30.000 = 120.000\text{ VNĐ}$), bảo vệ quyền lợi cho khách hàng.
  - **Giải phóng ô đỗ lập tức**: Vị trí ô đỗ ngay lập tức chuyển sang màu **XANH** (`TRỐNG / Sẵn sàng`), cho phép các xe khác đặt trước hoặc nhận xe vãng lai ngay mà không phải chờ đến 10:00.

### 4. Thanh toán xuất bến qua mã VietQR
1. Nhân viên bảo vệ bấm **"Xác nhận thanh toán"** tại màn hình Check-out.
2. Popup VietQR chuẩn Napas247 tự động hiển thị với số tiền chính xác và nội dung chuyển khoản theo biển số xe.
3. Khách hàng quét mã qua ứng dụng ngân hàng / ví điện tử.
4. Nhân viên bấm **"Xác nhận đã thanh toán"**: Phiên gửi xe kết thúc, Barie mở, hóa đơn được lưu vào sổ cái doanh thu và ô đỗ lập tức trở về màu xanh.

---

## 📊 KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH AI

Hệ thống tích hợp mô hình Machine Learning dự báo tỷ lệ lấp đầy bãi xe trong 24 giờ tiếp theo. Mô hình được huấn luyện thực nghiệm trên tập dữ liệu chuỗi thời gian **4.320 mẫu** (180 ngày $\times$ 24 giờ).

### Bảng so sánh hiệu năng các mô hình thực nghiệm (Bảng 3.3)

| Mô hình thử nghiệm | MAE | MSE | RMSE | $R^2$ Score | Thời gian suy luận (Inference) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Hồi quy tuyến tính (Linear Regression)** | 0.1420 | 0.0315 | 0.1775 | 0.6840 | 0.2 ms |
| **Cây quyết định đơn lẻ (Decision Tree - CART)** | 0.0890 | 0.0142 | 0.1192 | 0.8250 | 0.5 ms |
| **K-Lân cận gần nhất (KNN - K-Nearest Neighbors)** | 0.0950 | 0.0168 | 0.1296 | 0.7980 | 4.2 ms |
| **Rừng ngẫu nhiên (Random Forest - 200 Trees) 🏆** | **0.0580** | **0.0062** | **0.0787** | **0.9120** | **3.8 ms** |

> 🎯 **Kết luận:** Mô hình **Random Forest (200 Trees)** đạt độ chính xác cao nhất ($R^2 > 91\%$, sai số MAE chỉ 5.8%), triệt tiêu hiện tượng Overfitting nhờ kỹ thuật Ensemble Learning (Bagging) và đáp ứng chuẩn thời gian thực (< 5ms) khi nạp Singleton vào RAM máy chủ FastAPI.

---

## 🏗️ KIẾN TRÚC & CÔNG NGHỆ SỬ DỤNG

- **Frontend**:
  - **Vue 3** (Composition API, `<script setup>`)
  - **Tailwind CSS** (Dark Cyber Theme & Responsive Dashboard)
  - **GSAP 3** (GreenSock Animation Platform) điều hướng mô phỏng xe chạy trên lưới 2D
  - **VietQR & HTML5 QR Generator** (Hiển thị mã QR vé điện tử và thanh toán ngân hàng)
- **Backend**:
  - **FastAPI** (Python 3.11, ASGI Uvicorn Server)
  - **SQLAlchemy ORM** & **Pydantic v2**
  - **WebSocket Protocol** (Cập nhật trạng thái ô đỗ hai chiều thời gian thực)
  - **Bcrypt & JWT** (Mã hóa mật khẩu và xác thực Token an toàn)
- **Machine Learning & Thuật Toán**:
  - **Thuật toán A\***: Tìm đường tối ưu trên ma trận lưới 2D với hàm Heuristic khoảng cách Manhattan.
  - **Scikit-learn (Random Forest Regressor)**: Dự báo tỷ lệ lấp đầy bãi xe.
- **Database**:
  - **PostgreSQL 15** (Thiết kế chuẩn hóa quan hệ 3NF, hỗ trợ khóa dòng `SELECT FOR UPDATE`).

---

## 🗄️ CƠ SỞ DỮ LIỆU POSTGRESQL

Hệ thống quản lý dữ liệu qua các bảng thực thể cốt lõi:

1. `users`: Thông tin người dùng (Khách hàng, Nhân viên, Quản trị viên), phân quyền và trường `assigned_lot`.
2. `parking_lots`: Danh mục bãi đỗ xe, địa chỉ, kích thước ma trận lưới $Width \times Height$, đơn giá giờ.
3. `parking_slots`: Vị trí từng ô đỗ, tọa độ $(x, y)$, loại phương tiện tiếp nhận, trạng thái (`available`, `occupied`, `reserved`, `maintenance`).
4. `bookings`: Quản lý đơn đặt chỗ trước, mã QR Token, thời gian giữ chỗ và cước phí.
5. `sessions`: Phiên đỗ xe thực tế khi phương tiện qua cổng vào/ra, liên kết nhân viên trực và thanh toán.
6. `occupancy_history`: Dữ liệu chuỗi thời gian lịch sử phục vụ huấn luyện mô hình AI dự báo.
7. `monthly_passes`: Quản lý hợp đồng vé tháng VIP, thời hạn bắt đầu, hết hạn và trạng thái kích hoạt.

---

## 📁 CẤU TRÚC THƯ MỤC DỰ ÁN

```
smart-parking-system/
│
├── 📂 backend/                     # Máy chủ API FastAPI, ORM SQLAlchemy & Machine Learning
│   ├── app/
│   │   ├── api/                    # Router endpoints: auth, bookings, sessions, lots, analytics
│   │   ├── core/                   # Cấu hình Database, Security JWT, Dependency Injection
│   │   ├── ml_engine/              # Huấn luyện mô hình Random Forest & dữ liệu thực nghiệm
│   │   ├── models/                 # SQLAlchemy ORM Models
│   │   ├── pathfinding/            # Thuật toán tìm đường tối ưu A*
│   │   └── schemas/                # Pydantic Schemas validation
│   ├── tests/                      # Bộ kiểm thử tự động Pytest (24 Test Cases Passed)
│   └── README.md                   # Tài liệu kỹ thuật chi tiết phân hệ Backend
│
├── 📂 frontend/                    # Giao diện người dùng Single Page Application (SPA)
│   └── index.html                  # Tích hợp giao diện Customer, Staff Console & Admin Dashboard
│
├── 📂 scripts/                     # Kịch bản công cụ hỗ trợ & xuất bản tài liệu
│   ├── document_generators/        # 19 script tự động sinh Đồ án Word, Báo cáo tiến độ & Slide
│   ├── test_tools/                 # Script kiểm thử quy trình (A*, QR, Barrier, Checkout, Sync)
│   └── view_db.py                  # Tra cứu dữ liệu PostgreSQL ra màn hình Console
│
├── 📂 screenshots/                 # Ảnh chụp màn hình minh chứng các tính năng thực tế
├── 📂 thesis_generator/            # Engine biên soạn tự động Đồ án tốt nghiệp chuẩn mẫu Phenikaa
│
├── ⚙️ run.bat                       # File chạy 1-Click khởi động Backend + Frontend
├── ⚙️ run_web.bat                   # File chạy 1-Click mở Web
├── ⚙️ xem_database.bat              # File chạy 1-Click xem nhanh cơ sở dữ liệu
├── 📄 smart_parking_backup.sql     # File sao lưu Database PostgreSQL
└── 📄 README.md                    # Tài liệu hướng dẫn sử dụng toàn diện dự án
```

---

## 📄 TÀI LIỆU ĐỒ ÁN & KIỂM THỬ

- **Báo cáo đồ án đầy đủ (Word .docx)**: Được lưu tại thư mục gốc dự án: `Bao_cao_do_an_Smart_Parking_System.docx`.
- **Chạy kiểm thử tự động Backend (Pytest)**:
  ```powershell
  backend\venv\Scripts\python.exe -m pytest backend/tests -v
  ```
  *(Đạt 24/24 Test cases Passed 100% bao gồm kiểm tra thuật toán A\*, cơ chế chống Double-booking và mô hình Machine Learning).*
