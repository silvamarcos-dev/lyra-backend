from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, func
from app.core.database import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    remind_at = Column(DateTime(timezone=True), nullable=False, index=True)
    channel = Column(String(50), nullable=False, default="in_app")  # in_app, whatsapp, email, voice
    status = Column(String(50), nullable=False, default="pending")  # pending, sent, failed, cancelled
    sent = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())