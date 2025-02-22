from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    subscribed_categories = Column(ARRAY(String))  # Array of category names


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    source_id = Column(String)
    title = Column(String)
    description = Column(String)
    url = Column(String)
    published_at = Column(String)
    category = Column(String)
    