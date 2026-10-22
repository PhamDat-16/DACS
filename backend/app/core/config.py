from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Tập trung toàn bộ cấu hình ứng dụng tại một nơi.
    Giá trị được đọc từ file .env (xem .env.example để biết các key cần thiết).
    """

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    FRONTEND_ORIGIN: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Singleton - import settings này ở mọi nơi cần dùng config
settings = Settings()
