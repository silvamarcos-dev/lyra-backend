from app.brain.intent_engine import detect_intent
from app.brain.decision_engine import build_execution_plan


def analyze_message(user_message: str):
    intent = detect_intent(user_message)
    plan = build_execution_plan(user_message, intent)
    return plan


def process_user_message(user_message: str):
    return analyze_message(user_message)