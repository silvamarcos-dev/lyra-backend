from app.core.settings import OPENAI_API_KEY, OPENAI_MODEL
from app.services.llm.openai_client import client
from app.data.store.memory_store import append_message, get_recent_memory
from app.data.store.memory_summary_store import load_memory_summary
from app.services.memory_summary_service import update_agent_summary
from app.data.store.memory_tags_store import load_tags
from app.services.memory_tags_service import extract_tags
from app.data.store.agent_objectives_store import load_objectives
from app.agents.agent_objectives_service import update_objectives


def build_agent_response(agent_data: dict, user_message: str) -> str:
    agent_name = agent_data.get("name", "Agente")
    agent_goal = agent_data.get("goal", "")
    personality = agent_data.get("personality", "")
    base_prompt = agent_data.get("base_prompt", "")

    memory_summary_data = load_memory_summary(agent_name)
    memory_summary = memory_summary_data.get("summary", "")

    tags = load_tags(agent_name)
    objectives = load_objectives(agent_name)

    recent_memory = get_recent_memory(agent_name, limit=10)

    system_prompt = f"""
Você é {agent_name}.

OBJETIVO DO AGENTE:
{agent_goal}

OBJETIVOS PERSISTENTES:
{objectives}

PERSONALIDADE:
{personality}

PROMPT-BASE:
{base_prompt}

RESUMO DA MEMÓRIA:
{memory_summary}

TAGS DE MEMÓRIA:
{tags}

REGRAS:
- Responda em português do Brasil.
- Seja clara, objetiva e útil.
- Considere objetivos, resumo, tags e o histórico recente.
- Responda como esse agente especializado.
- Não diga que é um modelo de linguagem.
- Foque em resolver o pedido do usuário.
"""

    append_message(agent_name, "user", user_message)

    try:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY não configurada.")

        input_messages = [{"role": "system", "content": system_prompt}]

        for item in recent_memory:
            input_messages.append({
                "role": item["role"],
                "content": item["content"]
            })

        input_messages.append({
            "role": "user",
            "content": user_message
        })

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=input_messages
        )

        final_response = response.output_text.strip()

    except Exception as e:
        print(f"Erro OpenAI: {e}")
        final_response = (
            f"[Modo local] {agent_name}: considerando seu histórico resumido, "
            f"suas tags de memória, seus objetivos persistentes e sua mensagem "
            f"'{user_message}', vou continuar te orientando dentro do objetivo "
            f"'{agent_goal}'."
        )

    append_message(agent_name, "assistant", final_response)

    updated_messages = get_recent_memory(agent_name, limit=12)
    update_agent_summary(agent_name, updated_messages)
    extract_tags(agent_name, updated_messages)
    update_objectives(agent_name, updated_messages)

    return final_response