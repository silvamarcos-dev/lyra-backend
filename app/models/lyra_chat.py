from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from app.core.database import Base


class LyraChatMessage(Base):
    __tablename__ = "lyra_chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    role = Column(String(50), nullable=False)  # user / assistant
    content = Column(Text, nullable=False)
    mode_used = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())