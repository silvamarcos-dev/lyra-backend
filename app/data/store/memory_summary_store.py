import json
import re
from pathlib import Path
from typing import Dict


BASE_DIR = Path(__file__).resolve().parent
SUMMARIES_DIR = BASE_DIR / "memory_summaries"


def _ensure_summaries_dir() -> None:
    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)


def _normalize_agent_name(agent_name: str) -> str:
    normalized = agent_name.strip().lower()
    normalized = re.sub(r"\s+", "_", normalized)
    normalized = re.sub(r"[^a-z0-9_]", "", normalized)
    return normalized


def _get_summary_file(agent_name: str) -> Path:
    _ensure_summaries_dir()
    filename = f"{_normalize_agent_name(agent_name)}_summary.json"
    return SUMMARIES_DIR / filename


def load_memory_summary(agent_name: str) -> Dict:
    summary_file = _get_summary_file(agent_name)

    if not summary_file.exists():
        return {
            "agent_name": agent_name,
            "summary": "",
            "updated_at": None
        }

    try:
        content = summary_file.read_text(encoding="utf-8").strip()

        if not content:
            return {
                "agent_name": agent_name,
                "summary": "",
                "updated_at": None
            }

        data = json.loads(content)

        if isinstance(data, dict):
            return data

        return {
            "agent_name": agent_name,
            "summary": "",
            "updated_at": None
        }
    except (json.JSONDecodeError, OSError):
        return {
            "agent_name": agent_name,
            "summary": "",
            "updated_at": None
        }


def save_memory_summary(agent_name: str, summary: str, updated_at: str) -> Dict:
    summary_file = _get_summary_file(agent_name)

    data = {
        "agent_name": agent_name,
        "summary": summary.strip(),
        "updated_at": updated_at
    }

    summary_file.write_text(
        json.dumps(data, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )

    return data


def clear_memory_summary(agent_name: str) -> None:
    summary_file = _get_summary_file(agent_name)

    if summary_file.exists():
        summary_file.unlink()