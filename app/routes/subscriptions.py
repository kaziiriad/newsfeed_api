from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.database import get_db
from models.schemas import SubscriptionUpdate
from models.db_models import User
from dependencies import get_current_user
from utils.email import send_subscription_email

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

ALLOWED_CATEGORIES = ["Tech", "Health", "Business", "Science", "Sports", "Entertainment"]

@router.post("/subscribe")
async def subscribe(
    subscription: SubscriptionUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    invalid_categories = [category for category in subscription.categories if category not in ALLOWED_CATEGORIES]
    if invalid_categories:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid categories: {invalid_categories}")
    
    updated_categories = list(set(current_user.subscribed_categories + subscription.categories))
    current_user.subscribed_categories = updated_categories
    await db.commit()
    await db.refresh(current_user)

    background_tasks.add_task(send_subscription_email, current_user.email, current_user.subscribed_categories)
    
    return {"message": "Subscribed successfully"}

@router.post("/unsubscribe")
async def unsubscribe(
    subscription: SubscriptionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    updated_categories = [category for category in current_user.subscribed_categories if category not in subscription.categories]
    current_user.subscribed_categories = updated_categories
    await db.commit()
    await db.refresh(current_user)

    return {"message": "Unsubscribed successfully"}

