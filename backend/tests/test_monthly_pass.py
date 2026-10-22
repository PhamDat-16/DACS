import pytest
import uuid
from datetime import datetime, timedelta, timezone
from app.routers.analytics import normalize_plate, MONTHLY_PASSES_STORE, check_monthly_pass_by_plate
from app.services.session_service import check_in, check_out
from app.core.database import SessionLocal, engine, Base
from app.models.parking_slot import ParkingSlot, SlotStatus
from app.models.parking_lot import ParkingLot
from app.models.vehicle import Vehicle
from app.models.user import User, UserRole
from app.models.session import ParkingSession, SessionStatus
from app.core.security import hash_password

def test_normalize_plate():
    assert normalize_plate("59A1-123.45") == "59A112345"
    assert normalize_plate("59a1.123.45") == "59A112345"
    assert normalize_plate("  30E - 444.55  ") == "30E44455"
    assert normalize_plate("89AB-55930") == "89AB55930"

def test_monthly_pass_data_lookup():
    # Ensure PASS-8801 for 59A1-123.45 is active with future expiry and registered at lot 1
    for p in MONTHLY_PASSES_STORE:
        if normalize_plate(p.get("plate", "")) == "59A112345":
            p["status"] = "active"
            p["expiry_date"] = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
            p["lot_id"] = "1"
            p["lot_name"] = "Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông)"
        elif normalize_plate(p.get("plate", "")) == "30E44455":
            p["status"] = "expired"
            p["expiry_date"] = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    # 59A1-123.45 is registered at lot 1 / 'Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông)'
    res_correct_lot = check_monthly_pass_by_plate("59A1-123.45", lot_id="1")
    assert res_correct_lot["has_valid_pass"] is True
    assert res_correct_lot["is_free"] is True
    assert res_correct_lot["status"] == "active"
    
    # 59A1-123.45 looked up at lot 2 -> wrong_lot
    res_wrong_lot = check_monthly_pass_by_plate("59A1-123.45", lot_id="2", lot_name="Bãi Xe Khác")
    assert res_wrong_lot["has_valid_pass"] is False
    assert res_wrong_lot["is_free"] is False
    assert res_wrong_lot["is_wrong_lot"] is True
    assert res_wrong_lot["status"] == "wrong_lot"
    
    # 30E-444.55 is expired in MONTHLY_PASSES_STORE
    res_exp = check_monthly_pass_by_plate("30E-444.55", lot_id="1")
    assert res_exp["has_valid_pass"] is False
    assert res_exp["is_free"] is False
    assert res_exp["status"] == "expired"

    # Non-existent plate
    res_none = check_monthly_pass_by_plate("99Z-999.99", lot_id="1")
    assert res_none["has_valid_pass"] is False
    assert res_none["is_free"] is False
    assert res_none["status"] == "none"

def test_monthly_pass_checkin_and_checkout_flow():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    slot = None
    try:
        # Create or find a test staff user
        staff = db.query(User).filter(User.role == UserRole.staff).first()
        if not staff:
            staff = User(
                email="staff_test_monthly@parking.vn",
                password_hash=hash_password("123456"),
                full_name="Staff Monthly Tester",
                role=UserRole.staff
            )
            db.add(staff)
            db.commit()
            db.refresh(staff)

        # Create or find a test lot matching pass registered lot ('1' or 'Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông)')
        lot = db.query(ParkingLot).filter(ParkingLot.name.like("%Đô Nghĩa%")).first()
        if not lot:
            lot = ParkingLot(name="Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông)", grid_width=2, grid_height=2)
            db.add(lot)
            db.flush()

        # Create or reuse a test slot
        slot = db.query(ParkingSlot).filter(ParkingSlot.slot_code == "VIP-TEST-01").first()
        if not slot:
            slot = ParkingSlot(
                lot_id=lot.id,
                slot_code="VIP-TEST-01",
                pos_x=0,
                pos_y=0,
                status=SlotStatus.available
            )
            db.add(slot)
            db.commit()
            db.refresh(slot)
        else:
            slot.lot_id = lot.id
            slot.status = SlotStatus.available
            db.commit()

        # Clean existing sessions for test plate
        test_plate = "59A1-123.45"
        veh = db.query(Vehicle).filter(Vehicle.license_plate == test_plate).first()
        if veh:
            open_sessions = db.query(ParkingSession).filter(
                ParkingSession.vehicle_id == veh.id,
                ParkingSession.status == SessionStatus.PARKING
            ).all()
            for s in open_sessions:
                s.status = SessionStatus.COMPLETED
            db.commit()

        # Ensure monthly pass for test plate is active and points to registered lot
        for p in MONTHLY_PASSES_STORE:
            if normalize_plate(p.get("plate", "")) == normalize_plate(test_plate):
                p["status"] = "active"
                p["expiry_date"] = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
                p["lot_id"] = str(lot.id)
                p["lot_name"] = lot.name

        # 1. Check-in directly without booking at Registered Lot (Monthly Pass Active)
        session_out = check_in(
            db=db,
            staff=staff,
            license_plate=test_plate,
            slot_id=slot.id,
            slot_code=slot.slot_code
        )
        assert session_out is not None
        assert session_out.total_fee == 0
        assert "VIP" in (session_out.note or "")
        
        # Verify slot is occupied
        db.refresh(slot)
        assert slot.status == SlotStatus.occupied

        # 2. Check-out (Monthly Pass Active -> total_fee = 0)
        completed_session = check_out(
            db=db,
            staff=staff,
            session_id=session_out.id,
            license_plate=test_plate
        )
        assert completed_session is not None
        assert completed_session.total_fee == 0
        assert completed_session.status == SessionStatus.COMPLETED

        # Verify slot is freed to available
        db.refresh(slot)
        assert slot.status == SlotStatus.available

        # 3. Test list_sessions returns 0 fee for monthly pass vehicle
        from app.routers.sessions import get_sessions
        session_list = get_sessions(current_user=staff, db=db)
        target = next((s for s in session_list if s.id == session_out.id), None)
        assert target is not None
        assert target.total_fee == 0
        assert target.slot_code == "VIP-TEST-01"

        # 4. Test parking at WRONG lot -> charges standard fee
        other_lot = db.query(ParkingLot).filter(ParkingLot.id != lot.id).first()
        if not other_lot:
            other_lot = ParkingLot(name="Bãi Khác Khác Hà Đông", grid_width=2, grid_height=2)
            db.add(other_lot)
            db.flush()
        
        slot.lot_id = other_lot.id
        slot.status = SlotStatus.available
        db.commit()

        session_wrong_lot = check_in(
            db=db,
            staff=staff,
            license_plate=test_plate,
            slot_id=slot.id,
            slot_code=slot.slot_code
        )
        assert session_wrong_lot is not None
        assert "tính cước vãng lai" in (session_wrong_lot.note or "")

        # Checkout wrong lot (mock checkin 2 hours ago)
        session_obj = db.query(ParkingSession).filter(ParkingSession.id == session_wrong_lot.id).first()
        session_obj.check_in_time = datetime.now(timezone.utc) - timedelta(hours=2)
        db.commit()

        checkout_wrong_lot = check_out(
            db=db,
            staff=staff,
            session_id=session_wrong_lot.id,
            license_plate=test_plate
        )
        assert checkout_wrong_lot.total_fee > 0
        assert checkout_wrong_lot.status == SessionStatus.COMPLETED

    finally:
        if slot:
            db.query(ParkingSession).filter(ParkingSession.slot_id == slot.id).delete()
            db.query(ParkingSlot).filter(ParkingSlot.id == slot.id).delete()
            db.commit()
        db.close()


def test_duplicate_checkin_prevention():
    """
    Kiểm tra ngăn chặn check-in trùng lặp:
    Khi xe đang trong phiên đỗ chưa check-out, hệ thống chặn check-in thêm phiên mới.
    """
    import pytest
    from fastapi import HTTPException

    db = SessionLocal()
    slot = None
    slot2 = None
    try:
        staff = db.query(User).filter(User.role == UserRole.staff).first()
        if not staff:
            from app.core.security import hash_password
            staff = User(
                email="staff_test_dup@parking.vn",
                password_hash=hash_password("123456"),
                full_name="Staff Test Dup",
                role=UserRole.staff
            )
            db.add(staff)
            db.commit()
            db.refresh(staff)

        lot = db.query(ParkingLot).first()
        if not lot:
            lot = ParkingLot(name="Bãi Đỗ Xe Test", grid_width=2, grid_height=2)
            db.add(lot)
            db.commit()
            db.refresh(lot)

        slot = ParkingSlot(lot_id=lot.id, slot_code="DUP-01", pos_x=0, pos_y=0, status=SlotStatus.available)
        slot2 = ParkingSlot(lot_id=lot.id, slot_code="DUP-02", pos_x=1, pos_y=0, status=SlotStatus.available)
        db.add(slot)
        db.add(slot2)
        db.commit()

        test_plate = "30G-999.99"
        # 1. Check-in lần đầu thành công
        s1 = check_in(db=db, staff=staff, license_plate=test_plate, slot_id=slot.id)
        assert s1 is not None
        assert s1.status == SessionStatus.PARKING

        # 2. Thử check-in lần hai với cùng biển số (kể cả viết cách hoặc không dấu gạch ngang) -> Bị chặn 400
        with pytest.raises(HTTPException) as excinfo:
            check_in(db=db, staff=staff, license_plate="30G99999", slot_id=slot2.id)
        assert excinfo.value.status_code == 400
        assert "chưa thực hiện check-out" in excinfo.value.detail

        # 3. Check-out phiên đầu
        check_out(db=db, staff=staff, session_id=s1.id, license_plate=test_plate)

        # 4. Sau khi check-out xong, check-in lại được thành công
        s2 = check_in(db=db, staff=staff, license_plate=test_plate, slot_id=slot2.id)
        assert s2 is not None
        assert s2.status == SessionStatus.PARKING
    finally:
        slot_ids = []
        if slot: slot_ids.append(slot.id)
        if slot2: slot_ids.append(slot2.id)
        if slot_ids:
            db.query(ParkingSession).filter(ParkingSession.slot_id.in_(slot_ids)).delete()
            db.query(ParkingSlot).filter(ParkingSlot.id.in_(slot_ids)).delete()
            db.commit()
        db.close()


