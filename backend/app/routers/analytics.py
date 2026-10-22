import csv
import io
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session as DbSession
from app.core.database import get_db
from app.models.session import ParkingSession, SessionStatus
from app.models.vehicle import Vehicle
from app.models.user import User, UserRole

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


class RevenueSummaryOut(BaseModel):
    today_revenue: int
    month_revenue: int
    total_revenue: int = 0
    parking_revenue: int = 0
    monthly_pass_revenue: int = 0
    today_parking_revenue: int = 0
    today_monthly_revenue: int = 0
    month_parking_revenue: int = 0
    month_monthly_revenue: int = 0
    total_sessions: int = 0
    total_monthly_passes: int = 0
    total_transactions: int = 0
    cashless_rate: int = 100
    daily_revenue: List[dict] = []
    payment_methods: dict = {}
    vehicle_types: dict = {}


class InvoiceRecord(BaseModel):
    id: str
    type: str  # 'session' | 'monthly_pass'
    type_label: str  # 'Vé gửi xe theo lượt' | 'Thuê bao vé tháng'
    plate: str
    owner_name: str
    phone: Optional[str] = None
    vehicle_type: str
    lot_name: str
    slot_code: Optional[str] = None
    start_time: str
    end_time: str
    duration_str: str
    amount: int
    payment_method: str
    status: str
    status_label: str
    staff_name: Optional[str] = None
    note: Optional[str] = None


class MonthlyPassCreate(BaseModel):
    plate: str
    owner_name: str
    phone: str
    vehicle_type: Optional[str] = "car"  # 'car', 'moto', 'ev'
    months: int = 1
    lot_id: Optional[str] = None
    lot_name: Optional[str] = None
    room_no: Optional[str] = None
    user_id: Optional[str] = None
    user_email: Optional[str] = None


class MonthlyPassOut(BaseModel):
    id: str
    plate: str
    owner_name: str
    phone: str
    vehicle_type: str
    months: int = 1
    fee: int
    status: str  # 'pending_payment', 'active', 'expired'
    created_at: str
    paid_at: Optional[str] = None
    start_date: Optional[str] = None
    expiry_date: Optional[str] = None
    lot_id: Optional[str] = None
    lot_name: Optional[str] = None
    room_no: Optional[str] = None
    user_id: Optional[str] = None
    user_email: Optional[str] = None


# File lưu trữ vé tháng bền vững trên ổ đĩa backend
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PASSES_FILE = DATA_DIR / "monthly_passes.json"

# Dữ liệu mẫu khởi tạo gồm cả 3 trạng thái: Đang hiệu lực, Đợi thanh toán, Đã hết hạn
# Vé tháng gắn với 1 bãi đỗ xe duy nhất (Mặc định: Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông))
DEFAULT_MONTHLY_PASSES: List[dict] = [
    {
        "id": "PASS-8801",
        "plate": "59A1-123.45",
        "owner_name": "Nguyễn Văn A",
        "phone": "0901234567",
        "user_email": "customer@parking.vn",
        "vehicle_type": "moto",
        "months": 12,
        "fee": 1800000,
        "status": "active",
        "created_at": "2026-09-15",
        "paid_at": "2026-09-15 08:30:00",
        "start_date": "2026-09-15",
        "expiry_date": "2027-12-31",
        "lot_id": "1",
        "lot_name": "Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông)",
        "room_no": None,
    },
    {
        "id": "PASS-8802",
        "plate": "89AB-55930",
        "owner_name": "Nguyễn Văn A",
        "phone": "0901234567",
        "user_email": "customer@parking.vn",
        "vehicle_type": "car",
        "months": 3,
        "fee": 3600000,
        "status": "pending_payment",  # Đợi khách thanh toán
        "created_at": "2026-10-06",
        "paid_at": None,
        "start_date": None,
        "expiry_date": None,
        "lot_id": "1",
        "lot_name": "Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông)",
        "room_no": None,
    },
    {
        "id": "PASS-8803",
        "plate": "30E-444.55",
        "owner_name": "Trần Thị B",
        "phone": "0912345678",
        "user_email": "tranthib@gmail.com",
        "vehicle_type": "car",
        "months": 1,
        "fee": 1200000,
        "status": "expired",  # Đã hết hạn -> chuyển tính cước giờ
        "created_at": "2026-08-01",
        "paid_at": "2026-08-01 10:00:00",
        "start_date": "2026-08-01",
        "expiry_date": "2026-09-01",
        "lot_id": "1",
        "lot_name": "Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông)",
        "room_no": None,
    }
]


def _load_passes_from_disk() -> List[dict]:
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if PASSES_FILE.exists():
            with open(PASSES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    return data
        with open(PASSES_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_MONTHLY_PASSES, f, ensure_ascii=False, indent=2)
        return list(DEFAULT_MONTHLY_PASSES)
    except Exception as e:
        print(f"Lỗi đọc monthly_passes từ đĩa: {e}")
        return list(DEFAULT_MONTHLY_PASSES)


def _save_passes_to_disk():
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(PASSES_FILE, "w", encoding="utf-8") as f:
            json.dump(MONTHLY_PASSES_STORE, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Lỗi ghi monthly_passes vào đĩa: {e}")


MONTHLY_PASSES_STORE: List[dict] = _load_passes_from_disk()


def _parse_pass_date(p: dict) -> Optional[datetime]:
    for key in ["paid_at", "start_date", "created_at"]:
        val = p.get(key)
        if val:
            try:
                s = str(val)[:10]
                return datetime.strptime(s, "%Y-%m-%d")
            except Exception:
                pass
    return None


@router.get("/revenue-summary", response_model=RevenueSummaryOut)
def get_revenue_summary(db: DbSession = Depends(get_db)):
    """
    Tính toán doanh thu thực tế từ cơ sở dữ liệu và hệ thống thuê bao vé tháng:
    - Tiền gửi xe theo lượt: Từ các ParkingSession đã hoàn tất check-out (giả định khách hàng đã thanh toán).
    - Tiền đóng vé tháng: Từ các thuê bao vé tháng của cư dân/khách hàng đã đóng.
    - Tổng doanh thu = Tiền gửi xe theo lượt + Tiền đóng vé tháng.
    """
    now = datetime.now()
    all_sessions = db.query(ParkingSession).all()
    completed = [s for s in all_sessions if s.status in [SessionStatus.COMPLETED, SessionStatus.completed]]
    
    # 1. Doanh thu tiền gửi xe theo lượt
    parking_total = sum(s.total_fee or 0 for s in completed)
    parking_today = sum(s.total_fee or 0 for s in completed if s.check_out_time and s.check_out_time.date() == now.date())
    parking_month = sum(s.total_fee or 0 for s in completed if s.check_out_time and s.check_out_time.month == now.month and s.check_out_time.year == now.year)

    # 2. Doanh thu tiền đóng vé tháng (active hoặc đã thanh toán hoặc expired đã từng đóng)
    paid_passes = [
        p for p in MONTHLY_PASSES_STORE
        if p.get("status") in ["active", "expired"] or p.get("paid_at")
    ]
    monthly_total = sum(p.get("fee") or 0 for p in paid_passes)

    monthly_today = 0
    monthly_month = 0
    for p in paid_passes:
        p_dt = _parse_pass_date(p)
        if p_dt:
            p_date = p_dt.date()
            if p_date == now.date():
                monthly_today += p.get("fee") or 0
            if p_date.month == now.month and p_date.year == now.year:
                monthly_month += p.get("fee") or 0

    # Tổng hợp
    total_revenue = parking_total + monthly_total
    today_revenue = parking_today + monthly_today
    month_revenue = parking_month + monthly_month
    total_transactions = len(completed) + len(paid_passes)
    total_sessions = len(all_sessions)

    # 7 ngày gần nhất (kết hợp cả gửi xe lượt và vé tháng)
    days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
    daily_revenue = []
    for i in range(7):
        d = now - timedelta(days=(6 - i))
        day_date = d.date()
        day_completed = [s for s in completed if s.check_out_time and s.check_out_time.date() == day_date]
        day_parking_amt = sum(s.total_fee or 0 for s in day_completed)
        day_passes = [p for p in paid_passes if _parse_pass_date(p) and _parse_pass_date(p).date() == day_date]
        day_pass_amt = sum(p.get("fee") or 0 for p in day_passes)

        daily_revenue.append({
            "day": days[d.weekday()],
            "date": d.strftime("%d/%m"),
            "amount": day_parking_amt + day_pass_amt,
            "parking_amount": day_parking_amt,
            "monthly_amount": day_pass_amt,
            "sessions": len(day_completed) + len(day_passes),
        })

    # Phân loại phương tiện kết hợp cả xe vào bãi và xe đăng ký vé tháng
    car_count = 0
    moto_count = 0
    ev_count = 0
    for s in all_sessions:
        if s.vehicle:
            vt = (s.vehicle.vehicle_type or "").lower()
            if "ev" in vt or "điện" in vt:
                ev_count += 1
            elif "moto" in vt or "máy" in vt:
                moto_count += 1
            else:
                car_count += 1

    for p in paid_passes:
        vt = (p.get("vehicle_type") or "").lower()
        if "ev" in vt or "điện" in vt:
            ev_count += 1
        elif "moto" in vt or "máy" in vt:
            moto_count += 1
        else:
            car_count += 1

    tot_v = car_count + moto_count + ev_count
    car_pct = round((car_count / tot_v) * 100) if tot_v > 0 else 0
    moto_pct = round((moto_count / tot_v) * 100) if tot_v > 0 else 0
    ev_pct = 100 - car_pct - moto_pct if tot_v > 0 else 0

    return RevenueSummaryOut(
        today_revenue=today_revenue,
        month_revenue=month_revenue,
        total_revenue=total_revenue,
        parking_revenue=parking_total,
        monthly_pass_revenue=monthly_total,
        today_parking_revenue=parking_today,
        today_monthly_revenue=monthly_today,
        month_parking_revenue=parking_month,
        month_monthly_revenue=monthly_month,
        total_sessions=total_sessions,
        total_monthly_passes=len(paid_passes),
        total_transactions=total_transactions,
        cashless_rate=95 if total_transactions > 0 else 0,
        daily_revenue=daily_revenue,
        payment_methods={
            "vietqr": 75 if total_transactions > 0 else 0,
            "momo": 20 if total_transactions > 0 else 0,
            "cash": 5 if total_transactions > 0 else 0,
        },
        vehicle_types={
            "car": car_pct,
            "moto": moto_pct,
            "ev": ev_pct,
        },
    )


def build_all_invoices(db: DbSession) -> List[InvoiceRecord]:
    """
    Xây dựng danh sách toàn bộ hóa đơn từ:
    1. Tiền đóng vé tháng cư dân / khách hàng.
    2. Tiền gửi xe theo lượt khi nhân viên xác nhận check-out (đã thu tiền).
    """
    invoices: List[InvoiceRecord] = []
    
    # 1. Thuê bao vé tháng
    paid_passes = [
        p for p in MONTHLY_PASSES_STORE
        if p.get("status") in ["active", "expired"] or p.get("paid_at")
    ]
    for p in paid_passes:
        v_type = p.get("vehicle_type") or "car"
        months = p.get("months", 1) or 1
        s_date = p.get("start_date") or p.get("created_at") or ""
        e_date = p.get("expiry_date") or ""
        p_id = p.get("id") or "PASS"
        invoices.append(
            InvoiceRecord(
                id=f"INV-{p_id}",
                type="monthly_pass",
                type_label="Thuê bao vé tháng",
                plate=p.get("plate", ""),
                owner_name=p.get("owner_name") or "Khách hàng",
                phone=p.get("phone"),
                vehicle_type=v_type,
                lot_name=p.get("lot_name") or "Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông)",
                slot_code=p.get("room_no") or "Vé tháng tự do",
                start_time=s_date,
                end_time=e_date,
                duration_str=f"{months} tháng",
                amount=p.get("fee") or 0,
                payment_method="VietQR Chuyển khoản",
                status="paid",
                status_label="Đã thanh toán",
                staff_name="Hệ thống / Admin",
                note=f"Thuê bao {months} tháng ({s_date} - {e_date})",
            )
        )

    # 2. Phiên gửi xe hoàn tất (khách hàng thanh toán khi checkout)
    completed_sessions = (
        db.query(ParkingSession)
        .filter(ParkingSession.status.in_([SessionStatus.COMPLETED, SessionStatus.completed]))
        .order_by(ParkingSession.check_out_time.desc().nullslast())
        .all()
    )
    for s in completed_sessions:
        plate = "N/A"
        owner_name = "Khách vãng lai"
        phone = None
        vtype = "car"

        if s.vehicle:
            if s.vehicle.license_plate:
                plate = s.vehicle.license_plate
            if s.vehicle.owner_name:
                owner_name = s.vehicle.owner_name
            if s.vehicle.owner_phone:
                phone = s.vehicle.owner_phone
            if s.vehicle.vehicle_type:
                vtype = str(getattr(s.vehicle.vehicle_type, "value", s.vehicle.vehicle_type)).lower()
        elif s.booking:
            if s.booking.vehicle:
                plate = s.booking.vehicle.license_plate
            if s.booking.user:
                owner_name = s.booking.user.full_name or s.booking.user.username
                phone = s.booking.user.phone

        lot_name = s.slot.lot.name if (s.slot and s.slot.lot) else "Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông)"
        slot_code = s.slot.slot_code if s.slot else "N/A"
        st_time = s.check_in_time.strftime("%d/%m/%Y %H:%M") if s.check_in_time else ""
        en_time = s.check_out_time.strftime("%d/%m/%Y %H:%M") if s.check_out_time else ""

        duration_str = "1 giờ"
        if s.check_in_time and s.check_out_time:
            diff_sec = int((s.check_out_time - s.check_in_time).total_seconds())
            hours = diff_sec // 3600
            minutes = (diff_sec % 3600) // 60
            if hours > 0:
                duration_str = f"{hours}h {minutes}p" if minutes > 0 else f"{hours}h"
            else:
                duration_str = f"{max(1, minutes)}p"

        staff_name = "Nhân viên bảo vệ"
        if s.check_out_staff:
            staff_name = s.check_out_staff.full_name or s.check_out_staff.username
        elif s.handled_by_staff:
            staff_name = s.handled_by_staff

        invoices.append(
            InvoiceRecord(
                id=f"INV-SESS-{str(s.id)[:8].upper()}",
                type="session",
                type_label="Vé gửi xe theo lượt",
                plate=plate,
                owner_name=owner_name,
                phone=phone,
                vehicle_type="moto" if "moto" in vtype or "máy" in vtype else ("ev" if "ev" in vtype or "điện" in vtype else "car"),
                lot_name=lot_name,
                slot_code=slot_code,
                start_time=st_time,
                end_time=en_time,
                duration_str=duration_str,
                amount=s.total_fee or 0,
                payment_method="VietQR Chuyển khoản",
                status="paid",
                status_label="Đã thanh toán",
                staff_name=staff_name,
                note=s.note or "Thanh toán lúc check-out",
            )
        )

    return invoices


@router.get("/invoices", response_model=List[InvoiceRecord])
def get_invoices(
    type: Optional[str] = None,
    db: DbSession = Depends(get_db),
):
    """
    Trả về toàn bộ danh sách hóa đơn thu tiền (gửi xe + vé tháng).
    """
    invoices = build_all_invoices(db)
    if type:
        clean_t = type.strip().lower()
        invoices = [inv for inv in invoices if inv.type.lower() == clean_t]
    return invoices


@router.get("/export-excel")
def export_excel_invoices(db: DbSession = Depends(get_db)):
    """
    Xuất file báo cáo doanh thu & hóa đơn dạng CSV chuẩn tiếng Việt (UTF-8 with BOM)
    tương thích hoàn toàn với Microsoft Excel.
    """
    now = datetime.now()
    invoices = build_all_invoices(db)

    output = io.StringIO()
    # Write UTF-8 BOM so Excel opens with correct encoding
    output.write("\ufeff")

    writer = csv.writer(output)
    writer.writerow(["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM"])
    writer.writerow(["HỆ THỐNG QUẢN LÝ BÃI ĐỖ XE THÔNG MINH - SMART PARKING SYSTEM"])
    writer.writerow([])
    writer.writerow(["BÁO CÁO DOANH THU VÀ BẢNG KÊ HÓA ĐƠN THU TIỀN TỔNG HỢP"])
    writer.writerow([f"Thời gian xuất báo cáo: {now.strftime('%d/%m/%Y %H:%M:%S')}"])
    
    total_amt = sum(inv.amount for inv in invoices)
    parking_amt = sum(inv.amount for inv in invoices if inv.type == "session")
    pass_amt = sum(inv.amount for inv in invoices if inv.type == "monthly_pass")
    
    writer.writerow([f"Tổng doanh thu: {total_amt:,} VNĐ".replace(",", ".")])
    writer.writerow([f"- Tiền gửi xe theo lượt: {parking_amt:,} VNĐ ({len([i for i in invoices if i.type == 'session'])} lượt)".replace(",", ".")])
    writer.writerow([f"- Tiền đóng vé tháng: {pass_amt:,} VNĐ ({len([i for i in invoices if i.type == 'monthly_pass'])} vé)".replace(",", ".")])
    writer.writerow([])

    # Table Header
    writer.writerow([
        "STT",
        "Mã Hóa Đơn",
        "Phân Loại",
        "Khách Hàng / Chủ Xe",
        "Số Điện Thoại",
        "Biển Số Xe",
        "Loại Xe",
        "Bãi Đỗ Xe",
        "Vị Trí Ô Đỗ",
        "Thời Gian Bắt Đầu",
        "Thời Gian Kết Thúc",
        "Thời Lượng / Thời Hạn",
        "Số Tiền (VNĐ)",
        "Hình Thức Thanh Toán",
        "Trạng Thái",
        "Nhân Viên Xác Nhận",
        "Ghi Chú",
    ])

    for idx, inv in enumerate(invoices, start=1):
        v_name = "Ô tô" if inv.vehicle_type == "car" else ("Xe máy" if inv.vehicle_type == "moto" else "Xe điện EV")
        writer.writerow([
            idx,
            inv.id,
            inv.type_label,
            inv.owner_name,
            inv.phone or "",
            inv.plate,
            v_name,
            inv.lot_name,
            inv.slot_code or "",
            inv.start_time,
            inv.end_time,
            inv.duration_str,
            inv.amount,
            inv.payment_method,
            inv.status_label,
            inv.staff_name or "",
            inv.note or "",
        ])

    writer.writerow([])
    writer.writerow([
        "TỔNG CỘNG",
        f"{len(invoices)} giao dịch",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        total_amt,
        "",
        "ĐÃ THANH TOÁN",
        "",
        "",
    ])

    csv_data = output.getvalue().encode("utf-8-sig")
    filename = f"Bao_Cao_Doanh_Thu_SmartParking_{now.strftime('%Y%m%d_%H%M%S')}.csv"

    return Response(
        content=csv_data,
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f"attachment; filename=\"{filename}\"",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.get("/monthly-passes", response_model=List[MonthlyPassOut])
def list_monthly_passes(
    user_id: Optional[str] = None,
    user_email: Optional[str] = None,
    plate: Optional[str] = None,
    phone: Optional[str] = None,
):
    """
    Trả về danh sách thuê bao vé tháng toàn hệ thống hoặc theo người dùng cụ thể.
    Tự động cập nhật nếu hết hạn và đồng bộ xuống đĩa.
    """
    now_date = datetime.now().date()
    changed = False
    for p in MONTHLY_PASSES_STORE:
        if p.get("status") == "active" and p.get("expiry_date"):
            try:
                exp_date = datetime.strptime(p["expiry_date"], "%Y-%m-%d").date()
                if now_date > exp_date:
                    p["status"] = "expired"
                    changed = True
            except Exception:
                pass
    if changed:
        _save_passes_to_disk()

    passes = MONTHLY_PASSES_STORE
    if user_id:
        passes = [p for p in passes if p.get("user_id") and str(p.get("user_id")) == str(user_id)]
    elif user_email:
        clean_em = user_email.strip().lower()
        passes = [p for p in passes if p.get("user_email") and p.get("user_email").strip().lower() == clean_em]
    elif plate:
        clean_p = normalize_plate(plate)
        passes = [p for p in passes if normalize_plate(p.get("plate", "")) == clean_p]
    elif phone:
        clean_phone = re.sub(r"\D", "", phone)
        passes = [p for p in passes if p.get("phone") and re.sub(r"\D", "", p.get("phone")) == clean_phone]

    return passes


@router.post("/monthly-passes", response_model=MonthlyPassOut, status_code=201)
def add_monthly_pass(payload: MonthlyPassCreate, db: Optional[DbSession] = Depends(get_db)):
    """
    Admin hoặc hệ thống đăng ký vé tháng cho khách hàng.
    Tự động dò tìm tài khoản khách hàng qua SĐT / Biển số / Họ tên để gắn user_id và user_email.
    Lưu bền vững vào file JSON trên ổ cứng, không bao giờ bị mất khi restart server.
    """
    now = datetime.now()
    clean_plate = payload.plate.strip().upper()
    fee = (150000 if (payload.vehicle_type or "").lower() == "moto" else 1200000) * payload.months

    clean_user_id = payload.user_id
    clean_user_email = payload.user_email

    # Tự động dò tìm khách hàng trong DB nếu chưa được truyền
    session = None
    should_close = False
    if db is not None:
        session = db
    else:
        try:
            from app.core.database import SessionLocal
            session = SessionLocal()
            should_close = True
        except Exception:
            session = None

    if session:
        try:
            clean_digits = re.sub(r"\D", "", payload.phone or "")
            # 1. Tìm user theo số điện thoại
            if not clean_user_email and clean_digits:
                users = session.query(User).all()
                for u in users:
                    if u.phone and re.sub(r"\D", "", u.phone) == clean_digits:
                        clean_user_id = clean_user_id or str(u.id)
                        clean_user_email = clean_user_email or u.email
                        break

            # 2. Tìm user theo biển số xe đã đăng ký trong hệ thống
            if not clean_user_email and clean_plate:
                norm_p = normalize_plate(clean_plate)
                vehs = session.query(Vehicle).all()
                for v in vehs:
                    if normalize_plate(v.license_plate) == norm_p and v.user_id:
                        u = session.query(User).filter(User.id == v.user_id).first()
                        if u:
                            clean_user_id = clean_user_id or str(u.id)
                            clean_user_email = clean_user_email or u.email
                            break

            # 3. Tìm user theo họ tên khách hàng
            if not clean_user_email and payload.owner_name:
                name_str = payload.owner_name.strip().lower()
                u = session.query(User).filter(User.role == UserRole.customer, func.lower(User.full_name) == name_str).first()
                if u:
                    clean_user_id = clean_user_id or str(u.id)
                    clean_user_email = clean_user_email or u.email
        except Exception as e:
            print(f"Lỗi dò tìm khách hàng: {e}")
        finally:
            if should_close:
                session.close()

    # Tạo ID duy nhất không trùng lặp
    existing_ids = {p.get("id") for p in MONTHLY_PASSES_STORE}
    counter = len(MONTHLY_PASSES_STORE) + 8801
    while f"PASS-{counter}" in existing_ids:
        counter += 1
    new_id = f"PASS-{counter}"

    new_pass = {
        "id": new_id,
        "plate": clean_plate,
        "owner_name": payload.owner_name.strip(),
        "phone": payload.phone.strip(),
        "user_id": clean_user_id,
        "user_email": clean_user_email,
        "vehicle_type": payload.vehicle_type or "car",
        "months": payload.months,
        "fee": fee,
        "status": "pending_payment",  # Đợi khách thanh toán
        "created_at": now.strftime("%Y-%m-%d"),
        "paid_at": None,
        "start_date": None,  # Sẽ có hiệu lực từ lúc thanh toán
        "expiry_date": None,
        "lot_id": payload.lot_id or "1",
        "lot_name": payload.lot_name or "Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông)",
        "room_no": None,
    }
    MONTHLY_PASSES_STORE.insert(0, new_pass)
    _save_passes_to_disk()
    return new_pass


@router.post("/monthly-passes/{pass_id}/pay", response_model=MonthlyPassOut)
def pay_monthly_pass(pass_id: str):
    """
    Khách hàng hoặc Admin thực hiện thanh toán vé tháng.
    Vé tháng chuyển sang 'active', thời gian hiệu lực bắt đầu tính từ thời điểm thanh toán.
    Đồng bộ cập nhật ngay lập tức vào file lưu trữ trên đĩa.
    """
    target = None
    for p in MONTHLY_PASSES_STORE:
        if p["id"] == pass_id:
            target = p
            break
    if not target:
        raise HTTPException(status_code=404, detail="Không tìm thấy vé tháng")

    now = datetime.now()
    months = target.get("months", 1) or 1
    exp = now + timedelta(days=30 * months)

    target["paid_at"] = now.strftime("%Y-%m-%d %H:%M:%S")
    target["start_date"] = now.strftime("%Y-%m-%d")
    target["expiry_date"] = exp.strftime("%Y-%m-%d")
    target["status"] = "active"
    _save_passes_to_disk()
    return target


import re


def normalize_plate(plate: str) -> str:
    if not plate:
        return ""
    return re.sub(r"[^A-Z0-9]", "", plate.strip().upper())


@router.get("/monthly-passes/check/{plate}")
def check_monthly_pass_by_plate(
    plate: str,
    lot_id: Optional[str] = None,
    lot_name: Optional[str] = None,
):
    """
    Kiểm tra biển số xe có vé tháng hợp lệ không:
    - Vé tháng áp dụng theo 1 bãi đỗ xe duy nhất đã đăng ký.
    - Đúng bãi & còn hạn: Miễn phí đỗ xe (0 VNĐ).
    - Khác bãi: Cảnh báo xe có vé tháng ở bãi khác, tính cước giờ vãng lai (30.000 VNĐ/h).
    - Hết hạn hoặc Đợi thanh toán: Tính tiền theo giờ thực tế.
    """
    norm_query = normalize_plate(plate)
    now_date = datetime.now().date()

    for p in MONTHLY_PASSES_STORE:
        if normalize_plate(p.get("plate", "")) == norm_query:
            if p.get("status") == "active" and p.get("expiry_date"):
                try:
                    exp_date = datetime.strptime(p["expiry_date"], "%Y-%m-%d").date()
                    if now_date <= exp_date:
                        # Kiểm tra xem có trùng bãi đỗ xe đã đăng ký không
                        is_match_lot = True
                        p_lot_id = str(p.get("lot_id") or "").strip()
                        p_lot_name = str(p.get("lot_name") or "").strip().lower()

                        if lot_id or lot_name:
                            match_by_id = bool(lot_id and p_lot_id and str(lot_id).strip() == p_lot_id)
                            match_by_name = False
                            if lot_name and p_lot_name:
                                def _clean_tokens(text: str) -> set:
                                    t = re.sub(r"[^a-zA-Z0-9\u00C0-\u1EF9]", " ", text.lower())
                                    stop_words = {"bãi", "xe", "đỗ", "kđt", "kdt", "tp", "quận", "phường"}
                                    return {w for w in t.split() if w and w not in stop_words}
                                cur_tokens = _clean_tokens(lot_name)
                                pass_tokens = _clean_tokens(p_lot_name)
                                clean_cur = lot_name.strip().lower()
                                match_by_name = (
                                    clean_cur == p_lot_name
                                    or clean_cur in p_lot_name
                                    or p_lot_name in clean_cur
                                    or bool(cur_tokens and cur_tokens.issubset(pass_tokens))
                                    or bool(pass_tokens and pass_tokens.issubset(cur_tokens))
                                    or bool(cur_tokens and pass_tokens and len(cur_tokens & pass_tokens) >= 2)
                                )
                            
                            is_match_lot = match_by_id or match_by_name or (not p_lot_id and not p_lot_name)

                        if not is_match_lot:
                            registered_lot = p.get("lot_name") or f"Bãi #{p_lot_id}"
                            current_lot = lot_name or f"Bãi #{lot_id}"
                            return {
                                "has_valid_pass": False,
                                "is_free": False,
                                "is_wrong_lot": True,
                                "status": "wrong_lot",
                                "registered_lot_name": registered_lot,
                                "current_lot_name": current_lot,
                                "message": f"Vé tháng của xe {p['plate']} chỉ có hiệu lực tại '{registered_lot}'. Tại bãi hiện tại ('{current_lot}'), xe được tính cước vãng lai theo giờ (30.000 VNĐ/h).",
                                "pass": p
                            }

                        return {
                            "has_valid_pass": True,
                            "is_free": True,
                            "is_wrong_lot": False,
                            "status": "active",
                            "registered_lot_name": p.get("lot_name"),
                            "message": f"Xe {p['plate']} có vé tháng VIP hợp lệ tại '{p.get('lot_name') or 'bãi này'}' (Miễn phí đỗ xe 0đ).",
                            "pass": p
                        }
                    else:
                        p["status"] = "expired"
                        _save_passes_to_disk()
                        return {
                            "has_valid_pass": False,
                            "is_expired": True,
                            "is_free": False,
                            "status": "expired",
                            "message": f"Vé tháng của xe {p['plate']} đã hết hạn vào ngày {p['expiry_date']}. Tính tiền theo thời gian đỗ thực tế.",
                            "pass": p
                        }
                except Exception:
                    pass
            elif p.get("status") == "pending_payment":
                return {
                    "has_valid_pass": False,
                    "is_pending_payment": True,
                    "is_free": False,
                    "status": "pending_payment",
                    "message": f"Vé tháng của xe {p['plate']} đang đợi thanh toán. Tính cước theo thời gian thực tế.",
                    "pass": p
                }
            elif p.get("status") == "expired":
                return {
                    "has_valid_pass": False,
                    "is_expired": True,
                    "is_free": False,
                    "status": "expired",
                    "message": f"Vé tháng của xe {p['plate']} đã hết hạn. Tính tiền theo thời gian đỗ thực tế.",
                    "pass": p
                }

    return {
        "has_valid_pass": False,
        "is_free": False,
        "status": "none",
        "message": "Không có vé tháng. Tính cước theo thời gian thực tế."
    }


