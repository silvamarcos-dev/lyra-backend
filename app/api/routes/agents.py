from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.agent import (
    AgentBlueprintResponse,
    AgentCreateRequest,
    AgentListResponse,
    AgentChatRequest,
    AgentChatResponse,
    AgentMemoryResponse,
    AgentMemoryClearResponse,
    AgentMemorySummaryResponse,
)
from app.agents.agent_factory import generate_agent_blueprint
from app.services.agent_chat import build_agent_response
from app.data.repositories.agent_repository import (
    create_agent,
    list_agents,
    get_agent_by_name,
)

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("/create", response_model=AgentBlueprintResponse)
def create_agent_route(request: AgentCreateRequest, db: Session = Depends(get_db)):
    blueprint = generate_agent_blueprint(
        user_goal=request.goal,
        custom_name=request.name or "Agente sem nome",
        custom_role=request.role or "Assistente",
        custom_specialty=request.specialty or "Geral",
        custom_description=request.description or "Agente criado manualmente.",
    )

    agent = create_agent(
        db=db,
        name=blueprint["name"],
        role=blueprint["role"],
        specialty=blueprint["specialty"],
        goal=blueprint["goal"],
        description=blueprint["description"],
    )

    return AgentBlueprintResponse(
        name=agent.name,
        role=agent.role,
        specialty=agent.specialty,
        goal=agent.goal,
        description=agent.description,
    )


@router.get("/", response_model=AgentListResponse)
def get_all_agents(db: Session = Depends(get_db)):
    agents = list_agents(db)

    serialized_agents = [
        {
            "name": agent.name,
            "role": agent.role,
            "specialty": agent.specialty,
            "goal": agent.goal,
            "description": agent.description,
        }
        for agent in agents
    ]

    return AgentListResponse(agents=serialized_agents, total=len(serialized_agents))


@router.get("/{agent_name}", response_model=AgentBlueprintResponse)
def get_agent(agent_name: str, db: Session = Depends(get_db)):
    agent = get_agent_by_name(db, agent_name)

    if not agent:
        raise HTTPException(status_code=404, detail="Agente não encontrado.")

    return AgentBlueprintResponse(
        name=agent.name,
        role=agent.role,
        specialty=agent.specialty,
        goal=agent.goal,
        description=agent.description,
    )


@router.post("/{agent_name}/chat", response_model=AgentChatResponse)
def chat_with_agent(agent_name: str, request: AgentChatRequest, db: Session = Depends(get_db)):
    agent = get_agent_by_name(db, agent_name)

    if not agent:
        raise HTTPException(status_code=404, detail="Agente não encontrado.")

    agent_dict = {
        "name": agent.name,
        "role": agent.role,
        "specialty": agent.specialty,
        "goal": agent.goal,
        "description": agent.description,
    }

    response = build_agent_response(agent_dict, request.message)

    return AgentChatResponse(
        agent_name=agent.name,
        agent_goal=agent.goal,
        user_message=request.message,
        agent_response=response
    )


@router.get("/{agent_name}/memory", response_model=AgentMemoryResponse)
def get_agent_memory(agent_name: str):
    return AgentMemoryResponse(
        agent_name=agent_name,
        total_messages=0,
        messages=[]
    )


@router.delete("/{agent_name}/memory", response_model=AgentMemoryClearResponse)
def delete_agent_memory(agent_name: str):
    return AgentMemoryClearResponse(
        agent_name=agent_name,
        cleared=True,
        message="Memória do agente apagada com sucesso."
    )


@router.get("/{agent_name}/memory/summary", response_model=AgentMemorySummaryResponse)
def get_agent_memory_summary(agent_name: str):
    return AgentMemorySummaryResponse(
        agent_name=agent_name,
        summary="Sem resumo disponível.",
        updated_at=None
    )


@router.get("/{agent_name}/memory/tags")
def get_agent_tags(agent_name: str):
    return {
        "agent_name": agent_name,
        "tags": []
    }


@router.get("/{agent_name}/objectives")
def get_agent_objectives(agent_name: str):
    return {
        "agent_name": agent_name,
        "objectives": []
    }