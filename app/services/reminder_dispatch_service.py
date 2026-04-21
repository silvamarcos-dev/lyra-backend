from sqlalchemy.orm import Session

from app.core.settings import WHATSAPP_PROVIDER
from app.data.repositories.reminder_repository import (
    list_due_reminders,
    mark_reminder_sent,
)
from app.data.repositories.whatsapp_log_repository import create_whatsapp_log
from app.integrations.whatsapp.meta_whatsapp_service import MetaWhatsAppService


def dispatch_due_reminders(db: Session):
    reminders = list_due_reminders(db)
    processed = []

    whatsapp_service = MetaWhatsAppService() if WHATSAPP_PROVIDER == "meta_cloud" else None

    print(f"[DISPATCH] reminders vencidos encontrados: {len(reminders)}")

    for reminder in reminders:
        try:
            print(
                f"[DISPATCH] id={reminder.id} user_id={reminder.user_id} "
                f"title={reminder.title} channel={reminder.channel} "
                f"status={reminder.status} sent={reminder.sent}"
            )

            if reminder.channel == "whatsapp":
                to_phone = "5544997203562"

                if not to_phone:
                    create_whatsapp_log(
                        db,
                        user_id=reminder.user_id,
                        reminder_id=reminder.id,
                        provider="meta_cloud",
                        to_phone=None,
                        status="failed",
                        response_payload={"error": "Telefone do usuário não configurado."},
                        error_message="Telefone do usuário não configurado.",
                    )
                    continue

                result = whatsapp_service.send_text(
                    to_phone=to_phone,
                    message=f"Lembrete da Lyra: {reminder.title}",
                )

                print("[WHATSAPP RESULT]", result)

                create_whatsapp_log(
                    db,
                    user_id=reminder.user_id,
                    reminder_id=reminder.id,
                    provider="meta_cloud",
                    to_phone=to_phone,
                    status="sent" if result.get("success") else "failed",
                    provider_message_id=result.get("provider_message_id"),
                    response_payload=result.get("response"),
                    error_message=None if result.get("success") else str(result.get("response")),
                )

                if result.get("success"):
                    mark_reminder_sent(db, reminder.id)

            elif reminder.channel == "in_app":
                mark_reminder_sent(db, reminder.id)

            elif reminder.channel == "voice":
                print(
                    f"[VOICE MOCK] user_id={reminder.user_id} "
                    f"message=Lembrete da Lyra: {reminder.title}"
                )
                mark_reminder_sent(db, reminder.id)

            processed.append(reminder.id)

        except Exception as e:
            print(f"[Reminder Dispatch Error] reminder_id={reminder.id} error={e}")

    return {
        "processed_count": len(processed),
        "processed_ids": processed,
    }