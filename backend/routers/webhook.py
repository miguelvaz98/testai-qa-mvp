import stripe
from fastapi import APIRouter, Request, HTTPException
from shared.config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
from backend.services.trials import mark_paid

stripe.api_key = STRIPE_SECRET_KEY

router = APIRouter()


@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig, STRIPE_WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event["type"] == "checkout.session.completed":
        data = event["data"]["object"]
        session_id = data.get("client_reference_id")
        if session_id:
            mark_paid(session_id)

    return {"ok": True}
