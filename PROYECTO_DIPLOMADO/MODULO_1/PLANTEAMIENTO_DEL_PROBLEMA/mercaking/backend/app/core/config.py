from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "MercaKing"
    DATABASE_URL: str = "mysql+pymysql://root:@localhost:3306/mercaking"
    SECRET_KEY: str = "change-me-in-production"
    CORS_ORIGINS: list[str] = ["http://localhost:5000", "http://127.0.0.1:5000"]
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    class Config:
        env_file = ".env"

settings = Settings()
