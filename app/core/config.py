import os
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("/mnt/c/Users/Sultan Mahmud/Desktop/Peacockindia_backend_task/.env")

class Settings(BaseSettings):

    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "mydatabase")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "myuser")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "mypassword")
    DATABASE_URL: Optional[str] = None

    JWT_SECRET: str 
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION: int = int(os.getenv("JWT_EXPIRATION", "30"))

    NEWSAPI_KEY: Optional[str] = os.getenv("NEWSAPI_KEY")
    SENDGRID_API_KEY: Optional[str] = os.getenv("SENDGRID_API_KEY")
    SENDGRID_FROM_EMAIL: Optional[str] = os.getenv("SENDGRID_FROM_EMAIL")

    STRIPE_PUBLIC_KEY: Optional[str] = os.getenv("STRIPE_PUBLIC_KEY")
    STRIPE_SECRET_KEY: Optional[str] = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SECRET: Optional[str] = os.getenv("STRIPE_WEBHOOK_SECRET")

    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **data):
        super().__init__(**data)
        if not self.DATABASE_URL:
            port = self.DATABASE_PORT if self.DATABASE_PORT else "5432"            
            self.DATABASE_URL = f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{port}/{self.DATABASE_NAME}"

settings = Settings()