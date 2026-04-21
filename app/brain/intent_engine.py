def detect_intent(user_message: str) -> str:
    text = user_message.lower().strip()

    search_keywords = [
        "pesquise", "busque", "ache", "procure",
        "tema enem", "enem", "notícia", "noticia",
        "hoje", "atual", "último", "ultimo",
        "fonte", "link", "site oficial"
    ]

    code_keywords = [
        "código", "codigo", "programar", "python", "react", "tsx",
        "javascript", "api", "backend", "frontend", "bug", "erro",
        "corrigir", "função", "funcao", "classe", "arquivo", "rota"
    ]

    creative_keywords = [
        "crie um texto", "escreva", "roteiro", "copy", "post",
        "legenda", "branding", "manifesto", "storytelling",
        "pitch", "apresentação", "apresentacao", "campanha"
    ]

    memory_keywords = [
        "lembra", "lembrar", "memória", "memoria",
        "histórico", "historico", "o que eu falei",
        "salvou", "salvar", "contexto anterior"
    ]

    agent_builder_keywords = [
        "crie um agente", "criar agente", "gere um agente",
        "gerar agente", "monte um agente", "novo agente",
        "quero um agente", "faça um agente", "faca um agente"
    ]

    agent_management_keywords = [
        "listar agentes", "liste os agentes", "meus agentes",
        "editar agente", "edite o agente", "melhore esse agente",
        "reorganize os agentes", "gerencie os agentes",
        "gerenciar agentes", "atualize o agente"
    ]

    quick_chat_keywords = [
        "oi", "olá", "ola", "opa", "oie", "oii", "oiii",
        "bom dia", "boa tarde", "boa noite",
        "tudo bem", "como você está", "como voce está",
        "como você ta", "como voce ta", "quem é você",
        "quem e voce", "o que você faz", "o que voce faz"
    ]

    if any(keyword in text for keyword in quick_chat_keywords):
        return "quick_chat"

    if any(keyword in text for keyword in agent_builder_keywords):
        return "agent_builder"

    if any(keyword in text for keyword in agent_management_keywords):
        return "agent_management"

    if any(keyword in text for keyword in search_keywords):
        return "search"

    if any(keyword in text for keyword in memory_keywords):
        return "memory"

    if any(keyword in text for keyword in code_keywords):
        return "code"

    if any(keyword in text for keyword in creative_keywords):
        return "creative"

    return "general"