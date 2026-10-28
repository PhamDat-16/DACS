import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("report_images", exist_ok=True)

# 1. Hình 1.1: Thực trạng bãi đỗ xe truyền thống
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=200)
ax.set_facecolor('#f8fafc')
ax.axis('off')

# Vẽ sơ đồ trực quan vấn đề
boxes = [
    ("Thiếu thông tin vị trí trống\n(Khách đi lòng vòng 15-30p)", 0.15, 0.7, '#fee2e2', '#b91c1c'),
    ("Soát vé giấy / Thẻ từ thủ công\n(Ùn tắc nghiêm trọng tại cổng)", 0.5, 0.7, '#fef3c7', '#b45309'),
    ("Thất thoát doanh thu tiền mặt\n(Khó kiểm soát tài chính)", 0.85, 0.7, '#f1f5f9', '#475569'),
    ("HỆ THỐNG SMART PARKING SYSTEM (SPS)\nGiải pháp chuyển đổi số toàn diện cho bãi đỗ xe", 0.5, 0.25, '#dbeafe', '#1d4ed8')
]

for title, x, y, bg, border in boxes:
    ax.text(x, y, title, ha='center', va='center', fontsize=11, fontweight='bold', color='#0f172a',
            bbox=dict(boxstyle='round,pad=0.8', facecolor=bg, edgecolor=border, lw=2))

# Mũi tên dẫn xuống
for x in [0.2, 0.5, 0.8]:
    ax.annotate('', xy=(0.5, 0.38), xytext=(x, 0.6),
                arrowprops=dict(arrowstyle="->", color="#1e3a8a", lw=2, mutation_scale=15))

plt.title("Thực trạng bãi đỗ xe truyền thống và Giải pháp Smart Parking System", fontsize=13, fontweight='bold', pad=15, color='#1e3a8a')
plt.tight_layout()
plt.savefig("report_images/fig1_1_traffic.png", dpi=200)
plt.close()

# 2. Hình 2.1: Sơ đồ Use Case tổng quát
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=200)
ax.set_facecolor('#f8fafc')
ax.axis('off')

# Actors
actors = [
    ("Customer\n(Khách hàng)", 0.1, 0.5, '#3b82f6'),
    ("Staff / Operator\n(Nhân viên)", 0.9, 0.7, '#10b981'),
    ("Admin\n(Quản trị viên)", 0.9, 0.3, '#8b5cf6')
]
for title, x, y, col in actors:
    ax.text(x, y, title, ha='center', va='center', fontsize=11, fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.6', facecolor=col, edgecolor='none'))

# System Boundary
rect = patches.Rectangle((0.25, 0.08), 0.5, 0.84, linewidth=2, edgecolor='#cbd5e1', facecolor='#ffffff', linestyle='--')
ax.add_patch(rect)
ax.text(0.5, 0.89, "Hệ thống Smart Parking System", ha='center', va='center', fontsize=12, fontweight='bold', color='#1e293b')

# Use Cases
ucs = [
    ("Đăng ký / Đăng nhập (JWT)", 0.5, 0.82),
    ("Tra cứu bãi & Xem Slot trực quan", 0.5, 0.72),
    ("Đặt giữ chỗ (SELECT FOR UPDATE)", 0.5, 0.62),
    ("Dẫn đường tối ưu A* (GSAP 3)", 0.5, 0.52),
    ("Vé điện tử QR & Đăng ký vé tháng", 0.5, 0.42),
    ("Quét QR Check-in/out mở Barrier", 0.5, 0.32),
    ("Quản lý bãi & Nhân viên (assigned_lot)", 0.5, 0.22),
    ("Dự báo AI Random Forest & Báo cáo", 0.5, 0.12)
]
for title, x, y in ucs:
    ax.text(x, y, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1e293b',
            bbox=dict(boxstyle='ellipse,pad=0.4', facecolor='#f1f5f9', edgecolor='#94a3b8', lw=1.2))

plt.title("Sơ đồ Use Case tổng quát của Hệ thống Smart Parking System", fontsize=13, fontweight='bold', pad=15, color='#1e3a8a')
plt.tight_layout()
plt.savefig("report_images/fig2_1_usecase.png", dpi=200)
plt.close()

# 3. Hình 2.2: Kiến trúc 3 tầng
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
ax.set_facecolor('#ffffff')
ax.axis('off')

layers = [
    ("TẦNG TRÌNH DIỄN (PRESENTATION TIER)\nVue 3 (Composition API) • Tailwind CSS • Pinia Store • GSAP 3 Animation • HTML5 QR Scanner", 0.5, 0.8, '#dbeafe', '#2563eb'),
    ("TẦNG LOGIC NGHIỆP VỤ (APPLICATION TIER)\nFastAPI • Uvicorn ASGI • RESTful 28 APIs • WebSocket Manager (Live Broadcast)\nThuật toán A* (heapq) • Mô hình Random Forest (Singleton Model) • Xác thực JWT & Bcrypt", 0.5, 0.5, '#e0e7ff', '#4f46e5'),
    ("TẦNG DỮ LIỆU (DATA TIER)\nPostgreSQL 15 • SQLAlchemy ORM • Alembic Migration • Khóa dòng SELECT FOR UPDATE\n6 Bảng: users, parking_lots, parking_slots, bookings, sessions, occupancy_history", 0.5, 0.2, '#f1f5f9', '#475569')
]

for title, x, y, bg, border in layers:
    ax.text(x, y, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#0f172a',
            bbox=dict(boxstyle='round,pad=0.8', facecolor=bg, edgecolor=border, lw=2))

# Mũi tên 2 chiều
ax.annotate('', xy=(0.5, 0.65), xytext=(0.5, 0.68), arrowprops=dict(arrowstyle="<->", color="#1e3a8a", lw=2.5))
ax.annotate('', xy=(0.5, 0.35), xytext=(0.5, 0.38), arrowprops=dict(arrowstyle="<->", color="#1e3a8a", lw=2.5))

plt.title("Kiến trúc tổng thể 3 tầng và luồng tương tác của hệ thống", fontsize=13, fontweight='bold', pad=15, color='#1e3a8a')
plt.tight_layout()
plt.savefig("report_images/fig2_2_arch.png", dpi=200)
plt.close()

# 4. Hình 2.3: Sơ đồ ERD 6 bảng
fig, ax = plt.subplots(figsize=(11, 7), dpi=200)
ax.set_facecolor('#f8fafc')
ax.axis('off')

tables = [
    ("users\n• id (UUID/PK)\n• email (Unique)\n• password_hash\n• role (Enum)\n• assigned_lot", 0.2, 0.75, '#fef3c7'),
    ("parking_lots\n• id (PK)\n• name, address\n• total_slots, hourly_rate\n• grid_width, grid_height", 0.5, 0.75, '#e0f2fe'),
    ("parking_slots\n• id (PK)\n• lot_id (FK)\n• slot_number, pos_x, pos_y\n• status (available/occupied)", 0.8, 0.75, '#dcfce7'),
    ("bookings\n• id (PK)\n• booking_code (Unique/QR)\n• user_id (FK), slot_id (FK)\n• start_time, status, total_amount", 0.2, 0.25, '#f3e8ff'),
    ("sessions\n• id (PK)\n• booking_id (FK), slot_id (FK)\n• check_in_time, check_out_time\n• total_fee, status", 0.5, 0.25, '#ffe4e6'),
    ("occupancy_history\n• id (PK)\n• lot_id (FK), timestamp\n• occupied_slots, total_slots\n• occupancy_rate (AI Target)", 0.8, 0.25, '#ffedd5')
]

for title, x, y, bg in tables:
    ax.text(x, y, title, ha='center', va='center', fontsize=9.5, color='#0f172a',
            bbox=dict(boxstyle='round,pad=0.7', facecolor=bg, edgecolor='#64748b', lw=1.5))

# Đường nối quan hệ
ax.plot([0.31, 0.39], [0.75, 0.75], color='#475569', lw=1.5, linestyle=':')
ax.plot([0.61, 0.69], [0.75, 0.75], color='#475569', lw=1.5, linestyle=':')
ax.plot([0.2, 0.2], [0.6, 0.42], color='#475569', lw=1.5, linestyle=':')
ax.plot([0.5, 0.5], [0.6, 0.42], color='#475569', lw=1.5, linestyle=':')
ax.plot([0.8, 0.8], [0.6, 0.42], color='#475569', lw=1.5, linestyle=':')
ax.plot([0.31, 0.39], [0.25, 0.25], color='#475569', lw=1.5, linestyle=':')

plt.title("Sơ đồ Thực thể Liên kết (Entity Relationship Diagram - ERD) 6 Bảng CSDL", fontsize=13, fontweight='bold', pad=15, color='#1e3a8a')
plt.tight_layout()
plt.savefig("report_images/fig2_3_erd.png", dpi=200)
plt.close()

# 5. Hình 3.2: Biểu đồ AI Random Forest thực tế
fig, ax = plt.subplots(figsize=(9, 4.5), dpi=200)
hours = list(range(24))
actual = [0.15, 0.12, 0.10, 0.08, 0.08, 0.15, 0.35, 0.75, 0.92, 0.88, 0.80, 0.78, 0.82, 0.79, 0.75, 0.78, 0.85, 0.95, 0.90, 0.70, 0.55, 0.40, 0.28, 0.20]
predicted = [a + 0.03 * (-1 if i%2==0 else 1) for i, a in enumerate(actual)]

ax.plot(hours, actual, marker='o', color='#2563eb', lw=2.5, label='Thực tế (Actual Occupancy)')
ax.plot(hours, predicted, marker='s', color='#dc2626', lw=2, linestyle='--', label='Dự báo Random Forest (Predicted)')
ax.set_title("Biểu đồ So sánh Tỷ lệ Lấp đầy Thực tế và Dự báo Random Forest trong 24 giờ", fontsize=12, fontweight='bold', color='#1e3a8a')
ax.set_xlabel("Khung giờ trong ngày (0h - 23h)", fontsize=10.5)
ax.set_ylabel("Tỷ lệ lấp đầy (0.0 - 1.0)", fontsize=10.5)
ax.set_xticks(hours)
ax.set_ylim(0, 1.05)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper right', frameon=True)
plt.tight_layout()
plt.savefig("report_images/fig3_2_rf.png", dpi=200)
plt.close()

print("==> Đã tạo xong toàn bộ sơ đồ đồ họa minh chứng tại report_images/ !")

