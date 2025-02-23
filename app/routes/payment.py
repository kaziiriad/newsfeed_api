# app/routes/payment.py
import stripe
from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from fastapi.responses import JSONResponse
from core.database import get_db
from models.db_models import User
from dependencies import get_current_user
from core.config import settings
from models.schemas import PaymentCreate
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/payment", tags=["Payment"])
stripe.api_key = settings.STRIPE_SECRET_KEY

@router.post("/create-intent")
async def create_payment_intent(
    payment: PaymentCreate,
    user: User = Depends(get_current_user)
):
    try:
        intent = stripe.PaymentIntent.create(
            amount=payment.amount,
            currency=payment.currency,
            metadata={"user_id": user.id}
        )
        return {"client_secret": intent.client_secret}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Stripe Webhook Handler
@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None),
    db: AsyncSession = Depends(get_db)
):
    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload,
            stripe_signature,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JSONResponse({"error": "Invalid payload"}, 400)
    except stripe.error.SignatureVerificationError as e:
        return JSONResponse({"error": "Invalid signature"}, 400)

    # Handle successful payment
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        user_id = payment_intent["metadata"]["user_id"]

        # Update user premium status
        user = await db.get(User, user_id)
        user.is_premium = True
        await db.commit()

    return JSONResponse({"status": "success"})