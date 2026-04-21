from fastapi import APIRouter
from app.schemas.agent import AgentBlueprintResponse
from app.schemas.orchestration import (
    OrchestratorChatRequest,
    OrchestratorChatResponse,
    OrchestratorCollaborativeResponse,
    OrchestratorTeamResponse,
    TeamStepResponse,
    DynamicAgentResponse,
    OrchestratorDynamicTeamResponse,
    SupervisorEvaluationResponse,
    SupervisorScoreResponse,
)
from app.brain.orchestrator_service import orchestrate_user_message
from app.brain.orchestrator_collab_service import orchestrate_collaborative
from app.brain.orchestrator_team_service import orchestrate_team_chat
from app.agents.dynamic_agent_service import create_dynamic_agent_from_need
from app.services.dynamic_team_service import orchestrate_dynamic_team

router = APIRouter(prefix="/orchestrator", tags=["Orchestrator"])


@router.post("/chat", response_model=OrchestratorChatResponse)
def orchestrator_chat(request: OrchestratorChatRequest):
    result = orchestrate_user_message(request.message)

    return OrchestratorChatResponse(
        user_message=request.message,
        selected_agent=result["selected_agent"],
        selected_agent_role=result["selected_agent_role"],
        selection_reason=result["selection_reason"],
        agent_response=result["agent_response"]
    )


@router.post("/collaborative", response_model=OrchestratorCollaborativeResponse)
def orchestrator_collaborative(request: OrchestratorChatRequest):
    result = orchestrate_collaborative(request.message)

    return OrchestratorCollaborativeResponse(
        user_message=request.message,
        agents_used=result["agents_used"],
        final_response=result["final_response"]
    )


@router.post("/team-chat", response_model=OrchestratorTeamResponse)
def orchestrator_team_chat_route(request: OrchestratorChatRequest):
    result = orchestrate_team_chat(request.message)

    return OrchestratorTeamResponse(
        user_message=request.message,
        agents_used=result["agents_used"],
        steps=[
            TeamStepResponse(
                stage=step["stage"],
                agent_name=step["agent_name"],
                agent_role=step["agent_role"],
                agent_specialty=step["agent_specialty"],
                response=step["response"]
            )
            for step in result["steps"]
        ],
        evaluation=SupervisorEvaluationResponse(
            best_agent=result["evaluation"].get("best_agent"),
            analysis=result["evaluation"].get("analysis", ""),
            conflicts_found=result["evaluation"].get("conflicts_found", False),
            scores=[
                SupervisorScoreResponse(
                    agent_name=score["agent_name"],
                    score=score["score"],
                    reason=score["reason"]
                )
                for score in result["evaluation"].get("scores", [])
            ]
        ),
        final_response=result["final_response"]
    )


@router.post("/dynamic-agent", response_model=DynamicAgentResponse)
def create_dynamic_agent_route(request: OrchestratorChatRequest):
    result = create_dynamic_agent_from_need(request.message)

    return DynamicAgentResponse(
        created=result["created"],
        reason=result["reason"],
        agent=AgentBlueprintResponse(**result["agent"]).model_dump()
    )


@router.post("/dynamic-team", response_model=OrchestratorDynamicTeamResponse)
def orchestrator_dynamic_team_route(request: OrchestratorChatRequest):
    result = orchestrate_dynamic_team(request.message)

    return OrchestratorDynamicTeamResponse(
        user_message=request.message,
        team_strategy=result["team_strategy"],
        agents_used=result["agents_used"],
        final_response=result["final_response"]
    )