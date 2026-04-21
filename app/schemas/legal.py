from typing import List
from pydantic import BaseModel

class LegalAcceptRequest(BaseModel):
    document_ids: List[int]

class LegalDocumentResponse(BaseModel):
    id: int
    document_type: str
    version: str
    title: str
    content: str

class LegalDocumentsListResponse(BaseModel):
    documents: List[LegalDocumentResponse]

class LegalAcceptanceResponse(BaseModel):
    success: bool
    message: str

class LegalStatusResponse(BaseModel):
    accepted_all: bool
    missing_documents: List[str]