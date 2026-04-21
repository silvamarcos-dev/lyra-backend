from app.data.store.agent_registry import list_agents
from app.services.agent_chat import build_agent_response
from app.brain.supervisor import (
    build_supervisor_final_response,
    evaluate_agent_steps,
)


def _normalize(text: str) -> str:
    return text.strip().lower()


def _score_agent(agent: dict, user_message: str) -> int:
    message = _normalize(user_message)
    score = 0

    searchable = " ".join([
        agent.get("name", ""),
        agent.get("role", ""),
        agent.get("specialty", ""),
        agent.get("description", ""),
        agent.get("goal", "")
    ]).lower()

    keywords = [
        "imobili", "imóvel", "imovel", "aluguel", "lead",
        "jurid", "contrato", "cláusula", "clausula",
        "venda", "comercial", "negociação", "negociacao",
        "suporte", "erro", "bug",
        "estrateg", "marketing", "crescimento", "posicionamento"
    ]

    for keyword in keywords:
        if keyword in message and keyword in searchable:
            score += 3

    for token in message.split():
        if len(token) > 4 and token in searchable:
            score += 1

    return score


def select_team_agents(user_message: str, max_agents: int = 3) -> list[dict]:
    agents = list_agents()

    ranked = []

    for agent in agents:
        score = _score_agent(agent, user_message)
        if score > 0:
            ranked.append((score, agent))

    ranked.sort(key=lambda item: item[0], reverse=True)

    selected = [agent for _, agent in ranked[:max_agents]]

    if not selected and agents:
        selected = agents[:1]

    return selected


def _build_collaboration_message(
    user_message: str,
    previous_output: str | None,
    stage: int,
    agent_name: str
) -> str:
    if stage == 1 or not previous_output:
        return (
            f"Pedido original do usuário:\n{user_message}\n\n"
            "Gere a melhor resposta inicial possível dentro da sua especialidade."
        )

    return (
        f"Pedido original do usuário:\n{user_message}\n\n"
        f"Resposta anterior produzida por outro agente:\n{previous_output}\n\n"
        f"Agora atue como {agent_name} e melhore essa resposta dentro da sua especialidade. "
        "Você pode complementar, corrigir, refinar, reorganizar ou tornar mais útil."
    )


def orchestrate_team_chat(user_message: str) -> dict:
    selected_agents = select_team_agents(user_message, max_agents=3)

    if not selected_agents:
        return {
            "agents_used": [],
            "steps": [],
            "evaluation": {},
            "final_response": "Nenhum agente disponível para processar a solicitação."
        }

    steps = []
    current_output = None

    for index, agent in enumerate(selected_agents, start=1):
        collaboration_message = _build_collaboration_message(
            user_message=user_message,
            previous_output=current_output,
            stage=index,
            agent_name=agent.get("name", "Agente")
        )

        response = build_agent_response(agent, collaboration_message)

        step_data = {
            "stage": index,
            "agent_name": agent.get("name", "Agente"),
            "agent_role": agent.get("role", "Sem função definida"),
            "agent_specialty": agent.get("specialty", "Sem especialidade definida"),
            "response": response
        }

        steps.append(step_data)
        current_output = response

    evaluation = evaluate_agent_steps(
        user_message=user_message,
        steps=steps
    )

    final_response = build_supervisor_final_response(
        user_message=user_message,
        steps=steps,
        evaluation=evaluation
    )

    return {
        "agents_used": [agent.get("name", "Agente") for agent in selected_agents],
        "steps": steps,
        "evaluation": evaluation,
        "final_response": final_response
    }