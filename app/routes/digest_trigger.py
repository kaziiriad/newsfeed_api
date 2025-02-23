# app/routes/test.py
from fastapi import APIRouter
from services.digest_service import send_weekly_digests

router = APIRouter(prefix="/test", tags=["Test"])

@router.post("/trigger-digest")
async def trigger_digest():
    await send_weekly_digests()
    return {"message": "Digest triggered"}