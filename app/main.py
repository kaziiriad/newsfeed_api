from fastapi import FastAPI
from sqlalchemy import select
from core.database import AsyncSessionLocal, engine, Base
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.digest_service import send_weekly_digests
from routes import auth, subscriptions, content, payment, digest_trigger
from models.db_models import ContentCategory

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with AsyncSessionLocal() as db:
        existing_categories = await db.execute(select(ContentCategory))
        if not existing_categories.scalars().all():
            categories = [
                ContentCategory(
                    name="tech",
                    sample_articles=[
                        {"title": "AI Breakthrough", "url": "..."},
                        {"title": "Quantum Computing", "url": "..."}
                    ]
                ),
                ContentCategory(
                    name="health",
                    sample_articles=[
                        {"title": "New Vaccine", "url": "..."},
                        {"title": "Fitness Trends", "url": "..."}
                    ]
                ),
                ContentCategory(
                    name="business",
                    sample_articles=[
                        {"title": "Stock Market Update", "url": "..."},
                        {"title": "Economic Forecast", "url": "..."}
                    ]
                ),
                ContentCategory(
                    name="science",
                    sample_articles=[
                        {"title": "Space Exploration", "url": "..."},
                        {"title": "Climate Change", "url": "..."}
                    ]
                ),
                ContentCategory(
                    name="eports",
                    sample_articles=[
                        {"title": "World Cup", "url": "..."},
                        {"title": "Olympics", "url": "..."}
                    ]
                ),
                ContentCategory(
                    name="entertainment",
                    sample_articles=[
                        {"title": "Movie Reviews", "url": "..."},
                        {"title": "Music Trends", "url": "..."}
                    ]
                )
            ]
            db.add_all(categories)
            await db.commit()
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_weekly_digests, "cron", day_of_week="mon", hour=9) # Every Monday at 9 AM
    scheduler.start()
    yield
    scheduler.shutdown()
    # Shutdown
    # Add any cleanup code here if needed

app = FastAPI(
    lifespan=lifespan,
    title="Newsfeed API",
    description="A simple API for fetching and managing news subscriptions.",
    version="1.0.0",
              )

app.include_router(auth.router)
app.include_router(subscriptions.router)
app.include_router(content.router)  
app.include_router(payment.router)  
# app.include_router(digest_trigger.router) 

@app.get("/")
def read_root():
    return {
        "message": "Hello World"
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=True)