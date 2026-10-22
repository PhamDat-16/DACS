# Smart Parking System — Backend (Phase 1)

Phase 1 hoàn thành: Database schema, kết nối PostgreSQL, và luồng Authentication
(đăng ký / đăng nhập / JWT) chạy được đầu-cuối.

## 1. Yêu cầu môi trường

- Python 3.11+ (khuyến nghị)
- PostgreSQL 14+ đã cài và đang chạy trên máy
  (Windows: dùng installer từ postgresql.org; macOS: `brew install postgresql`;
  Ubuntu/WSL: `sudo apt install postgresql`)

## 2. Tạo database

Mở `psql` hoặc pgAdmin, chạy:

```sql
CREATE DATABASE parking_system;
```

## 3. Cài đặt Python environment

Trong VSCode, mở terminal tại thư mục `backend/`:

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

## 4. Cấu hình biến môi trường

```bash
cp .env.example .env
```

Mở `.env` vừa tạo, sửa `DATABASE_URL` cho khớp với user/password PostgreSQL của bạn.
Ví dụ nếu user là `postgres`, password là `123456`:

```
DATABASE_URL=postgresql://postgres:123456@localhost:5432/parking_system
```

## 5. Chạy migration để tạo bảng

```bash
# Tạo migration đầu tiên từ toàn bộ model đã định nghĩa
alembic revision --autogenerate -m "init tables"

# Áp dụng migration vào database
alembic upgrade head
```

Nếu chạy thành công, vào `psql -d parking_system -c "\dt"` sẽ thấy đủ 6 bảng:
`users, parking_lots, parking_slots, bookings, sessions, occupancy_history`
(cộng thêm bảng `alembic_version` do Alembic tự quản lý).

## 6. Chạy server

```bash
uvicorn app.main:app --reload --port 8000
```

Mở trình duyệt: **http://localhost:8000/docs** — đây là Swagger UI tự sinh,
bạn có thể test toàn bộ API ngay tại đây mà không cần Postman.

## 7. Test luồng Authentication (test thủ công)

**Cách 1 — dùng Swagger UI** (`/docs`): mở endpoint `POST /api/auth/register`,
bấm "Try it out", điền JSON mẫu rồi Execute.

**Cách 2 — dùng curl:**

```bash
# 1. Kiểm tra server sống chưa
curl http://localhost:8000/api/health
# => {"status":"ok"}

# 2. Đăng ký tài khoản
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"123456","full_name":"Nguyen Van A"}'

# 3. Đăng nhập, lấy access_token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"123456"}'
# => {"access_token": "eyJhbGc...", "token_type": "bearer"}

# 4. Dùng token để gọi endpoint được bảo vệ (thay YOUR_TOKEN bằng token ở bước 3)
curl http://localhost:8000/api/users/me \
  -H "Authorization: Bearer YOUR_TOKEN"
# => trả về thông tin user vừa đăng ký
```

Nếu bước 4 trả về đúng thông tin user (không phải lỗi 401) → toàn bộ luồng
Database + Auth + JWT của Phase 1 đã chạy đúng.

## 8. Cấu trúc đã hoàn thành trong Phase 1

```
backend/
├── app/
│   ├── main.py              # Entry point, khởi tạo FastAPI + CORS
│   ├── core/
│   │   ├── config.py        # Đọc .env qua pydantic-settings
│   │   ├── database.py      # SQLAlchemy engine, SessionLocal, Base, get_db()
│   │   ├── security.py      # Hash password (bcrypt), tạo/giải mã JWT
│   │   └── deps.py          # Dependency get_current_user, require_role
│   ├── models/               # 6 model tương ứng ERD đã thống nhất
│   ├── schemas/               # Pydantic schema cho request/response
│   └── routers/
│       ├── auth.py           # POST /api/auth/register, /login
│       └── users.py          # GET /api/users/me (test JWT)
├── alembic/                   # Quản lý migration database
├── requirements.txt
└── .env.example
```

## 9. Những điều cần lưu ý (quan trọng)

- **SQLAlchemy đồng bộ (sync), không phải async**: đây là lựa chọn có chủ đích
  để đồ án dễ hiểu, dễ debug hơn cho người mới. Với quy mô đồ án cơ sở,
  hiệu năng sync là hoàn toàn đủ dùng. Có thể nâng cấp lên `asyncpg` sau nếu
  muốn mở rộng.
- **Model `ParkingSession`** (không phải `Session`): tránh trùng tên với
  `sqlalchemy.orm.Session`. Import đúng: `from app.models.session import ParkingSession`.
- Nếu `alembic revision --autogenerate` báo lỗi "target database is not up to
  date" ở các lần sau, luôn chạy `alembic upgrade head` trước khi tạo revision mới.

## 11. Phase 2 — API đặt chỗ, QR code, chống Double-Booking (MỚI)

Sau khi đã setup xong Phase 1 (DB + auth chạy được), làm thêm các bước sau để
kích hoạt Phase 2:

```bash
# Cài thêm thư viện mới (qrcode, pytest) - chỉ cần chạy 1 lần
pip install -r requirements.txt

# Sinh migration mới cho các thay đổi (nếu có) rồi áp dụng
alembic revision --autogenerate -m "phase 2 - no schema change, safe to skip if empty"
alembic upgrade head
```

### Test luồng đặt chỗ thủ công qua Swagger UI (`/docs`)

1. `POST /api/auth/register` — tạo 1 tài khoản role mặc định là `customer`
2. Để tạo bãi xe cần role `admin` — vào thẳng database đổi role user vừa tạo:
   ```sql
   UPDATE users SET role = 'admin' WHERE email = 'test@example.com';
   ```
3. Login lại (để lấy token mới có role admin), bấm nút "Authorize" trên Swagger,
   dán token vào.
4. `POST /api/lots` — tạo bãi xe mẫu:
   ```json
   {
     "name": "Bãi xe Demo",
     "address": "123 Đường ABC",
     "grid_width": 5,
     "grid_height": 5,
     "obstacle_positions": [
       [2, 2],
       [2, 3]
     ]
   }
   ```
5. `GET /api/lots/{lot_id}` — xem danh sách slot vừa được tự sinh
6. `POST /api/bookings` — đặt 1 slot bất kỳ (lấy `slot_id` từ bước 5), sẽ nhận
   về `qr_code_image` (base64) — dán vào trình duyệt dạng
   `data:image/png;base64,...` để xem ảnh QR thật.
7. Đổi role user (hoặc tạo user khác) thành `staff`, dùng `POST /api/sessions/check-in`
   với `qr_code` lấy từ booking để check-in, rồi `POST /api/sessions/check-out`
   với `session_id` để check-out.

## 12. Test tự động chống Double-Booking (QUAN TRỌNG NHẤT của Phase 2)

```bash
pytest tests/test_double_booking.py -v -s
```

Test này tự tạo 2 user + 1 slot, rồi cho 2 thread cùng gọi `create_booking()`
gần như đồng thời để mô phỏng 2 khách bấm "Đặt chỗ" cùng lúc trên 1 slot.
Assertion kiểm tra: **đúng 1** booking thành công, **đúng 1** booking nhận lỗi 409.
Nếu test pass — cơ chế row-level locking đã hoạt động đúng.

## 13. Phase 3 — Thuật toán A\* tìm đường đến vị trí đỗ

### Test thuật toán độc lập (không cần DB, chạy cực nhanh)

```bash
pytest tests/test_astar.py -v
```

6 test case kiểm tra: đường thẳng không vật cản, né vật cản, không có đường đi khi bị chặn hoàn toàn, start=goal, đường đi phải NGẮN NHẤT (đúng bằng khoảng cách Manhattan), và trường hợp đích là vật cản.

### Test qua API (cần DB, dùng bãi xe đã tạo ở Phase 2)

Trong Swagger UI (`/docs`), endpoint mới:

```
GET /api/lots/{lot_id}/navigate?slot_id={slot_id}&from_x=0&from_y=0
```

- `lot_id`: ID bãi xe (lấy từ `GET /api/lots`)
- `slot_id`: ID slot muốn đến (lấy từ `GET /api/lots/{lot_id}`)
- `from_x`, `from_y`: tọa độ xuất phát, mặc định `(0,0)` coi như vị trí cổng vào

Kết quả trả về danh sách tọa độ `path` — đây chính là dữ liệu Frontend (Phase 5) sẽ dùng để vẽ mũi tên/đường chỉ dẫn trên sơ đồ bãi xe.

### Cấu trúc mới trong Phase 3

```
app/pathfinding/
├── grid.py      # Biểu diễn bãi xe thành lưới 2D thuần Python
└── astar.py     # Thuật toán A* - độc lập hoàn toàn, không phụ thuộc DB/FastAPI
```

Tách `pathfinding/` thành module thuần Python (không import SQLAlchemy hay FastAPI)
là chủ đích — giúp: (1) unit test cực nhanh không cần DB, (2) code thuật toán rõ
ràng, dễ giải thích trong báo cáo đồ án, (3) có thể tái sử dụng ở nơi khác nếu cần.

## 14. Phase 4 — Machine Learning dự báo tỷ lệ lấp đầy (MỚI)

### Cài thêm thư viện

```bash
pip install -r requirements.txt
```

### Test logic ML thuần túy (không cần DB, chạy nhanh)

```bash
pytest tests/test_ml_engine.py -v
```

5 test case: kiểm tra dữ liệu synthetic hợp lệ, tái lập được (reproducible) với
cùng seed, giờ đêm phải thấp hơn giờ cao điểm, model train ra sai số (MAE) chấp
nhận được, và model phải học được đúng pattern (giờ cao điểm dự báo cao hơn giờ đêm).

### Bước 1: Sinh dữ liệu lịch sử giả lập vào database

Dùng `lot_id` đã tạo ở Phase 2 (ví dụ bãi xe Demo):

```bash
python -m app.ml_engine.data_generator --lot-id <lot_id_của_bạn> --days 180
```

Lệnh này sinh 180 ngày x 24 giờ = 4320 bản ghi lịch sử có quy luật thực tế
(cao điểm sáng/chiều, cuối tuần thấp hơn, có nhiễu ngẫu nhiên) và lưu vào bảng
`occupancy_history`.

### Bước 2: Huấn luyện model

```bash
python -m app.ml_engine.train
```

Kết quả in ra MAE, RMSE, và lưu model tại `app/ml_engine/models/occupancy_model.joblib`.
MAE dưới ~0.05-0.08 (5-8%) là hợp lý với dữ liệu synthetic này.

### Bước 3: Test API dự báo qua Swagger UI

Khởi động lại server, thử 2 endpoint mới:

```
GET /api/predict-occupancy?date=2026-09-15&hour_of_day=18&is_holiday=false
GET /api/predict-occupancy/day?date=2026-09-15&is_holiday=false
```

Endpoint đầu trả về dự báo cho 1 giờ cụ thể, endpoint sau trả về cả 24 giờ
trong ngày (dùng để vẽ biểu đồ ở Frontend Phase 5). Lưu ý: `day_of_week` và
`is_weekend` được **tự động tính** từ `date`, không cần tự nhập.

### Cấu trúc mới trong Phase 4

```
app/ml_engine/
├── data_generator.py   # Sinh dữ liệu synthetic có quy luật + CLI seed vào DB
├── train.py             # Train Random Forest + CLI train, tách riêng phần
│                         # train_from_dataframe() thuần túy (test được không cần DB)
├── predict.py            # Load model (lazy singleton), dự báo theo giờ/ngày
└── models/                # Nơi lưu file model .joblib (không commit vào git)
```

### Lưu ý quan trọng

- Model là **1 model chung** cho toàn hệ thống (không tách riêng theo từng bãi xe)
  - lựa chọn đơn giản hóa hợp lý cho đồ án cơ sở, vì pattern giờ cao điểm
    thường tương tự nhau giữa các bãi xe. Có thể mở rộng thành model riêng theo
    `lot_id` sau này nếu muốn nâng cao đồ án.
- Nếu gọi API predict mà chưa chạy `train.py`, sẽ nhận lỗi `503` kèm thông báo
  rõ ràng "chưa có model" - đây là xử lý lỗi có chủ đích, không phải bug.
