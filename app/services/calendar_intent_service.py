import re
from datetime import datetime, timedelta


def detect_calendar_intent(message: str):
    text = message.lower().strip()

    trigger_words = [
        "tenho uma reunião",
        "tenho um compromisso",
        "marcar reunião",
        "marcar compromisso",
        "agendar",
        "agenda",
        "cliente",
        "visita",
    ]

    if not any(word in text for word in trigger_words):
        return None

    now = datetime.now()

    # -------------------------
    # 🧠 RELATIVO: "daqui 30 minutos"
    # -------------------------
    match_minutes = re.search(r"daqui (\d+) minutos?", text)
    if match_minutes:
        minutes = int(match_minutes.group(1))
        event_dt = now + timedelta(minutes=minutes)

        return {
            "summary": message.strip(),
            "start_dt": event_dt,
            "duration_minutes": 60,
        }

    # -------------------------
    # 🧠 HOJE / AMANHÃ
    # -------------------------
    day_offset = 0

    if "amanhã" in text:
        day_offset = 1
    elif "hoje" in text:
        day_offset = 0

    # -------------------------
    # 🧠 HORÁRIO FLEXÍVEL
    # -------------------------
    time_match = re.search(r"(\d{1,2})(?::(\d{2}))?", text)

    if not time_match:
        return None

    hour = int(time_match.group(1))
    minute = int(time_match.group(2) or 0)

    # -------------------------
    # 🧠 PERÍODO (manhã/tarde/noite)
    # -------------------------
    if "tarde" in text and hour < 12:
        hour += 12
    elif "noite" in text and hour < 12:
        hour += 12
    elif "manhã" in text and hour == 12:
        hour = 0

    event_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    event_dt += timedelta(days=day_offset)

    # se ficou no passado → joga pro próximo dia
    if event_dt < now:
        event_dt += timedelta(days=1)

    return {
        "summary": message.strip(),
        "start_dt": event_dt,
        "duration_minutes": 60,
    }