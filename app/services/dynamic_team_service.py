from app.data.store.agent_registry import list_agents
from app.services.agent_chat import build_agent_response
from app.brain.supervisor import build_supervisor_final_response


def _normalize(text: str) -> str:
    return text.strip().lower()


def _classify_need_dimensions(user_message: str) -> list[str]:
    text = _normalize(user_message)
    dimensions = []

    if any(word in text for word in ["imobili", "imóvel", "imovel", "aluguel", "lead", "cliente"]):
        dimensions.append("atendimento_imobiliario")

    if any(word in text for word in ["jurid", "contrato", "cláusula", "clausula", "lei", "termo"]):
        dimensions.append("juridico")

    if any(word in text for word in ["estrateg", "crescimento", "posicionamento", "planejamento"]):
        dimensions.append("estrategia")

    if any(word in text for word in ["marketing", "conteúdo", "conteudo", "copy", "post", "instagram"]):
        dimensions.append("marketing")

    if any(word in text for word in ["finance", "financeiro", "roi", "caixa", "faturamento", "custos"]):
        dimensions.append("financeiro")

    if any(word in text for word in ["produto", "ux", "feature", "funcionalidade", "roadmap"]):
        dimensions.append("produto")

    if any(word in text for word in ["suporte", "bug", "erro", "falha", "sistema"]):
        dimensions.append("suporte")

    if not dimensions:
        dimensions.append("geral")

    return dimensions


def _agent_matches_dimension(agent: dict, dimension: str) -> bool:
    searchable = " ".join([
        agent.get("name", ""),
        agent.get("role", ""),
        agent.get("specialty", ""),
        agent.get("description", ""),
        agent.get("goal", "")
    ]).lower()

    mapping = {
        "atendimento_imobiliario": ["imobili", "imóvel", "imovel", "lead", "aluguel", "atendimento"],
        "juridico": ["jurid", "contrato", "cláusula", "clausula", "lei"],
        "estrategia": ["estrateg", "planejamento", "crescimento", "posicionamento"],
        "marketing": ["marketing", "conteúdo", "conteudo", "copy", "post"],
        "financeiro": ["finance", "caixa", "roi", "custos", "faturamento"],
        "produto": ["produto", "ux", "roadmap", "feature", "funcionalidade"],
        "suporte": ["suporte", "erro", "bug", "falha", "técnico", "tecnico"],
        "geral": ["agente", "assistente", "especializado"]
    }

    keywords = mapping.get(dimension, [])
    return any(keyword in searchable for keyword in keywords)


def _select_best_agent_for_dimension(dimension: str, agents: list[dict], used_names: set[str]) -> dict | None:
    candidates = []

    for agent in agents:
        name = agent.get("name", "")
        if name in used_names:
            continue

        if _agent_matches_dimension(agent, dimension):
            score = 0
            searchable = " ".join([
                agent.get("role", ""),
                agent.get("specialty", ""),
                agent.get("description", ""),
                agent.get("goal", "")
            ]).lower()

            for token in dimension.split("_"):
                if token in searchable:
                    score += 2

            if dimension == "atendimento_imobiliario" and ("imobili" in searchable or "atendimento" in searchable):
                score += 4

            if dimension == "juridico" and ("jurid" in searchable or "contrato" in searchable):
                score += 4

            if dimension == "estrategia" and ("estrateg" in searchable or "planejamento" in searchable):
                score += 4

            candidates.append((score, agent))

    if not candidates:
        return None

    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


def build_dynamic_team(user_message: str) -> tuple[list[dict], str]:
    agents = list_agents()

    if not agents:
        return [], "Nenhum agente cadastrado."

    dimensions = _classify_need_dimensions(user_message)
    selected_agents = []
    used_names = set()
    reasons = []

    for dimension in dimensions:
        agent = _select_best_agent_for_dimension(dimension, agents, used_names)

        if agent:
            selected_agents.append(agent)
            used_names.add(agent.get("name", ""))
            reasons.append(f"{agent.get('name', 'Agente')} para {dimension}")

    if not selected_agents and agents:
        selected_agents.append(agents[0])
        reasons.append("nenhum match forte; equipe mínima com agente disponível")

    team_strategy = "Equipe montada para cobrir: " + ", ".join(reasons)
    return selected_agents, team_strategy


def _build_team_message(user_message: str, previous_output: str | None, stage: int, agent: dict) -> str:
    agent_name = agent.get("name", "Agente")
    role = agent.get("role", "Sem função definida")
    specialty = agent.get("specialty", "Sem especialidade definida")

    if stage == 1 or not previous_output:
        return (
            f"Pedido original do usuário:\n{user_message}\n\n"
            f"Você é {agent_name}, atuando como {role}, com especialidade em {specialty}.\n"
            "Produza a melhor contribuição inicial dentro da sua especialidade."
        )

    return (
        f"Pedido original do usuário:\n{user_message}\n\n"
        f"Resposta anterior produzida por outro agente:\n{previous_output}\n\n"
        f"Você é {agent_name}, atuando como {role}, com especialidade em {specialty}.\n"
        "Agora complemente, refine ou corrija a resposta anterior com foco na sua especialidade."
    )


def orchestrate_dynamic_team(user_message: str) -> dict:
    selected_agents, team_strategy = build_dynamic_team(user_message)

    if not selected_agents:
        return {
            "team_strategy": team_strategy,
            "agents_used": [],
            "steps": [],
            "final_response": "Não há agentes disponíveis para formar uma equipe."
        }

    steps = []
    current_output = None

    for index, agent in enumerate(selected_agents, start=1):
        team_message = _build_team_message(
            user_message=user_message,
            previous_output=current_output,
            stage=index,
            agent=agent
        )

        response = build_agent_response(agent, team_message)

        step_data = {
            "stage": index,
            "agent_name": agent.get("name", "Agente"),
            "agent_role": agent.get("role", "Sem função definida"),
            "agent_specialty": agent.get("specialty", "Sem especialidade definida"),
            "response": response
        }

        steps.append(step_data)
        current_output = response

    final_response = build_supervisor_final_response(
        user_message=user_message,
        steps=steps
    )

    return {
        "team_strategy": team_strategy,
        "agents_used": [agent.get("name", "Agente") for agent in selected_agents],
        "steps": steps,
        "final_response": final_response
    }