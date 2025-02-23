from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.schemas import Article, ContentResponse
from dependencies import get_current_user
from services.content_service import fetch_news
from core.database import get_db
from models.db_models import User

router = APIRouter(prefix="/content", tags=["Content"])

@router.get("", response_model=ContentResponse)
async def get_personalized_content(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.subscribed_categories:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No subscribed categories")
    
    raw_articles = await fetch_news(current_user.subscribed_categories)
    articles = []
    for article in raw_articles:
        cleaned_article = Article(
            source={"id": article["source"].get("id") or "", "name": article["source"].get("name") or ""},
            author=article.get("author") or "",
            title=article.get("title") or "",
            description=article.get("description") or "",
            url=article.get("url") or "",
            urlToImage=article.get("urlToImage") or "",
            publishedAt=article.get("publishedAt") or datetime.now().isoformat(),
            content=article.get("content") or ""
        )
        articles.append(cleaned_article)

    return ContentResponse(articles=articles)

@router.get("/premium")
async def get_premium_content(
    user: User = Depends(get_current_user)
):
    if not user.is_premium:
        return {"content": "Upgrade to premium for exclusive articles!"}
        
    return {"content": "Exclusive premium articles here!"}
