import os
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):

    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "mydatabase")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "myuser")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "mypassword")
    DATABASE_URL: Optional[str] = None

    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-secret-key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION: int = int(os.getenv("JWT_EXPIRATION", "30"))

    NEWSAPI_KEY: Optional[str] = os.getenv("NEWSAPI_KEY")
    SENDGRID_API_KEY: Optional[str] = os.getenv("SENDGRID_API_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **data):
        super().__init__(**data)
        if not self.DATABASE_URL:
            port = self.DATABASE_PORT if self.DATABASE_PORT else "5432"            
            self.DATABASE_URL = f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{port}/{self.DATABASE_NAME}"

        print("Environment variables:")
        print(f"DATABASE_HOST: {os.getenv('DATABASE_HOST')}")
        print(f"DATABASE_PORT: {os.getenv('DATABASE_PORT')}")
        print(f"DATABASE_NAME: {os.getenv('DATABASE_NAME')}")
        print(f"DATABASE_USER: {os.getenv('DATABASE_USER')}")
        print(f"DATABASE_PASSWORD: {os.getenv('DATABASE_PASSWORD')}")

        print("\nSettings values:")
        print(f"DATABASE_HOST: {self.DATABASE_HOST}")
        print(f"DATABASE_PORT: {self.DATABASE_PORT}")
        print(f"DATABASE_NAME: {self.DATABASE_NAME}")
        print(f"DATABASE_USER: {self.DATABASE_USER}")
        print(f"DATABASE_URL: {self.DATABASE_URL}")

settings = Settings()