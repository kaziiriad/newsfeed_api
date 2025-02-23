from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import AsyncSessionLocal
from models.db_models import User
from utils.email import send_digest_email
from services.content_service import fetch_news

async def send_weekly_digests():
    async with AsyncSessionLocal() as db:
        # Fetch users with subscribed categories
        result = await db.execute(
            select(User).where(User.subscribed_categories != [])
        )
        users = result.scalars().all()

        # Collect all unique categories
        all_categories = set()
        for user in users:
            all_categories.update(user.subscribed_categories)
        
        # Fetch articles for each category (cache to avoid redundant API calls)
        category_articles = {}
        for category in all_categories:
            articles = await fetch_news([category])
            category_articles[category] = articles[:10]  # Top 10 articles
        
        # Send emails to users
        for user in users:
            user_articles = []
            for category in user.subscribed_categories:
                user_articles.extend(category_articles.get(category, []))
            
            if user_articles:
                await send_digest_email(user.email, user_articles)