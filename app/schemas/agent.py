from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentInput(BaseModel):
    user_message: str
    memory_context: Dict[str, Any] = Field(default_factory=dict)
    objective: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentOutput(BaseModel):
    content: str
    source_agent: str
    success: bool = True
    confidence: Optional[float] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None


class AgentCreateRequest(BaseModel):
    goal: str
    name: Optional[str] = None
    role: Optional[str] = None
    specialty: Optional[str] = None
    description: Optional[str] = None


class AgentBlueprintResponse(BaseModel):
    name: str
    role: str
    specialty: str
    goal: str
    description: str


class AgentListResponse(BaseModel):
    agents: List[Dict[str, Any]]
    total: int


class AgentChatRequest(BaseModel):
    message: str


class AgentChatResponse(BaseModel):
    agent_name: str
    agent_goal: str
    user_message: str
    agent_response: str


class AgentMemoryResponse(BaseModel):
    agent_name: str
    total_messages: int
    messages: List[Dict[str, Any]]


class AgentMemoryClearResponse(BaseModel):
    agent_name: str
    cleared: bool
    message: str


class AgentMemorySummaryResponse(BaseModel):
    agent_name: str
    summary: str
    updated_at: Optional[str] = None