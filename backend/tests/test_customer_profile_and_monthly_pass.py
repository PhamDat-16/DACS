from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import hash_password
from app.schemas.user import ProfileUpdate
from app.routers.users import update_current_user
from app.routers.analytics import list_monthly_passes, add_monthly_pass, MonthlyPassCreate

def test_customer_profile_update_and_persistence():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "customer@parking.vn").first()
        if not user:
            user = User(
                email="customer@parking.vn",
                password_hash=hash_password("123456"),
                full_name="Khách Hàng Ban Đầu",
                phone="0901111111",
                role=UserRole.customer,
                status="active"
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        user_id = user.id

        # 1. Update Profile via router endpoint update_current_user
        new_name = "Nguyễn Văn Đạt (Đã Cập Nhật)"
        new_phone = "0988999888"
        payload = ProfileUpdate(full_name=new_name, phone=new_phone)
        updated_res = update_current_user(payload=payload, current_user=user, db=db)

        assert updated_res.full_name == new_name
        assert updated_res.phone == new_phone

        # 2. Check directly in PostgreSQL database after reload
        db.expire_all()
        reloaded = db.query(User).filter(User.id == user_id).first()
        assert reloaded.full_name == new_name
        assert reloaded.phone == new_phone

    finally:
        db.close()

def test_monthly_pass_customer_isolation():
    email_a = "customer@parking.vn"
    email_b = "customer_b_test@parking.vn"

    # Add monthly pass for User B
    create_payload = MonthlyPassCreate(
        plate="29A-777.88",
        owner_name="Người Dùng B",
        phone="0911222333",
        vehicle_type="car",
        months=1,
        user_email=email_b,
        lot_id="1",
        lot_name="Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông)"
    )
    pass_b = add_monthly_pass(create_payload)
    assert pass_b.get("user_email") == email_b

    # User A listing their monthly passes MUST NOT see User B's pass
    passes_a = list_monthly_passes(user_email=email_a)
    for p in passes_a:
        assert p.get("user_email") != email_b, "User A must NOT see User B's pass!"
        assert p.get("plate") != "29A-777.88", "User A must NOT see User B's vehicle!"

    # User B listing their monthly passes ONLY sees User B's passes
    passes_b = list_monthly_passes(user_email=email_b)
    assert len(passes_b) >= 1
    for p in passes_b:
        assert p.get("user_email") == email_b

def test_customer_vehicle_persistence():
    from starlette.requests import Request
    from app.schemas.vehicle import VehicleCreate
    from app.routers.vehicles import create_vehicle, get_vehicles
    from app.models.vehicle import Vehicle

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "customer@parking.vn").first()
        assert user is not None

        test_plate = "30H-999.88"
        # Clean up if exists
        existing = db.query(Vehicle).filter(Vehicle.license_plate == test_plate).first()
        if existing:
            db.delete(existing)
            db.commit()

        # Mock dummy request
        scope = {"type": "http", "headers": []}
        req = Request(scope)

        # 1. Customer adds vehicle
        payload = VehicleCreate(
            license_plate=test_plate,
            vehicle_type="car",
            brand="VinFast VF8",
            color="Đỏ Ruby",
            owner_name=user.full_name,
            owner_phone=user.phone,
            user_id=user.id
        )
        created = create_vehicle(payload=payload, request=req, db=db)
        assert created.license_plate == test_plate
        assert created.user_id == user.id

        # 2. Check directly in database
        db.expire_all()
        db_veh = db.query(Vehicle).filter(Vehicle.license_plate == test_plate).first()
        assert db_veh is not None
        assert db_veh.user_id == user.id

        # 3. Simulate logging in again -> loadCustomerVehicles() calling GET /api/vehicles?user_id=...
        loaded_list = get_vehicles(request=req, user_id=user.id, db=db)
        plates = [v.license_plate for v in loaded_list]
        assert test_plate in plates, "Newly added vehicle MUST be found when user logs back in!"

        # 4. Clean up test vehicle
        db.delete(db_veh)
        db.commit()
    finally:
        db.close()


def test_revenue_calculation_and_excel_export():
    from app.routers.analytics import get_revenue_summary, get_invoices, export_excel_invoices

    db = SessionLocal()
    try:
        summary = get_revenue_summary(db=db)
        assert summary.total_revenue == summary.parking_revenue + summary.monthly_pass_revenue
        assert summary.total_revenue > 0
        assert summary.monthly_pass_revenue > 0

        # Verify invoices
        invoices = get_invoices(db=db)
        assert len(invoices) > 0
        types = {inv.type for inv in invoices}
        assert "monthly_pass" in types

        # Verify Excel / CSV export
        export_resp = export_excel_invoices(db=db)
        assert export_resp.status_code == 200
        assert export_resp.media_type.startswith("text/csv")
        content = export_resp.body.decode("utf-8-sig")
        assert "BÁO CÁO DOANH THU" in content
        assert "Tổng doanh thu:" in content
        assert "Mã Hóa Đơn" in content
    finally:
        db.close()


def test_monthly_pass_disk_persistence_and_reload():
    from app.routers.analytics import (
        add_monthly_pass,
        pay_monthly_pass,
        list_monthly_passes,
        MonthlyPassCreate,
        _load_passes_from_disk,
        PASSES_FILE,
        MONTHLY_PASSES_STORE,
    )
    import json

    db = SessionLocal()
    try:
        # Create user if needed
        user = db.query(User).filter(User.email == "customer@parking.vn").first()
        assert user is not None

        test_plate = "51K-888.99"
        create_payload = MonthlyPassCreate(
            plate=test_plate,
            owner_name="Khách Hàng Ban Đầu",
            phone=user.phone or "0901111111",
            vehicle_type="car",
            months=2,
            lot_id="1",
            lot_name="Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông)"
        )
        new_pass = add_monthly_pass(create_payload, db=db)
        pass_id = new_pass["id"]

        # Verify auto user lookup by phone or name
        assert new_pass.get("user_email") == user.email, "Pass must automatically link to customer email!"
        assert new_pass.get("user_id") == str(user.id), "Pass must automatically link to customer id!"

        # Pay pass
        paid_pass = pay_monthly_pass(pass_id)
        assert paid_pass["status"] == "active"
        assert paid_pass["start_date"] is not None
        assert paid_pass["expiry_date"] is not None

        # Verify physical file existence and content
        assert PASSES_FILE.exists(), "monthly_passes.json MUST exist on disk!"
        with open(PASSES_FILE, "r", encoding="utf-8") as f:
            disk_data = json.load(f)
        disk_plates = [p.get("plate") for p in disk_data]
        assert test_plate in disk_plates, "Pass must be stored in monthly_passes.json on disk!"

        # SIMULATE FULL SERVER RESTART / MODULE RELOAD
        reloaded_passes = _load_passes_from_disk()
        reloaded_match = next((p for p in reloaded_passes if p["id"] == pass_id), None)
        assert reloaded_match is not None, "Pass MUST survive server restarts and reloads!"
        assert reloaded_match["status"] == "active"
        assert reloaded_match["user_email"] == user.email

        # Verify customer can list their active pass
        cust_passes = list_monthly_passes(user_email=user.email)
        cust_plates = [p.get("plate") for p in cust_passes]
        assert test_plate in cust_plates, "Customer must see their monthly pass after restart!"

    finally:
        db.close()



