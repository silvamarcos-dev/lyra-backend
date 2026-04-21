from app.data.store.agent_registry import list_agents, save_agent
from app.agents.agent_factory import generate_agent_blueprint


def _normalize(text: str) -> str:
    return text.strip().lower()


def _agent_already_exists(user_message: str) -> tuple[bool, dict | None]:
    message = _normalize(user_message)

    for agent in list_agents():
        searchable = " ".join([
            agent.get("name", ""),
            agent.get("role", ""),
            agent.get("specialty", ""),
            agent.get("description", ""),
            agent.get("goal", "")
        ]).lower()

        score = 0

        for token in message.split():
            if len(token) >= 5 and token in searchable:
                score += 1

        if score >= 2:
            return True, agent

    return False, None


def _infer_agent_profile(user_message: str) -> dict:
    text = _normalize(user_message)

    # padrão genérico
    name = "Nova"
    role = "Agente Especializado"
    specialty = "Suporte especializado"
    description = "Agente criada dinamicamente para atender uma nova demanda"
    goal = f"Criar uma IA especializada para a seguinte necessidade: {user_message}"

    if any(word in text for word in ["finance", "financeiro", "caixa", "fluxo de caixa", "roi", "faturamento"]):
        name = "Cifra"
        role = "Assistente Financeira"
        specialty = "Fluxo de caixa, ROI, custos e análise financeira"
        description = "Agente focada em apoio financeiro e análise de indicadores"

    elif any(word in text for word in ["rh", "recrutamento", "contratação", "colaborador", "equipe"]):
        name = "Nexa"
        role = "Assistente de RH"
        specialty = "Pessoas, contratação, organização de equipe e processos internos"
        description = "Agente focada em apoio a recursos humanos e gestão de equipe"

    elif any(word in text for word in ["conteúdo", "conteudo", "copy", "legenda", "post", "instagram", "marketing"]):
        name = "Mira"
        role = "Assistente de Conteúdo e Marketing"
        specialty = "Copywriting, conteúdo, posicionamento e comunicação"
        description = "Agente focada em marketing, conteúdo e comunicação estratégica"

    elif any(word in text for word in ["dados", "dashboard", "métricas", "metricas", "indicadores", "analytics"]):
        name = "Orion"
        role = "Assistente de Dados"
        specialty = "Análise de métricas, dashboards e indicadores"
        description = "Agente focada em análise de dados e interpretação de indicadores"

    elif any(word in text for word in ["produto", "roadmap", "funcionalidade", "feature", "ux", "interface"]):
        name = "Kael"
        role = "Assistente de Produto"
        specialty = "Produto, roadmap, experiência do usuário e evolução funcional"
        description = "Agente focada em produto, funcionalidades e experiência"

    return {
        "name": name,
        "role": role,
        "specialty": specialty,
        "description": description,
        "goal": goal
    }


def create_dynamic_agent_from_need(user_message: str) -> dict:
    exists, existing_agent = _agent_already_exists(user_message)

    if exists and existing_agent:
        return {
            "created": False,
            "reason": "Já existe um agente suficientemente próximo para essa necessidade.",
            "agent": existing_agent
        }

    inferred = _infer_agent_profile(user_message)

    blueprint = generate_agent_blueprint(
        user_goal=inferred["goal"],
        custom_name=inferred["name"],
        custom_role=inferred["role"],
        custom_specialty=inferred["specialty"],
        custom_description=inferred["description"],
    )

    save_agent(blueprint)

    return {
        "created": True,
        "reason": "Novo agente criado dinamicamente com base na necessidade informada.",
        "agent": blueprint
    }