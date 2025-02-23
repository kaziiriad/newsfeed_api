from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Dict, List

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    subscribed_categories: List[str]

class Token(BaseModel):
    access_token: str
    token_type: str

class SubscriptionUpdate(BaseModel):
    categories: List[str]

class ArticleSource(BaseModel):
    id: str
    name: str

class Article(BaseModel):
    source: ArticleSource
    title: str
    description: str | None
    url: str
    published_at: datetime


class ContentResponse(BaseModel):
    articles: List[Article]

class ContentCategoryCreate(BaseModel):
    name: str
    sample_articles: List[Dict]  # List of article objects

class ContentCategoryResponse(BaseModel):
    id: int
    name: str
    sample_articles: List[Dict]

class EmailRequest(BaseModel):
    recipient: EmailStr
    subject: str
    body: str


class ErrorResponse(BaseModel):
    detail: str


