from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DbSession  # alias để không đụng ParkingSession

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut, Token, ResetPasswordRequest

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: DbSession = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email đã được đăng ký")

    username = payload.username if payload.username else payload.email.split("@")[0]
    assigned_lot = payload.assigned_lot.strip() if (payload.assigned_lot and payload.assigned_lot.strip()) else None
    user = User(
        email=payload.email,
        username=username,
        phone=payload.phone,
        assigned_lot=assigned_lot,
        shift=payload.shift or "Ca Sáng (06h - 14h)",
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role if payload.role else UserRole.customer,
        status="active",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: DbSession = Depends(get_db)):
    clean_identifier = payload.email.strip().lower()

    # Map common convenience aliases
    if clean_identifier == "staff":
        clean_identifier = "staff@parking.vn"
    elif clean_identifier == "admin":
        clean_identifier = "admin@parking.vn"
    elif clean_identifier == "customer":
        clean_identifier = "customer@parking.vn"
    elif clean_identifier == "dan@gmai.com":
        clean_identifier = "dan@gmail.com"

    user = (
        db.query(User)
        .filter(
            (User.email.ilike(clean_identifier))
            | (User.username.ilike(clean_identifier))
        )
        .first()
    )
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không chính xác")

    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )
    return Token(access_token=access_token)


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: DbSession = Depends(get_db)):
    clean_email = payload.email.strip().lower()
    clean_phone = payload.phone.strip()

    if not clean_email or not clean_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vui lòng cung cấp đầy đủ Email và Số điện thoại đã đăng ký."
        )

    if len(payload.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu mới phải có tối thiểu 6 ký tự."
        )

    # Tìm user theo email
    user = db.query(User).filter(User.email.ilike(clean_email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy tài khoản tương ứng với Email này trong hệ thống."
        )

    # Xác thực số điện thoại
    user_phone = (user.phone or "").strip().replace(" ", "").replace(".", "")
    input_phone = clean_phone.replace(" ", "").replace(".", "")

    if not user_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản này chưa đăng ký số điện thoại bảo mật. Vui lòng liên hệ Quản trị viên."
        )

    if user_phone != input_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Số điện thoại xác thực không khớp với thông tin tài khoản đã đăng ký."
        )

    # Cập nhật mật khẩu mới đã hash
    user.password_hash = hash_password(payload.new_password)
    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "message": f"Đặt lại mật khẩu cho tài khoản {user.email} thành công! Quý khách có thể đăng nhập ngay với mật khẩu mới."
    }
