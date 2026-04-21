import json
import re
from pathlib import Path
from typing import Dict, List


BASE_DIR = Path(__file__).resolve().parent
MEMORIES_DIR = BASE_DIR / "memories"


def _ensure_memories_dir() -> None:
    MEMORIES_DIR.mkdir(parents=True, exist_ok=True)


def _normalize_agent_name(agent_name: str) -> str:
    normalized = agent_name.strip().lower()
    normalized = re.sub(r"\s+", "_", normalized)
    normalized = re.sub(r"[^a-z0-9_]", "", normalized)
    return normalized


def _get_memory_file(agent_name: str) -> Path:
    _ensure_memories_dir()
    filename = f"{_normalize_agent_name(agent_name)}.json"
    return MEMORIES_DIR / filename


def load_agent_memory(agent_name: str) -> List[Dict]:
    memory_file = _get_memory_file(agent_name)

    if not memory_file.exists():
        return []

    try:
        content = memory_file.read_text(encoding="utf-8").strip()

        if not content:
            return []

        data = json.loads(content)

        if isinstance(data, list):
            return data

        return []
    except (json.JSONDecodeError, OSError):
        return []


def save_agent_memory(agent_name: str, messages: List[Dict]) -> None:
    memory_file = _get_memory_file(agent_name)

    memory_file.write_text(
        json.dumps(messages, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )


def append_message(agent_name: str, role: str, content: str) -> List[Dict]:
    messages = load_agent_memory(agent_name)

    messages.append({
        "role": role,
        "content": content.strip()
    })

    save_agent_memory(agent_name, messages)
    return messages


def clear_agent_memory(agent_name: str) -> None:
    memory_file = _get_memory_file(agent_name)

    if memory_file.exists():
        memory_file.unlink()


def get_recent_memory(agent_name: str, limit: int = 10) -> List[Dict]:
    messages = load_agent_memory(agent_name)
    return messages[-limit:]