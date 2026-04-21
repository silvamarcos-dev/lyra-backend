from datetime import datetime
from typing import List, Dict

from app.core.settings import OPENAI_API_KEY, OPENAI_MODEL
from app.services.llm.openai_client import client
from app.data.store.memory_summary_store import load_memory_summary, save_memory_summary


def _build_summary_prompt(
    agent_name: str,
    existing_summary: str,
    recent_messages: List[Dict]
) -> str:
    parts = []

    parts.append(f"Nome do agente: {agent_name}")

    if existing_summary.strip():
        parts.append(f"Resumo anterior: {existing_summary.strip()}")
    else:
        parts.append("Resumo anterior: vazio")

    parts.append("Mensagens recentes:")

    for message in recent_messages:
        role = message.get("role", "unknown")
        content = message.get("content", "").strip()

        if not content:
            continue

        if role == "user":
            parts.append(f"Usuário: {content}")
        elif role == "assistant":
            parts.append(f"Agente: {content}")
        else:
            parts.append(f"{role}: {content}")

    parts.append(
        "Crie um resumo inteligente, curto e útil da conversa. "
        "Mantenha objetivos do usuário, contexto importante, preferências, "
        "tarefas em andamento e decisões relevantes. "
        "Escreva em português do Brasil. "
        "Não repita tudo literalmente. "
        "Limite a resposta a no máximo 1200 caracteres."
    )

    return "\n".join(parts)


def _generate_local_summary(existing_summary: str, recent_messages: List[Dict]) -> str:
    parts = []

    if existing_summary.strip():
        parts.append(f"Resumo anterior: {existing_summary.strip()}")

    if recent_messages:
        parts.append("Atualizações recentes:")

        for message in recent_messages[-6:]:
            role = message.get("role", "unknown")
            content = message.get("content", "").strip()

            if not content:
                continue

            if role == "user":
                parts.append(f"Usuário pediu: {content}")
            elif role == "assistant":
                parts.append(f"Agente respondeu: {content}")

    summary = " | ".join(parts).strip()

    if len(summary) > 1200:
        summary = summary[-1200:]

    return summary


def update_agent_summary(agent_name: str, recent_messages: List[Dict]) -> Dict:
    current_data = load_memory_summary(agent_name)
    current_summary = current_data.get("summary", "")

    try:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY não configurada.")

        prompt = _build_summary_prompt(
            agent_name=agent_name,
            existing_summary=current_summary,
            recent_messages=recent_messages
        )

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Você é um sistema de memória para agentes de IA. "
                        "Sua função é condensar conversas em um resumo útil, "
                        "claro e acionável."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        new_summary = response.output_text.strip()

        if len(new_summary) > 1200:
            new_summary = new_summary[:1200]

    except Exception as e:
        print(f"Erro ao gerar resumo inteligente com IA: {e}")
        new_summary = _generate_local_summary(current_summary, recent_messages)

    updated_at = datetime.utcnow().isoformat()

    return save_memory_summary(
        agent_name=agent_name,
        summary=new_summary,
        updated_at=updated_at
    )