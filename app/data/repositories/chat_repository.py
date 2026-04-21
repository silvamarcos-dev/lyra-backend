from sqlalchemy.orm import Session
from app.models.lyra_chat import LyraChatMessage


def save_message(db: Session, user_id, role, content, mode=None):
    msg = LyraChatMessage(
        user_id=user_id,
        role=role,
        content=content,
        mode_used=mode,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def get_chat_history(db: Session, user_id: int):
    return (
        db.query(LyraChatMessage)
        .filter(LyraChatMessage.user_id == user_id)
        .order_by(LyraChatMessage.created_at.asc())
        .all()
    )


def clear_chat(db: Session, user_id: int):
    db.query(LyraChatMessage).filter(LyraChatMessage.user_id == user_id).delete()
    db.commit()