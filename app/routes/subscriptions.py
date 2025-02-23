from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.database import get_db
from models.schemas import SubscriptionUpdate
from models.db_models import ContentCategory, User
from dependencies import get_current_user
from utils.email import send_subscription_email

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

# ALLOWED_CATEGORIES = ["tech", "health", "business", "science", "sports", "entertainment"]


@router.post("/subscribe")
async def subscribe(
    subscription: SubscriptionUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ContentCategory.name))
    allowed_categories = [cat for cat in result.scalars().all()]

    invalid_categories = [
        category
        for category in subscription.categories
        if category not in allowed_categories
    ]
    if invalid_categories:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid categories: {invalid_categories}",
        )

    current_categories = current_user.subscribed_categories or []
    updated_categories = list(set(current_categories + subscription.categories))
    current_user.subscribed_categories = updated_categories
    await db.commit()
    await db.refresh(current_user)

    background_tasks.add_task(
        send_subscription_email, current_user.email, current_user.subscribed_categories
    )

    return {"message": "Subscribed successfully"}


@router.post("/unsubscribe")
async def unsubscribe(
    subscription: SubscriptionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    current_categories = current_user.subscribed_categories or []
    updated_categories = [
        category
        for category in current_categories
        if category not in subscription.categories
    ]
    current_user.subscribed_categories = updated_categories
    await db.commit()
    await db.refresh(current_user)

    return {"message": "Unsubscribed successfully"}
