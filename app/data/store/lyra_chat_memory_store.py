import json
from pathlib import Path
from typing import List, Dict


BASE_DIR = Path(__file__).resolve().parent
CHAT_MEMORY_FILE = BASE_DIR / "lyra_chat_memory.json"


def _ensure_memory_file() -> None:
    if not CHAT_MEMORY_FILE.exists():
        CHAT_MEMORY_FILE.write_text("[]", encoding="utf-8")


def load_lyra_chat_memory() -> List[Dict]:
    _ensure_memory_file()

    try:
        content = CHAT_MEMORY_FILE.read_text(encoding="utf-8").strip()

        if not content:
            return []

        data = json.loads(content)

        if isinstance(data, list):
            return data

        return []
    except (json.JSONDecodeError, OSError):
        return []


def save_lyra_chat_memory(messages: List[Dict]) -> None:
    _ensure_memory_file()

    CHAT_MEMORY_FILE.write_text(
        json.dumps(messages, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )


def append_lyra_chat_message(role: str, content: str) -> List[Dict]:
    messages = load_lyra_chat_memory()

    messages.append({
        "role": role,
        "content": content.strip()
    })

    save_lyra_chat_memory(messages)
    return messages


def clear_lyra_chat_memory() -> None:
    save_lyra_chat_memory([])