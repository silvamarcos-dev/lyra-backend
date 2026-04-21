from app.data.store.agent_registry import list_agents
from app.services.agent_chat import build_agent_response


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
        "imobili", "imóvel", "aluguel", "lead",
        "jurid", "contrato",
        "venda", "comercial",
        "suporte", "erro",
        "estrateg", "marketing"
    ]

    for k in keywords:
        if k in message and k in searchable:
            score += 3

    for token in message.split():
        if len(token) > 4 and token in searchable:
            score += 1

    return score


def select_multiple_agents(user_message: str, max_agents: int = 3):
    agents = list_agents()

    ranked = []

    for agent in agents:
        score = _score_agent(agent, user_message)
        if score > 0:
            ranked.append((score, agent))

    ranked.sort(key=lambda x: x[0], reverse=True)

    selected = [agent for _, agent in ranked[:max_agents]]

    if not selected and agents:
        selected = [agents[0]]

    return selected


def synthesize_response(user_message: str, agent_outputs: list) -> str:
    combined = "\n\n".join([
        f"{item['name']} ({item['role']}): {item['response']}"
        for item in agent_outputs
    ])

    # versão simples (sem IA)
    return (
        "Síntese colaborativa:\n\n"
        f"Pedido do usuário: {user_message}\n\n"
        f"Contribuições dos agentes:\n{combined}\n\n"
        "Resumo final:\n"
        "Com base nas análises acima, recomenda-se integrar as abordagens apresentadas."
    )


def orchestrate_collaborative(user_message: str) -> dict:
    agents = select_multiple_agents(user_message)

    outputs = []

    for agent in agents:
        response = build_agent_response(agent, user_message)

        outputs.append({
            "name": agent.get("name"),
            "role": agent.get("role"),
            "response": response
        })

    final = synthesize_response(user_message, outputs)

    return {
        "agents_used": [a["name"] for a in outputs],
        "agent_outputs": outputs,
        "final_response": final
    }