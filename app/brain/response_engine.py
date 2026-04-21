from app.schemas.agent import AgentOutput


def finalize_response(user_message: str, output: AgentOutput, response_mode: str = "default") -> str:
    content = (output.content or "").strip()

    if not content:
        return "Desculpe, não consegui gerar uma resposta válida agora."

    if response_mode == "short":
        return content

    if response_mode == "technical":
        return content

    if response_mode == "creative":
        return content

    if response_mode == "factual":
        return content

    if response_mode == "contextual":
        return content

    return content