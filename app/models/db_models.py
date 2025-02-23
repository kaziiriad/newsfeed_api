from sqlalchemy import Boolean, Column, Integer, String, ARRAY, JSON
from core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    subscribed_categories = Column(ARRAY(String), default=[])  # Array of category names
    is_premium: bool = Column(Boolean, default=False)


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    source_id = Column(String)
    title = Column(String)
    description = Column(String)
    url = Column(String)
    published_at = Column(String)
    category = Column(String)

class ContentCategory(Base):
    __tablename__ = "content_categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)  # e.g., "Tech", "Health"
    sample_articles = Column(JSON)  # Store articles as JSON
