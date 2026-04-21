import json
from sqlalchemy.orm import Session
from app.models.whatsapp_log import WhatsAppMessageLog


def create_whatsapp_log(
    db: Session,
    *,
    user_id: int | None = None,
    reminder_id: int | None = None,
    provider: str = "meta_cloud",
    to_phone: str | None = None,
    status: str = "pending",
    provider_message_id: str | None = None,
    response_payload: dict | None = None,
    error_message: str | None = None,
):
    log = WhatsAppMessageLog(
        user_id=user_id,
        reminder_id=reminder_id,
        provider=provider,
        phone_number=to_phone,
        message_body="",
        status=status,
        provider_message_id=provider_message_id,
        response_payload=json.dumps(response_payload, ensure_ascii=False) if response_payload else None,
        error_message=error_message,
    )

    db.add(log)
    db.commit()
    db.refresh(log)
    return log