import stripe
from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from fastapi.responses import JSONResponse
from core.database import get_db
from models.db_models import User
from dependencies import get_current_user
from core.config import settings
from utils.email import send_payment_confirmation
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/payment", tags=["Payment"])
stripe.api_key = settings.STRIPE_SECRET_KEY

@router.post("/create-intent")
async def create_payment_intent(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        if not user.stripe_customer_id:
            customer = stripe.Customer.create(email=user.email)
            user.stripe_customer_id = customer.id
            await db.commit()

        intent = stripe.PaymentIntent.create(
            amount=999,
            currency="usd",
            customer=user.stripe_customer_id,
            metadata={"user_id": str(user.id)},  # Link payment to user
            automatic_payment_methods={"enabled": True},
        )
        return {"clientSecret": intent.client_secret}
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
    logger.info(f"Webhook received: {payload.decode()}")  # Log raw payload

    try:
        event = stripe.Webhook.construct_event(
            payload,
            stripe_signature,
            settings.STRIPE_WEBHOOK_SECRET
        )
        logger.info(f"Event type: {event['type']}")

    # except ValueError as e:

    #     return JSONResponse({"error": "Invalid payload"}, 400)
    # except stripe.error.SignatureVerificationError as e:
    #     return JSONResponse({"error": "Invalid signature"}, 400)

    # Handle successful payment
        if event["type"] == "payment_intent.succeeded":
            payment_intent = event["data"]["object"]
            user_id = payment_intent["metadata"].get("user_id")
            logger.info(f"Updating user {user_id} to premium")

            try:
                user_id = int(user_id)
            except ValueError:
                logger.error(f"Invalid user_id: {user_id}")
                # return JSONResponse({"error": "Invalid user_id"}, 400)

            # Update user premium status
            user = await db.get(User, user_id)
            if not user:
                logger.error(f"User {user_id} not found")
                raise HTTPException(404, "User not found")
            
            user.is_premium = True
            await db.commit()
            logger.info(f"Updated premium status for user {user_id}")

            # Send payment confirmation email
            await send_payment_confirmation(user.email)
            logger.info(f"Sent payment confirmation email to {user.email}")

    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        raise
