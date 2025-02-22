# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Log SQL queries (disable in production)
    future=True  # Enable SQLAlchemy 2.0 features
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False  # Prevent attribute expiration after commit
)

# 3. Base class for SQLAlchemy models
Base = declarative_base()

# 4. Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session