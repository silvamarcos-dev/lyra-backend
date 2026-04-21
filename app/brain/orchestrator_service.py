from app.data.store.agent_registry import list_agents
from app.services.agent_chat import build_agent_response


def _normalize(text: str) -> str:
    return text.strip().lower()


def _score_agent(agent: dict, user_message: str) -> tuple[int, str]:
    message = _normalize(user_message)

    score = 0
    reasons = []

    searchable_fields = [
        agent.get("name", ""),
        agent.get("role", ""),
        agent.get("specialty", ""),
        agent.get("description", ""),
        agent.get("goal", ""),
        agent.get("base_prompt", ""),
    ]

    combined = " ".join(searchable_fields).lower()

    keyword_groups = {
        "imobili": "pedido ligado ao contexto imobiliário",
        "imóvel": "pedido ligado a imóveis",
        "imovel": "pedido ligado a imóveis",
        "aluguel": "pedido ligado a aluguel",
        "lead": "pedido ligado a leads",
        "jurid": "pedido ligado ao contexto jurídico",
        "contrato": "pedido ligado a contratos",
        "venda": "pedido ligado a vendas",
        "comercial": "pedido ligado ao contexto comercial",
        "suporte": "pedido ligado a suporte técnico",
        "erro": "pedido ligado a problema técnico",
        "estratég": "pedido ligado a estratégia",
        "estrateg": "pedido ligado a estratégia",
        "marketing": "pedido ligado a comunicação/marketing",
    }

    for keyword, reason in keyword_groups.items():
        if keyword in message and keyword in combined:
            score += 3
            reasons.append(reason)

    # bônus por matches amplos em campos importantes
    role = agent.get("role", "").lower()
    specialty = agent.get("specialty", "").lower()
    goal = agent.get("goal", "").lower()

    for token in message.split():
        if len(token) < 4:
            continue

        if token in role:
            score += 2
        if token in specialty:
            score += 2
        if token in goal:
            score += 1

    if score == 0:
        reasons.append("agente disponível como opção geral")

    return score, "; ".join(dict.fromkeys(reasons))


def select_best_agent(user_message: str) -> tuple[dict | None, str]:
    agents = list_agents()

    if not agents:
        return None, "Nenhum agente cadastrado."

    ranked = []

    for agent in agents:
        score, reason = _score_agent(agent, user_message)
        ranked.append((score, agent, reason))

    ranked.sort(key=lambda item: item[0], reverse=True)

    best_score, best_agent, reason = ranked[0]

    if best_score <= 0:
        return best_agent, "Nenhuma especialidade teve match forte; usando melhor opção disponível."

    return best_agent, reason


def orchestrate_user_message(user_message: str) -> dict:
    selected_agent, reason = select_best_agent(user_message)

    if not selected_agent:
        return {
            "selected_agent": "Nenhum",
            "selected_agent_role": "Nenhum",
            "selection_reason": reason,
            "agent_response": "Não há agentes cadastrados para processar a solicitação."
        }

    response = build_agent_response(selected_agent, user_message)

    return {
        "selected_agent": selected_agent.get("name", "Agente"),
        "selected_agent_role": selected_agent.get("role", "Sem função definida"),
        "selection_reason": reason,
        "agent_response": response
    }