from app.services.search.web_search_service import search_web
from app.core.settings import OPENAI_API_KEY, OPENAI_MODEL
from app.services.llm.openai_client import client
from app.brain.orchestrator_service import orchestrate_user_message
from app.data.store.lyra_chat_memory_store import (
    load_lyra_chat_memory,
    append_lyra_chat_message,
    clear_lyra_chat_memory,
)
from app.services.observability.unanswered_logger import log_unanswered_question


def _should_use_orchestration(message: str) -> bool:
    text = message.lower()

    simple_patterns = [
        "oi", "olá", "ola", "tudo bem",
        "quem é você", "quem e voce",
        "o que você faz", "o que voce faz"
    ]

    if any(p in text for p in simple_patterns):
        return False

    complex_signals = [
        "criar", "montar", "estratégia", "estrategia",
        "planejamento", "negócio", "negocio",
        "empresa", "sistema", "automatizar",
        "melhorar", "analisar", "resolver",
        "agente", "orquestrar", "arquitetura"
    ]

    return any(p in text for p in complex_signals)


def _is_simple_conversation(message: str) -> bool:
    text = message.lower().strip()

    simple_inputs = [
        "oi", "olá", "ola", "opa", "oie", "oii", "oiii",
        "bom dia", "boa tarde", "boa noite",
        "tudo bem", "como você tá", "como voce ta",
        "quem é você", "quem é vc", "quem e voce", "quem e vc"
    ]

    return text in simple_inputs


def _should_log_unanswered(message: str, response: str, used_fallback: bool) -> bool:
    if used_fallback:
        return True

    weak_patterns = [
        "me explica melhor",
        "entendi o que você quis dizer",
        "entendi o que você quis dizer.",
        "posso continuar essa conversa",
        "tive um problema",
        "continuo aqui com você",
        "openai_api_key não configurada",
        "vou continuar te orientando",
    ]

    response_lower = response.lower()
    return any(pattern in response_lower for pattern in weak_patterns)


def _should_use_web_search(message: str) -> bool:
    triggers = [
        "tema enem",
        "enem",
        "notícia",
        "noticia",
        "atual",
        "hoje",
        "último",
        "ultimo",
        "pesquise",
        "busque",
        "ache",
        "procure",
        "me diga o tema",
        "qual foi o tema"
    ]

    text = message.lower()
    return any(t in text for t in triggers)


def chat_with_lyra(message: str, conversation_history: list | None = None) -> dict:
    # 1. Busca web primeiro
    if _should_use_web_search(message):
        print(f"[Lyra] Busca web ativada para: {message}")

        result = search_web(message)
        print(f"[Lyra] Resultado da busca web: {result}")

        if result.get("answer"):
            final_response = (
                f"{result['answer']}\n\n"
                f"Fonte:\n{result['source']}"
            )

            append_lyra_chat_message("user", message)
            append_lyra_chat_message("assistant", final_response)

            return {
                "user_message": message,
                "lyra_response": final_response,
                "mode_used": "web_search"
            }
        else:
            print("[Lyra] Busca web não retornou resposta útil.")

    # 2. Depois tenta orquestração
    if not _is_simple_conversation(message) and _should_use_orchestration(message):
        print(f"[Lyra] Orquestração ativada para: {message}")

        orchestration_result = orchestrate_user_message(message)
        lyra_response = (
            orchestration_result.get("agent_response")
            or orchestration_result.get("final_response")
            or "A orquestração foi executada, mas não retornou uma resposta final."
        )

        append_lyra_chat_message("user", message)
        append_lyra_chat_message("assistant", lyra_response)

        return {
            "user_message": message,
            "lyra_response": lyra_response,
            "mode_used": "orchestration"
        }

    # 3. Resposta normal com OpenAI
    system_prompt = """
Você é Lyra.

Você não é um chatbot comum. Você é um sistema inteligente que conversa, entende, organiza e ajuda o usuário a executar ideias.

━━━━━━━━━━━━━━━━━━━━━━━
IDENTIDADE
━━━━━━━━━━━━━━━━━━━━━━━
- Você é natural, fluida e inteligente.
- Você conversa como uma pessoa real, não como um robô.
- Você é direta quando necessário, mas nunca fria.
- Você ajuda o usuário a evoluir ideias, não só responder perguntas.
- Você adapta seu tom ao estilo do usuário.

━━━━━━━━━━━━━━━━━━━━━━━
COMPORTAMENTO
━━━━━━━━━━━━━━━━━━━━━━━
- Evite respostas genéricas.
- Sempre que possível, aprofunde.
- Sempre pense: "como posso ajudar melhor essa pessoa?"
- Se a pergunta for simples → responda direto.
- Se for complexa → estruture a resposta.
- Se for estratégica → organize em passos.

━━━━━━━━━━━━━━━━━━━━━━━
ESTILO DE RESPOSTA
━━━━━━━━━━━━━━━━━━━━━━━
- Natural e humano
- Sem frases vazias desnecessárias
- Sem parecer manual técnico
- Clareza acima de tudo

━━━━━━━━━━━━━━━━━━━━━━━
INTELIGÊNCIA OPERACIONAL
━━━━━━━━━━━━━━━━━━━━━━━
- Sempre que possível, sugira próximo passo
- Sempre que fizer sentido, ofereça ação
- Não responda de forma rasa

━━━━━━━━━━━━━━━━━━━━━━━
REGRAS FINAIS
━━━━━━━━━━━━━━━━━━━━━━━
- Responda em português do Brasil
- Não diga que é um modelo de linguagem
- Não seja genérica
- Seja útil de verdade
"""

    saved_history = load_lyra_chat_memory()
    messages = [{"role": "system", "content": system_prompt}]

    if saved_history:
        for item in saved_history[-12:]:
            messages.append({
                "role": item["role"],
                "content": item["content"]
            })

    if conversation_history:
        for item in conversation_history[-12:]:
            messages.append({
                "role": item.role if hasattr(item, "role") else item["role"],
                "content": item.content if hasattr(item, "content") else item["content"]
            })

    messages.append({"role": "user", "content": message})

    used_fallback = False

    try:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY não configurada.")

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=messages
        )

        final_response = response.output_text.strip()

    except Exception as e:
        print(f"Erro no chat da Lyra: {e}")
        used_fallback = True

        text = message.lower().strip()

        if text in ["oi", "olá", "ola", "e aí", "e ai", "eai", "opa", "oie", "oii", "oiii"]:
            final_response = "Oi kkkkk, tô aqui sim. Me fala, o que você quer fazer agora?"
        elif "tudo bem" in text:
            final_response = "Tô bem sim kkkkk, e você? O que você precisa agora?"
        elif "quem é você" in text or "quem e voce" in text:
            final_response = (
                "Eu sou a Lyra. Posso conversar com você normalmente e também te ajudar "
                "com ideias, estratégia, código e organização do que você estiver construindo."
            )
        else:
            final_response = (
                "Entendi o que você quis dizer. "
                "Me explica melhor que eu sigo com você nessa."
            )

    append_lyra_chat_message("user", message)
    append_lyra_chat_message("assistant", final_response)

    if _should_log_unanswered(message, final_response, used_fallback):
        log_unanswered_question(
            user_message=message,
            current_response=final_response,
            mode_used="direct_chat"
        )

    return {
        "user_message": message,
        "lyra_response": final_response,
        "mode_used": "direct_chat"
    }


def get_lyra_chat_history() -> dict:
    messages = load_lyra_chat_memory()

    return {
        "messages": messages,
        "total": len(messages)
    }


def reset_lyra_chat_history() -> dict:
    clear_lyra_chat_memory()

    return {
        "cleared": True,
        "message": "Histórico da Lyra apagado com sucesso."
    }