from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent
UNANSWERED_FILE = BASE_DIR / "unanswered_questions.txt"


def log_unanswered_question(user_message: str, current_response: str, mode_used: str) -> None:
    UNANSWERED_FILE.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    block = (
        "\n========================================\n"
        f"DATA: {timestamp}\n"
        f"MODO: {mode_used}\n"
        f"USUÁRIO: {user_message.strip()}\n"
        f"RESPOSTA_ATUAL: {current_response.strip()}\n"
        "STATUS: pendente\n"
        "========================================\n"
    )

    with open(UNANSWERED_FILE, "a", encoding="utf-8") as file:
        file.write(block)