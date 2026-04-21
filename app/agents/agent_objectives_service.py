from typing import Dict, List
from app.services.llm.openai_client import client
from app.core.settings import OPENAI_API_KEY, OPENAI_MODEL
from app.data.store.agent_objectives_store import load_objectives, save_objectives


def _get_last_user_message(recent_messages: List[Dict]) -> str:
    for message in reversed(recent_messages):
        if message.get("role") == "user":
            return message.get("content", "").strip()
    return ""


def update_objectives(agent_name: str, recent_messages: List[Dict]) -> Dict:
    existing = load_objectives(agent_name)

    try:
        if not OPENAI_API_KEY:
            raise ValueError("Sem API")

        prompt = f"""
Você atualiza objetivos de um agente.

Objetivos atuais:
{existing}

Mensagens recentes:
{recent_messages}

Atualize ou defina:
- objetivo_principal
- objetivo_atual
- meta_curto_prazo
- status

Regras:
- Responda apenas JSON válido.
- Seja curto, claro e objetivo.
- Não copie respostas longas do agente.
- Foque na intenção do usuário.
"""

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=[
                {"role": "system", "content": "Gerencie objetivos persistentes do agente em JSON limpo."},
                {"role": "user", "content": prompt}
            ]
        )

        import json
        new_data = json.loads(response.output_text.strip())

    except Exception as e:
        print("Erro objetivos:", e)

        new_data = existing.copy()
        last_user_message = _get_last_user_message(recent_messages).lower()

        if last_user_message:
            if "imobili" in last_user_message:
                new_data["objetivo_principal"] = "Melhorar atendimento imobiliário"

            if "humano" in last_user_message:
                new_data["objetivo_atual"] = "Tornar a comunicação mais humana"

            if "lead" in last_user_message or "mensagens" in last_user_message:
                new_data["meta_curto_prazo"] = "Ajustar mensagens de atendimento"

            if "melhorar" in last_user_message:
                new_data["status"] = "em andamento"

        if not new_data.get("status"):
            new_data["status"] = "em andamento"

    merged = {**existing, **new_data}

    return save_objectives(agent_name, merged)