from app.core.settings import OPENAI_API_KEY, OPENAI_MODEL
from app.services.llm.openai_client import client


def generate_response(message: str, messages: list | None = None) -> dict:
    if not OPENAI_API_KEY:
        return {
            "success": False,
            "provider": "openai",
            "response": "",
            "error": "OPENAI_API_KEY não configurada ou sem quota."
        }

    try:
        input_messages = messages if messages else [
            {"role": "user", "content": message}
        ]

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=input_messages
        )

        return {
            "success": True,
            "provider": "openai",
            "response": response.output_text.strip(),
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "provider": "openai",
            "response": "",
            "error": str(e)
        }