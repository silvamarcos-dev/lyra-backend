from app.data.repositories.reminder_repository import list_due_reminders, mark_reminder_sent


def dispatch_due_reminders(db, whatsapp_service=None, voice_service=None):
    reminders = list_due_reminders(db)

    for reminder in reminders:
        try:
            if reminder.channel == "whatsapp" and whatsapp_service:
                whatsapp_service.send_text(
                    user_id=reminder.user_id,
                    message=f"Lembrete: {reminder.title}"
                )

            elif reminder.channel == "voice" and voice_service:
                voice_service.call_and_speak(
                    user_id=reminder.user_id,
                    text=f"Lembrete importante: {reminder.title}"
                )

            # in_app por enquanto só marca como enviado
            mark_reminder_sent(db, reminder.id)

        except Exception:
            # depois a gente adiciona log e status failed
            pass