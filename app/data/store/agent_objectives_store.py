import json
import re
from pathlib import Path
from typing import Dict


BASE_DIR = Path(__file__).resolve().parent
OBJECTIVES_DIR = BASE_DIR / "agent_objectives"


def _ensure_dir():
    OBJECTIVES_DIR.mkdir(parents=True, exist_ok=True)


def _normalize(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^a-z0-9_]", "", name)
    return name


def _file(agent_name: str) -> Path:
    _ensure_dir()
    return OBJECTIVES_DIR / f"{_normalize(agent_name)}_objectives.json"


def load_objectives(agent_name: str) -> Dict:
    f = _file(agent_name)

    if not f.exists():
        return {}

    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except:
        return {}


def save_objectives(agent_name: str, data: Dict) -> Dict:
    f = _file(agent_name)

    f.write_text(
        json.dumps(data, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )

    return data