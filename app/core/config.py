from pydantic import BaseSettings

class Settings(BaseSettings):
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()

SQLALCHEMY_DATABASE_URL="postgresql+asyncpg://postgres:postgrespassword@db:5432/fitness_db"