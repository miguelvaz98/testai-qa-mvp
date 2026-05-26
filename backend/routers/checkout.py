import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from shared.config import STRIPE_SECRET_KEY, STRIPE_PRICE_ID

stripe.api_key = STRIPE_SECRET_KEY

FRONTEND_URL = "https://testai-qa-mvp.vercel.app"

router = APIRouter()


class CheckoutRequest(BaseModel):
    session_id: str


@router.post("/checkout")
def create_checkout(req: CheckoutRequest):
    if not STRIPE_PRICE_ID:
        raise HTTPException(status_code=503, detail="Payments not configured yet.")
    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": STRIPE_PRICE_ID, "quantity": 1}],
            client_reference_id=req.session_id,
            success_url=f"{FRONTEND_URL}?upgraded=true",
            cancel_url=FRONTEND_URL,
        )
        return {"url": session.url}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=str(e))
