from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# echo=False khi production; đổi thành True nếu muốn debug SQL query lúc dev
engine = create_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class dùng chung cho toàn bộ model - alembic sẽ đọc Base.metadata để tạo migration
Base = declarative_base()


def get_db():
    """
    Dependency dùng trong các router: mở session, trả về, và luôn đóng lại sau khi
    request xử lý xong (kể cả khi có lỗi) nhờ try/finally.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
