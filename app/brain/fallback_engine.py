from app.agents.registry import AgentRegistry
from app.brain.supervisor import Supervisor
from app.schemas.agent import AgentInput, AgentOutput
from app.schemas.orchestration import ExecutionPlan


def execute_with_fallback(
    registry: AgentRegistry,
    plan: ExecutionPlan,
    agent_input: AgentInput
) -> tuple[AgentOutput, bool]:
    attempted_agents: list[str] = []

    for agent_name in [plan.primary_agent, *plan.fallback_agents]:
        if not registry.has(agent_name):
            attempted_agents.append(f"{agent_name}:not_registered")
            continue

        try:
            agent = registry.get(agent_name)
            output = agent.run(agent_input)
            status = Supervisor.evaluate(output)

            if status == "ok":
                output.metadata["attempted_agents"] = attempted_agents + [agent_name]
                return output, agent_name != plan.primary_agent

            attempted_agents.append(f"{agent_name}:supervisor_rejected")

        except Exception as exc:
            attempted_agents.append(f"{agent_name}:exception:{str(exc)}")

    failed_output = AgentOutput(
        content="Desculpe, não consegui gerar uma resposta confiável agora.",
        source_agent="fallback_engine",
        success=False,
        error="all_agents_failed",
        metadata={"attempted_agents": attempted_agents}
    )
    return failed_output, True