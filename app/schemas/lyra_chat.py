from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class LyraChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Mensagem enviada para a Lyra")
    conversation_history: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Histórico opcional da conversa"
    )


class LyraChatResponse(BaseModel):
    user_message: str
    lyra_response: str
    mode_used: str


class LyraChatHistoryMessage(BaseModel):
    role: str
    content: str


class LyraChatHistoryResponse(BaseModel):
    messages: List[LyraChatHistoryMessage] = Field(default_factory=list)
    total: int = 0


class LyraChatResetResponse(BaseModel):
    cleared: bool
    message: str