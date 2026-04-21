import json
import re
from pathlib import Path
from typing import Dict


BASE_DIR = Path(__file__).resolve().parent
TAGS_DIR = BASE_DIR / "memory_tags"


def _ensure_tags_dir():
    TAGS_DIR.mkdir(parents=True, exist_ok=True)


def _normalize_name(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^a-z0-9_]", "", name)
    return name


def _get_file(agent_name: str) -> Path:
    _ensure_tags_dir()
    filename = f"{_normalize_name(agent_name)}_tags.json"
    return TAGS_DIR / filename


def load_tags(agent_name: str) -> Dict:
    file = _get_file(agent_name)

    if not file.exists():
        return {}

    try:
        return json.loads(file.read_text(encoding="utf-8"))
    except:
        return {}


def save_tags(agent_name: str, tags: Dict) -> Dict:
    file = _get_file(agent_name)

    file.write_text(
        json.dumps(tags, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )

    return tags