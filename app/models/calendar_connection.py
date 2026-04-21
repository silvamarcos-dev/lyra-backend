from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.core.database import Base


class CalendarConnection(Base):
    __tablename__ = "calendar_connections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    provider = Column(String(50), nullable=False, default="google")
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    calendar_email = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())