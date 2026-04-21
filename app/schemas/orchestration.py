from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ExecutionPlan(BaseModel):
    intent: str
    primary_agent: str
    fallback_agents: List[str] = Field(default_factory=list)
    use_memory: bool = True
    use_web: bool = False
    use_multi_agent: bool = False
    store_memory: bool = True
    response_mode: str = "default"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LyraContext(BaseModel):
    user_message: str
    memory_context: Dict[str, Any] = Field(default_factory=dict)
    intent: str = "general"
    execution_plan: Optional[ExecutionPlan] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LyraResult(BaseModel):
    response: str
    intent: str
    agent_used: str
    success: bool = True
    used_fallback: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)


class OrchestratorChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    selected_mode: Optional[str] = "auto"
    selected_agents: List[str] = Field(default_factory=list)
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)


class OrchestratorChatResponse(BaseModel):
    user_message: str
    final_response: str
    mode_used: str
    selected_agents: List[str] = Field(default_factory=list)
    execution_plan: Optional[Dict[str, Any]] = None


class OrchestratorModeResponse(BaseModel):
    mode: str
    label: str
    description: str


class OrchestratorModesResponse(BaseModel):
    modes: List[OrchestratorModeResponse] = Field(default_factory=list)


class OrchestratorAgentCard(BaseModel):
    name: str
    role: Optional[str] = None
    specialty: Optional[str] = None
    description: Optional[str] = None


class OrchestratorAgentsResponse(BaseModel):
    agents: List[OrchestratorAgentCard] = Field(default_factory=list)
    total: int = 0


class CollaborativeStep(BaseModel):
    agent_name: str
    role: Optional[str] = None
    response: str
    status: str = "completed"


class OrchestratorCollaborativeResponse(BaseModel):
    user_message: str
    mode_used: str
    final_response: str
    steps: List[CollaborativeStep] = Field(default_factory=list)
    selected_agents: List[str] = Field(default_factory=list)
    execution_plan: Optional[Dict[str, Any]] = None


class TeamMember(BaseModel):
    name: str
    role: Optional[str] = None
    specialty: Optional[str] = None
    description: Optional[str] = None


class TeamStepResponse(BaseModel):
    agent_name: str
    role: Optional[str] = None
    response: str
    status: str = "completed"


class OrchestratorTeamResponse(BaseModel):
    user_message: str
    mode_used: str
    team_name: Optional[str] = None
    team_members: List[TeamMember] = Field(default_factory=list)
    steps: List[TeamStepResponse] = Field(default_factory=list)
    final_response: str
    execution_plan: Optional[Dict[str, Any]] = None

class TeamStepResponse(BaseModel):
    agent_name: str
    role: Optional[str] = None
    response: str
    status: str = "completed"


class OrchestratorTeamResponse(BaseModel):
    user_message: str
    mode_used: str
    team_name: Optional[str] = None
    team_members: List[TeamMember] = Field(default_factory=list)
    steps: List[TeamStepResponse] = Field(default_factory=list)
    final_response: str
    execution_plan: Optional[Dict[str, Any]] = None

class DynamicAgentResponse(BaseModel):
    agent_name: str
    role: Optional[str] = None
    specialty: Optional[str] = None
    description: Optional[str] = None
    goal: Optional[str] = None
    created_by: Optional[str] = "lyra"
    status: str = "active"
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TeamStepResponse(BaseModel):
    agent_name: str
    action: str
    result: str
    success: bool = True


class OrchestratorDynamicTeamResponse(BaseModel):
    objective: str
    final_response: str
    steps: List[TeamStepResponse] = Field(default_factory=list)
    agents_involved: List[str] = Field(default_factory=list)
    success: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SupervisorEvaluationResponse(BaseModel):
    success: bool = True
    selected_mode: str
    selected_agents: List[str] = Field(default_factory=list)
    reasoning: str
    confidence: float = 0.0
    execution_plan: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SupervisorScoreResponse(BaseModel):
    agent_name: str
    score: float
    reasoning: str
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    selected: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)