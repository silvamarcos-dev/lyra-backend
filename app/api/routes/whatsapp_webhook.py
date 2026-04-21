from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse

from app.core.settings import WHATSAPP_VERIFY_TOKEN

router = APIRouter(prefix="/webhooks/whatsapp", tags=["WhatsApp Webhook"])


@router.get("")
def verify_whatsapp_webhook(
    hub_mode: str | None = None,
    hub_verify_token: str | None = None,
    hub_challenge: str | None = None,
):
    if hub_mode == "subscribe" and hub_verify_token == WHATSAPP_VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge or "")

    raise HTTPException(status_code=403, detail="Webhook verification failed.")


@router.post("")
async def receive_whatsapp_webhook(request: Request):
    payload = await request.json()

    print("[WHATSAPP WEBHOOK] payload recebido:")
    print(payload)

    return {"success": True}