import sys
import os
import subprocess

# Tự động chuyển sang môi trường ảo backend/venv nếu người dùng chạy bằng Python toàn cục
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
venv_python = os.path.abspath(os.path.join(project_root, "backend", "venv", "Scripts", "python.exe"))
if os.path.exists(venv_python) and os.path.normcase(sys.executable) != os.path.normcase(venv_python):
    result = subprocess.run([venv_python] + sys.argv)
    sys.exit(result.returncode)

# Đảm bảo import được backend
sys.path.insert(0, os.path.abspath(os.path.join(project_root, "backend")))
sys.stdout.reconfigure(encoding="utf-8")

from app.core.database import SessionLocal
from app.models.user import User
from app.models.parking_lot import ParkingLot
from app.models.parking_slot import ParkingSlot
from app.models.booking import Booking
from app.models.session import ParkingSession
from app.models.occupancy_history import OccupancyHistory

def show_summary():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        lots = db.query(ParkingLot).all()
        slots = db.query(ParkingSlot).all()
        bookings = db.query(Booking).all()
        sessions = db.query(ParkingSession).all()
        history = db.query(OccupancyHistory).count()

        print("=" * 80)
        print("          HỆ THỐNG CƠ SỞ DỮ LIỆU POSTGRESQL: parking_system")
        print("=" * 80)
        print(f"1. Bảng `users` (Tài khoản người dùng)       : {len(users)} bản ghi")
        print(f"2. Bảng `parking_lots` (Danh sách bãi xe)    : {len(lots)} bản ghi")
        print(f"3. Bảng `parking_slots` (Vị trí ô đỗ xe)    : {len(slots)} bản ghi")
        print(f"4. Bảng `bookings` (Vé đặt chỗ trước)        : {len(bookings)} bản ghi")
        print(f"5. Bảng `sessions` (Phiên xe gửi thực tế)    : {len(sessions)} bản ghi")
        print(f"6. Bảng `occupancy_history` (Lịch sử lấp đầy): {history} bản ghi (Dataset AI)")
        print("=" * 80)

        # In mẫu bảng users
        print("\n[+] MẪU DỮ LIỆU BẢNG `users` (Tài khoản hệ thống):")
        print(f"{'ID':<10} | {'Họ và tên':<24} | {'Email':<28} | {'Vai trò':<10} | {'Đơn vị công tác'}")
        print("-" * 105)
        for u in users[:6]:
            lot = u.assigned_lot or "Toàn hệ thống"
            print(f"{str(u.id)[:8]:<10} | {str(u.full_name or '')[:22]:<24} | {str(u.email)[:26]:<28} | {str(u.role.value):<10} | {lot}")

        # In mẫu bảng parking_lots
        print("\n[+] MẪU DỮ LIỆU BẢNG `parking_lots` (Các bãi xe):")
        print(f"{'ID':<10} | {'Tên bãi xe':<35} | {'Địa chỉ':<35} | {'Kích thước / Slots'}")
        print("-" * 105)
        for l in lots[:5]:
            slots_cnt = len(l.slots)
            print(f"{str(l.id)[:8]:<10} | {str(l.name)[:33]:<35} | {str(l.address or 'Hà Nội')[:33]:<35} | Lưới {l.grid_width}x{l.grid_height} ({slots_cnt} slots)")

        # In mẫu bảng sessions
        print("\n[+] MẪU DỮ LIỆU BẢNG `sessions` (Các phiên gửi xe thực tế gần nhất):")
        print(f"{'ID':<10} | {'Biển số xe':<16} | {'Slot ID':<10} | {'Trạng thái':<14} | {'Tổng tiền'}")
        print("-" * 75)
        for s in sessions[-5:]:
            fee = f"{int(s.total_fee or 0):,} đ" if s.total_fee else "0 đ (Đang đỗ)"
            plate = (s.vehicle.license_plate if s.vehicle else s.note) or "Xe vãng lai"
            print(f"{str(s.id)[:8]:<10} | {str(plate)[:14]:<16} | {str(s.slot_id)[:8]:<10} | {str(s.status.value):<14} | {fee}")

        print("=" * 80)
        print("=> Kết nối thành công tới PostgreSQL: localhost:5432/parking_system")
    except Exception as e:
        print("Lỗi kết nối cơ sở dữ liệu:", e)
    finally:
        db.close()

if __name__ == "__main__":
    show_summary()
