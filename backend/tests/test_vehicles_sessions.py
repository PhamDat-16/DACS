"""
Unit test kiểm tra ORM models và logic nghiệp vụ của Vehicles và Sessions
Chạy: pytest tests/test_vehicles_sessions.py -v
"""

from datetime import datetime, timezone
import uuid

from app.models.user import User, UserRole
from app.models.vehicle import Vehicle, VehicleType
from app.models.parking_lot import ParkingLot
from app.models.parking_slot import ParkingSlot, SlotStatus
from app.models.session import ParkingSession, SessionStatus
from app.schemas.vehicle import VehicleCreate, VehicleOut
from app.schemas.session import CheckInRequest, SessionOut


def test_vehicle_schema_validation():
    payload = {
        "license_plate": "30A-999.88",
        "vehicle_type": "car",
        "brand": "VinFast VF9",
        "color": "Xanh Dương",
        "owner_name": "Trần Văn B",
        "owner_phone": "0912345678",
    }
    vc = VehicleCreate(**payload)
    assert vc.license_plate == "30A-999.88"
    assert vc.vehicle_type == VehicleType.car
    assert vc.brand == "VinFast VF9"


def test_session_status_and_defaults():
    now = datetime.now(timezone.utc)
    sess = ParkingSession(
        slot_id=uuid.uuid4(),
        check_in_time=now,
        status=SessionStatus.PARKING,
        total_fee=0,
        note="Thử nghiệm",
    )
    assert sess.status == SessionStatus.PARKING
    assert sess.total_fee == 0
    assert sess.note == "Thử nghiệm"


def test_customer_parking_history_isolation():
    from app.core.database import SessionLocal
    from app.routers.sessions import get_my_sessions, get_sessions

    db = SessionLocal()
    try:
        # Create test users
        u_cust1 = db.query(User).filter(User.email == "customer@parking.vn").first()
        u_admin = db.query(User).filter(User.role == UserRole.admin).first()
        assert u_cust1 is not None
        assert u_admin is not None

        # Call get_my_sessions for customer 1
        sessions_cust1 = get_my_sessions(current_user=u_cust1, db=db)
        # Check that all returned sessions belong to customer 1's vehicles or bookings
        cust1_veh_ids = [v.id for v in db.query(Vehicle.id).filter(Vehicle.user_id == u_cust1.id).all()]
        for s in sessions_cust1:
            assert s.vehicle_id in cust1_veh_ids or s.vehicle_id is None

        # Call get_sessions as customer 1 (should be isolated)
        cust1_all_view = get_sessions(current_user=u_cust1, db=db)
        for s in cust1_all_view:
            assert s.vehicle_id in cust1_veh_ids or s.vehicle_id is None

        # Call get_sessions as admin (can see all)
        admin_all_view = get_sessions(current_user=u_admin, db=db)
        total_in_db = db.query(ParkingSession).count()
        assert len(admin_all_view) == total_in_db
    finally:
        db.close()

