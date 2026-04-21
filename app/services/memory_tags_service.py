from typing import Dict, List
from app.services.llm.openai_client import client
from app.core.settings import OPENAI_API_KEY, OPENAI_MODEL
from app.data.store.memory_tags_store import load_tags, save_tags


def extract_tags(agent_name: str, recent_messages: List[Dict]) -> Dict:
    existing_tags = load_tags(agent_name)

    try:
        if not OPENAI_API_KEY:
            raise ValueError("Sem API")

        prompt = f"""
Você é um sistema que extrai informações importantes da conversa.

Tags existentes:
{existing_tags}

Mensagens recentes:
{recent_messages}

Extraia ou atualize as seguintes categorias (se fizer sentido):
- objetivo_usuario
- preferencia_tom
- tipo_negocio
- tarefa_ativa
- problema_principal

Retorne apenas JSON válido.
"""

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=[
                {"role": "system", "content": "Extraia tags estruturadas."},
                {"role": "user", "content": prompt}
            ]
        )

        raw = response.output_text.strip()

        import json
        new_tags = json.loads(raw)

    except Exception as e:
        print("Erro tags:", e)

        # fallback simples
        new_tags = existing_tags

        if recent_messages:
            last = recent_messages[-1]["content"].lower()

            if "humano" in last:
                new_tags["preferencia_tom"] = "mais humano"

            if "imobili" in last:
                new_tags["tipo_negocio"] = "imobiliária"

    # merge inteligente
    merged = {**existing_tags, **new_tags}

    return save_tags(agent_name, merged)