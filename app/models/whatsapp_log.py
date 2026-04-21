from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from app.core.database import Base


class WhatsAppMessageLog(Base):
    __tablename__ = "whatsapp_message_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    reminder_id = Column(Integer, ForeignKey("reminders.id"), nullable=True, index=True)
    provider = Column(String(50), nullable=False, default="meta_cloud")
    phone_number = Column(String(50), nullable=True)
    message_body = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    provider_message_id = Column(String(255), nullable=True)
    response_payload = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())