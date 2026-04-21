from fastapi import APIRouter, HTTPException

from app.schemas.orchestration import (
    OrchestratorChatRequest,
    OrchestratorChatResponse,
    OrchestratorModeResponse,
    OrchestratorModesResponse,
    OrchestratorAgentCard,
    OrchestratorAgentsResponse,
    OrchestratorCollaborativeResponse,
    CollaborativeStep,
    OrchestratorTeamResponse,
    TeamMember,
)
from app.brain.brain import analyze_message
from app.data.store.agent_registry import list_agents


router = APIRouter(prefix="/orchestrator", tags=["Orchestrator"])


@router.get("/modes", response_model=OrchestratorModesResponse)
def get_orchestrator_modes():
    modes = [
        OrchestratorModeResponse(
            mode="auto",
            label="Automático",
            description="Lyra decide o melhor fluxo com base na intenção da mensagem."
        ),
        OrchestratorModeResponse(
            mode="chat",
            label="Chat simples",
            description="Resposta direta e objetiva com foco em conversa padrão."
        ),
        OrchestratorModeResponse(
            mode="collaborative",
            label="Colaborativo",
            description="Múltiplos agentes colaboram em sequência para responder."
        ),
        OrchestratorModeResponse(
            mode="team",
            label="Equipe dinâmica",
            description="Lyra monta uma equipe ideal com base no contexto da solicitação."
        ),
    ]

    return OrchestratorModesResponse(modes=modes)


@router.get("/agents", response_model=OrchestratorAgentsResponse)
def get_orchestrator_agents():
    raw_agents = list_agents()

    agents = [
        OrchestratorAgentCard(
            name=agent.get("name", ""),
            role=agent.get("role"),
            specialty=agent.get("specialty"),
            description=agent.get("description"),
        )
        for agent in raw_agents
    ]

    return OrchestratorAgentsResponse(
        agents=agents,
        total=len(agents)
    )


@router.post("/chat", response_model=OrchestratorChatResponse)
def orchestrator_chat(request: OrchestratorChatRequest):
    try:
        plan = analyze_message(request.message)

        selected_agents = request.selected_agents or []
        mode_used = request.selected_mode or "auto"

        final_response = (
            f"Lyra analisou sua solicitação e definiu o fluxo '{plan.intent}' "
            f"com agente principal '{plan.primary_agent}'."
        )

        return OrchestratorChatResponse(
            user_message=request.message,
            final_response=final_response,
            mode_used=mode_used,
            selected_agents=selected_agents,
            execution_plan=plan.model_dump(),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar orquestração: {str(e)}")


@router.post("/collaborative", response_model=OrchestratorCollaborativeResponse)
def orchestrator_collaborative(request: OrchestratorChatRequest):
    try:
        plan = analyze_message(request.message)

        selected_agents = request.selected_agents or []
        if not selected_agents:
            selected_agents = [plan.primary_agent] + list(plan.fallback_agents)

        steps = []
        for agent_name in selected_agents:
            steps.append(
                CollaborativeStep(
                    agent_name=agent_name,
                    role="specialist",
                    response=f"O agente '{agent_name}' contribuiu para a análise da solicitação.",
                    status="completed",
                )
            )

        final_response = (
            f"Resposta colaborativa concluída com {len(steps)} agente(s). "
            f"Agente principal: {plan.primary_agent}."
        )

        return OrchestratorCollaborativeResponse(
            user_message=request.message,
            mode_used="collaborative",
            final_response=final_response,
            steps=steps,
            selected_agents=selected_agents,
            execution_plan=plan.model_dump(),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na colaboração entre agentes: {str(e)}")


@router.post("/team", response_model=OrchestratorTeamResponse)
def orchestrator_team(request: OrchestratorChatRequest):
    try:
        plan = analyze_message(request.message)

        raw_agents = list_agents()
        team_members = []

        if raw_agents:
            for agent in raw_agents[:3]:
                team_members.append(
                    TeamMember(
                        name=agent.get("name", ""),
                        role=agent.get("role"),
                        specialty=agent.get("specialty"),
                        description=agent.get("description"),
                    )
                )
        else:
            team_members.append(
                TeamMember(
                    name=plan.primary_agent,
                    role="primary",
                    specialty=plan.intent,
                    description="Agente principal definido pela Lyra para esta execução."
                )
            )

        final_response = (
            f"Lyra montou uma equipe dinâmica com {len(team_members)} integrante(s) "
            f"para lidar com a solicitação."
        )

        return OrchestratorTeamResponse(
            user_message=request.message,
            mode_used="team",
            team_name="Equipe Dinâmica da Lyra",
            team_members=team_members,
            final_response=final_response,
            execution_plan=plan.model_dump(),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao montar equipe dinâmica: {str(e)}")