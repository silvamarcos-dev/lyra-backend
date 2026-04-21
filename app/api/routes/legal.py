from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.schemas.legal import (
    LegalAcceptRequest,
    LegalDocumentsListResponse,
    LegalAcceptanceResponse,
    LegalStatusResponse,
)
from app.data.repositories.legal_repository import (
    get_active_documents,
    get_user_acceptances,
    has_acceptance_for_document,
    register_acceptance,
)

router = APIRouter(prefix="/legal", tags=["Legal"])


@router.get("/documents", response_model=LegalDocumentsListResponse)
def list_legal_documents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    docs = get_active_documents(db)

    return LegalDocumentsListResponse(
        documents=[
            {
                "id": doc.id,
                "document_type": doc.document_type,
                "version": doc.version,
                "title": doc.title,
                "content": doc.content,
            }
            for doc in docs
        ]
    )


@router.get("/status", response_model=LegalStatusResponse)
def get_legal_status(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    docs = get_active_documents(db)
    acceptances = get_user_acceptances(db, current_user.id)

    accepted_ids = {item.legal_document_id for item in acceptances}
    missing_docs = [doc.document_type for doc in docs if doc.id not in accepted_ids]

    return LegalStatusResponse(
        accepted_all=len(missing_docs) == 0,
        missing_documents=missing_docs,
    )


@router.post("/accept", response_model=LegalAcceptanceResponse)
def accept_legal_documents(
    payload: LegalAcceptRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    docs = get_active_documents(db)
    active_doc_ids = {doc.id for doc in docs}

    for doc_id in payload.document_ids:
        if doc_id not in active_doc_ids:
            raise HTTPException(status_code=400, detail=f"Documento inválido: {doc_id}")

    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    try:
        for doc_id in payload.document_ids:
            already_accepted = has_acceptance_for_document(
                db=db,
                user_id=current_user.id,
                document_id=doc_id,
            )

            if not already_accepted:
                register_acceptance(
                    db=db,
                    user_id=current_user.id,
                    document_id=doc_id,
                    ip_address=ip_address,
                    user_agent=user_agent,
                )

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Não foi possível registrar o aceite legal."
        )

    return LegalAcceptanceResponse(
        success=True,
        message="Aceite legal registrado com sucesso."
    )