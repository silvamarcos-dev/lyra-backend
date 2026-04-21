from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, func
from app.core.database import Base


class LegalDocument(Base):
    __tablename__ = "legal_documents"

    id = Column(Integer, primary_key=True, index=True)
    document_type = Column(String(50), nullable=False)
    version = Column(String(20), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserLegalAcceptance(Base):
    __tablename__ = "user_legal_acceptances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    legal_document_id = Column(Integer, ForeignKey("legal_documents.id"), nullable=False, index=True)
    accepted = Column(Boolean, nullable=False, default=True)
    accepted_at = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String(100), nullable=True)
    user_agent = Column(String(500), nullable=True)