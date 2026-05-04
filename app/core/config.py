import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        
    UPLOADS_DIR: str = "uploads"
    # app
    APP_NAME: str = "FastAPI App"
    DEBUG: bool = True

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "tutor_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
