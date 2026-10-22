"""
Test mô phỏng tình huống double-booking: 2 "khách" cùng cố đặt 1 slot gần như
đồng thời bằng 2 thread riêng biệt (mỗi thread có DB session riêng, giống hệt
2 request HTTP thật đến server cùng lúc).

Chạy: (đứng trong thư mục backend/, đã activate venv, đã có DB + đã migrate)
    pytest tests/test_double_booking.py -v -s

Kỳ vọng: đúng 1 trong 2 thread đặt thành công (status 200), thread còn lại
nhận lỗi 409 Conflict - không bao giờ có trường hợp cả 2 cùng thành công.
"""

import threading
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException

from app.core.database import SessionLocal
from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.parking_lot import ParkingLot
from app.models.parking_slot import ParkingSlot, SlotStatus
from app.models.booking import Booking
from app.core.security import hash_password
from app.schemas.booking import BookingCreate
from app.services.booking_service import create_booking


@pytest.fixture
def sample_slot():
    """Tạo sẵn 2 user + 1 lot + 1 slot trống để 2 user cùng tranh nhau đặt."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    lot = ParkingLot(name="Test Lot", grid_width=2, grid_height=2)
    db.add(lot)
    db.flush()

    slot = ParkingSlot(lot_id=lot.id, slot_code="A1", pos_x=0, pos_y=0, status=SlotStatus.available)
    db.add(slot)

    user_a = User(email="racer_a@test.com", password_hash=hash_password("123456"), full_name="Racer A")
    user_b = User(email="racer_b@test.com", password_hash=hash_password("123456"), full_name="Racer B")
    db.add_all([user_a, user_b])

    db.commit()
    db.refresh(slot)
    db.refresh(user_a)
    db.refresh(user_b)

    yield slot, user_a, user_b

    # Dọn dẹp sau khi test xong
    db.query(Booking).filter(Booking.slot_id == slot.id).delete()
    db.query(ParkingSlot).filter(ParkingSlot.id == slot.id).delete()
    db.query(ParkingLot).filter(ParkingLot.id == lot.id).delete()
    db.query(User).filter(User.id.in_([user_a.id, user_b.id])).delete(synchronize_session=False)
    db.commit()
    db.close()


def test_only_one_booking_wins(sample_slot):
    slot, user_a, user_b = sample_slot
    results = {}

    def attempt_booking(user_key: str, user: User):
        # Mỗi thread PHẢI có DB session riêng - đây là điều kiện bắt buộc để
        # mô phỏng đúng 2 transaction độc lập như 2 request HTTP thật.
        db = SessionLocal()
        try:
            payload = BookingCreate(
                slot_id=slot.id,
                start_time=datetime.now(timezone.utc),
                end_time=datetime.now(timezone.utc) + timedelta(hours=2),
            )
            booking, _qr = create_booking(db, user, payload)
            results[user_key] = ("SUCCESS", booking.id)
        except HTTPException as e:
            results[user_key] = ("FAILED", e.status_code)
        finally:
            db.close()

    t1 = threading.Thread(target=attempt_booking, args=("A", user_a))
    t2 = threading.Thread(target=attempt_booking, args=("B", user_b))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print("Kết quả:", results)

    outcomes = [v[0] for v in results.values()]
    assert outcomes.count("SUCCESS") == 1, "Phải có ĐÚNG 1 booking thành công, không được cả 2 hoặc 0"
    assert outcomes.count("FAILED") == 1, "Người thua cuộc phải nhận lỗi rõ ràng (409), không phải im lặng"
