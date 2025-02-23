# app/routes/payment.py
import stripe
from fastapi import APIRouter, Depends
from models.db_models import User
from dependencies import get_current_user
from core.config import settings

router = APIRouter(prefix="/payment", tags=["Payment"])
stripe.api_key = settings.STRIPE_SECRET_KEY

@router.post("/create-intent")
async def create_payment_intent(
    payment: PaymentCreate,
    user: User = Depends(get_current_user)
):
    intent = stripe.PaymentIntent.create(
        amount=payment.amount,
        currency=payment.currency,
        metadata={"user_id": user.id}
    )
    return {"client_secret": intent.client_secret}