from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.schemas import ContentResponse
from dependencies import get_current_user
from services.content_service import fetch_news
from core.database import get_db, User

router = APIRouter(prefix="/content", tags=["Content"])

@router.get("", response_model=ContentResponse)
async def get_personalized_content(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.subscribed_categories:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No subscribed categories")
    
    articles = await fetch_news(current_user.subscribed_categories)
    return {"articles": articles}
