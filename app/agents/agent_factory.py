def generate_agent_blueprint(
    user_goal: str,
    custom_name: str | None = None,
    custom_role: str | None = None,
    custom_specialty: str | None = None,
    custom_description: str | None = None,
) -> dict:
    goal = user_goal.strip()
    goal_lower = goal.lower()

    agent_name = custom_name.strip() if custom_name else "Nova"
    role = custom_role.strip() if custom_role else "Agente Especializado"
    specialty = custom_specialty.strip() if custom_specialty else "Assistência geral"
    description = custom_description.strip() if custom_description else "Agente inteligente especializada"

    if not custom_name:
        if "imobili" in goal_lower:
            agent_name = "Aurora"
        elif "juríd" in goal_lower or "jurid" in goal_lower:
            agent_name = "Lex"
        elif "vendas" in goal_lower or "comercial" in goal_lower:
            agent_name = "Pulse"
        elif "suporte" in goal_lower:
            agent_name = "Volt"
        elif "estratég" in goal_lower or "estrateg" in goal_lower:
            agent_name = "Atlas"

    if not custom_role:
        if "imobili" in goal_lower:
            role = "Assistente de Atendimento Imobiliário"
        elif "juríd" in goal_lower or "jurid" in goal_lower:
            role = "Assistente Jurídico"
        elif "vendas" in goal_lower or "comercial" in goal_lower:
            role = "Assistente Comercial"
        elif "suporte" in goal_lower:
            role = "Assistente de Suporte Técnico"

    if not custom_specialty:
        if "imobili" in goal_lower:
            specialty = "Leads, imóveis e atendimento humanizado"
        elif "juríd" in goal_lower or "jurid" in goal_lower:
            specialty = "Contratos, análise e apoio jurídico"
        elif "vendas" in goal_lower or "comercial" in goal_lower:
            specialty = "Conversão, abordagem e negociação"
        elif "suporte" in goal_lower:
            specialty = "Diagnóstico técnico e orientação ao usuário"

    if not custom_description:
        if "imobili" in goal_lower:
            description = "Agente focada em atendimento imobiliário com linguagem humana"
        elif "juríd" in goal_lower or "jurid" in goal_lower:
            description = "Agente focada em apoio jurídico e organização contratual"
        elif "vendas" in goal_lower or "comercial" in goal_lower:
            description = "Agente focada em vendas, conversão e comunicação comercial"
        elif "suporte" in goal_lower:
            description = "Agente focada em suporte técnico e resolução de problemas"

    return {
        "name": agent_name,
        "role": role,
        "specialty": specialty,
        "description": description,
        "goal": goal,
        "target_audience": "Usuários definidos conforme o caso de uso",
        "personality": "Objetiva, especializada, útil e adaptável",
        "base_prompt": (
            f"Você é {agent_name}, atuando como {role}. "
            f"Sua especialidade é {specialty}. "
            f"Seu objetivo é: {goal}. "
            "Responda com clareza, precisão, organização e foco em resultado."
        ),
        "expected_inputs": [
            "mensagem do usuário",
            "contexto da tarefa",
            "objetivo da interação"
        ],
        "expected_outputs": [
            "resposta estruturada",
            "solução prática",
            "orientação especializada"
        ],
        "recommended_stack": [
            "Python",
            "FastAPI",
            "Pydantic",
            "python-dotenv",
            "modelo generativo futuro",
            "banco de dados futuro"
        ],
        "recommended_architecture": [
            "camada de rotas",
            "camada de schemas",
            "camada de serviços",
            "prompt layer",
            "registry futuro",
            "memory layer futura"
        ],
        "evolution_possibilities": [
            "memória conversacional",
            "multiagentes",
            "integração com APIs",
            "painel administrativo",
            "aprendizado por contexto",
            "geração automática de novos agentes"
        ]
    }