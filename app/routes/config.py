from fastapi import APIRouter
from core.config import settings

router = APIRouter(tags=["Config"])

@router.get("/config")
async def get_frontend_config():
    return {
        "stripePublishableKey": settings.STRIPE_PUBLIC_KEY,
        # Add other non-sensitive configs here
    }