from sqlalchemy.orm import Session
from app.models.legal import LegalDocument, UserLegalAcceptance


def get_active_documents(db: Session):
    return (
        db.query(LegalDocument)
        .filter(LegalDocument.is_active == True)
        .order_by(LegalDocument.document_type.asc())
        .all()
    )


def get_user_acceptances(db: Session, user_id: int):
    return (
        db.query(UserLegalAcceptance)
        .filter(UserLegalAcceptance.user_id == user_id)
        .all()
    )


def has_acceptance_for_document(db: Session, user_id: int, document_id: int) -> bool:
    return (
        db.query(UserLegalAcceptance)
        .filter(
            UserLegalAcceptance.user_id == user_id,
            UserLegalAcceptance.legal_document_id == document_id,
        )
        .first()
        is not None
    )


def register_acceptance(
    db: Session,
    user_id: int,
    document_id: int,
    ip_address: str | None = None,
    user_agent: str | None = None,
):
    acceptance = UserLegalAcceptance(
        user_id=user_id,
        legal_document_id=document_id,
        accepted=True,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    db.add(acceptance)
    db.commit()
    db.refresh(acceptance)
    return acceptance