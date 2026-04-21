from typing import List, Dict, Any


def evaluate_supervisor_mode(user_message: str) -> str:
    text = user_message.lower()

    if any(word in text for word in ["equipe", "time", "multiagente", "multi-agente"]):
        return "team"

    if any(word in text for word in ["colaborativo", "colaboração", "colaboracao"]):
        return "collaborative"

    return "auto"


def evaluate_agent_steps(team_outputs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Avalia as etapas executadas pelos agentes e devolve uma lista padronizada.
    """
    steps = []

    for item in team_outputs:
        agent_name = item.get("agent_name") or item.get("name") or "agente"
        response = item.get("response") or item.get("content") or item.get("result") or ""
        success = item.get("success", True)

        status = "completed" if success else "failed"

        steps.append(
            {
                "agent_name": agent_name,
                "action": item.get("action", "execution"),
                "result": response,
                "response": response,
                "status": status,
                "success": success,
            }
        )

    return steps


def build_supervisor_final_response(
    user_message: str,
    team_outputs: List[Dict[str, Any]],
    selected_agents: List[str] | None = None,
) -> str:
    """
    Monta uma resposta final consolidada com base nas saídas dos agentes.
    """
    if not team_outputs:
        return (
            "Analisei a solicitação, mas a equipe não retornou resultados suficientes "
            "para montar uma resposta final."
        )

    parts = []
    for item in team_outputs:
        agent_name = item.get("agent_name") or item.get("name") or "agente"
        response = item.get("response") or item.get("content") or item.get("result") or ""

        if response:
            parts.append(f"[{agent_name}] {response}")

    if not parts:
        return (
            "A equipe foi acionada, mas ainda não houve conteúdo suficiente "
            "para consolidar uma resposta final."
        )

    final_text = "\n\n".join(parts)

    if selected_agents:
        agents_text = ", ".join(selected_agents)
        return (
            f"Lyra coordenou os agentes: {agents_text}.\n\n"
            f"Solicitação: {user_message}\n\n"
            f"Resultado consolidado:\n{final_text}"
        )

    return (
        f"Solicitação: {user_message}\n\n"
        f"Resultado consolidado:\n{final_text}"
    )