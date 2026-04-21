
from app.core.settings import ANTHROPIC_API_KEY, CLAUDE_MODEL

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None


def build_agent(message: str) -> dict:
    if not ANTHROPIC_API_KEY or Anthropic is None:
        return {
            "success": False,
            "provider": "claude",
            "response": "",
            "error": "Claude/Anthropic não configurado."
        }

    try:
        client = Anthropic(api_key=ANTHROPIC_API_KEY)

        prompt = f"""
Você é um construtor de agentes da Lyra.

Com base no pedido do usuário, gere um agente em JSON com:
- name
- goal
- personality
- base_prompt
- initial_tags

Pedido do usuário:
{message}
"""

        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1200,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        text = response.content[0].text if response.content else ""

        return {
            "success": True,
            "provider": "claude",
            "response": text,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "provider": "claude",
            "response": "",
            "error": str(e)
        }