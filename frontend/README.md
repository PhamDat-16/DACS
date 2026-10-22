# Smart Parking System — Frontend

Giao diện web trực quan hóa hệ thống bãi đỗ xe thông minh, tích hợp thuật toán dẫn đường A\* và mô hình Machine Learning dự báo tỷ lệ lấp đầy.

## 🚀 Công Nghệ Sử Dụng

- **Vue 3 (Composition API / ESM)**: Kiến trúc component dạng module, tối ưu tốc độ render và vòng đời ứng dụng.
- **GSAP Animation Engine** (theo chuẩn `gsap-frameworks` & `gsap-utils`):
  - `gsap.context()` và `ctx.revert()` trong `onMounted` / `onUnmounted` để chống rò rỉ bộ nhớ (memory leaks).
  - Diễn hoạt xe ảo lăn bánh bám sát tọa độ A\* từ cổng vào đến slot đỗ đích với xoay đầu xe theo góc chuyển động.
  - Hiệu ứng Stagger 2D xuất hiện cho các ô đỗ xe.
  - Hiệu ứng Numeric Counter đếm số liệu thống kê KPI thời gian thực.
  - Biểu đồ dự báo ML 24h kèm thanh trượt chọn giờ mượt mà bằng `gsap.utils.mapRange` và `clamp`.
- **Tailwind CSS (Dark Cyber UI)**: Thiết kế giao diện trung tâm điều hành hiện đại, tương thích đa kích thước màn hình.
- **RESTful API Client**: Kết nối trực tiếp với backend FastAPI (`http://localhost:8000`).

---

## ⚡ Cách Chạy Frontend

### Cách 1: Chạy bằng Python HTTP Server (Khuyên dùng - Không cần cài đặt gì thêm)

Mở terminal tại thư mục `frontend/` và chạy:

```bash
python -m http.server 3000
```

Sau đó truy cập trình duyệt tại: **http://localhost:3000** (khớp với cấu hình `FRONTEND_ORIGIN` của backend).

### Cách 2: Mở trực tiếp

Bạn cũng có thể mở trực tiếp file `frontend/index.html` bằng trình duyệt (Chrome, Edge, Firefox). Hệ thống đã tích hợp sẵn cơ chế **Standalone Mock Engine** tự động tính toán thuật toán A\* và mô phỏng số liệu nếu backend chưa được bật!

---

## 🧭 Các Tính Năng Chính

1. **Sơ đồ lưới bãi đỗ xe (Parking Grid Map)**:
   - Hiển thị trực quan trạng thái từng ô: Trống (Xanh), Đã đặt (Vàng), Đang đỗ (Đỏ), Vật cản (Xám).
2. **Dẫn đường ngắn nhất A\* (A-Star Navigation)**:
   - Bấm vào một vị trí trống bất kỳ trên bản đồ.
   - Hệ thống tự động tính toán lộ trình tối ưu tránh vật cản từ Cổng vào `(0, 0)` đến ô đích.
   - Xe ảo di chuyển mượt mà dọc theo lộ trình.
3. **Dự báo tỷ lệ lấp đầy ML 24h (AI Forecast)**:
   - Xem xu hướng cao điểm/thấp điểm trong ngày.
   - Kéo thanh trượt điều khiển giờ để xem biến động công suất bãi xe.
4. **Đặt chỗ & Vé QR (Booking & QR Check-in)**:
   - Nhập biển số, chọn số giờ đỗ xe và tính phí tự động.
   - Tự động sinh mã QR để quét qua barrier.
