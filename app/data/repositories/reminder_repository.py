from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.reminder import Reminder


def create_reminder(
    db: Session,
    user_id: int,
    title: str,
    remind_at,
    description: str | None = None,
    channel: str = "in_app",
):
    reminder = Reminder(
        user_id=user_id,
        title=title,
        description=description,
        remind_at=remind_at,
        channel=channel,
        status="pending",
        sent=False,
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


def list_user_reminders(db: Session, user_id: int):
    return (
        db.query(Reminder)
        .filter(Reminder.user_id == user_id)
        .order_by(Reminder.remind_at.asc())
        .all()
    )


def list_due_reminders(db: Session):
    now = datetime.now(timezone.utc)
    return (
        db.query(Reminder)
        .filter(Reminder.sent == False, Reminder.status == "pending", Reminder.remind_at <= now)
        .order_by(Reminder.remind_at.asc())
        .all()
    )


def mark_reminder_sent(db: Session, reminder_id: int):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if reminder:
        reminder.sent = True
        reminder.status = "sent"
        db.commit()
        db.refresh(reminder)
    return reminder