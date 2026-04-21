import json
from pathlib import Path
from typing import Dict, List, Optional


BASE_DIR = Path(__file__).resolve().parent
AGENTS_FILE = BASE_DIR / "agents.json"


def _ensure_agents_file() -> None:
    if not AGENTS_FILE.exists():
        AGENTS_FILE.write_text("[]", encoding="utf-8")


def _read_agents() -> List[Dict]:
    _ensure_agents_file()

    try:
        content = AGENTS_FILE.read_text(encoding="utf-8").strip()

        if not content:
            return []

        data = json.loads(content)

        if isinstance(data, list):
            return data

        return []
    except (json.JSONDecodeError, OSError):
        return []


def _write_agents(agents: List[Dict]) -> None:
    AGENTS_FILE.write_text(
        json.dumps(agents, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )


def save_agent(agent_data: Dict) -> Dict:
    agents = _read_agents()
    normalized_name = agent_data.get("name", "").strip().lower()

    existing_index = None

    for index, agent in enumerate(agents):
        if agent.get("name", "").strip().lower() == normalized_name:
            existing_index = index
            break

    if existing_index is not None:
        agents[existing_index] = agent_data
    else:
        agents.append(agent_data)

    _write_agents(agents)
    return agent_data


def list_agents() -> List[Dict]:
    return _read_agents()


def get_agent_by_name(name: str) -> Optional[Dict]:
    normalized_name = name.strip().lower()

    for agent in _read_agents():
        if agent.get("name", "").strip().lower() == normalized_name:
            return agent

    return None