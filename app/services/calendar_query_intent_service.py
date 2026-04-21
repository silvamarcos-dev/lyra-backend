def detect_calendar_query_intent(message: str):
    text = message.lower().strip()

    triggers_today = [
        "o que tenho hoje",
        "minha agenda hoje",
        "mnh agenda hj",
        "agenda hoje",
        "agenda hj",
        "quais compromissos tenho hoje",
        "quais compromissos tenho hj",
        "meus compromissos hoje",
        "meus compromissos hj",
        "compromisso hoje",
        "compromisso hj",
    ]

    triggers_tomorrow = [
        "o que tenho amanha",
        "oq tenho amanha",
        "oq tenho amnh"
        "o que tenho amanhã",
        "minha agenda amanha",
        "minha agenda amanhã",
        "agenda amanha",
        "agenda amanhã",
        "quais compromissos tenho amanha",
        "quais compromissos tenho amanhã",
        "meus compromissos amanha",
        "meus compromissos amanhã",
        "compromisso amanha",
        "compromisso amanhã",
        
    ]

    if any(trigger in text for trigger in triggers_today):
        return {"period": "today"}

    if any(trigger in text for trigger in triggers_tomorrow):
        return {"period": "tomorrow"}

    return None