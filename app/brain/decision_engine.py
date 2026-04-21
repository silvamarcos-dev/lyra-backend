from app.schemas.orchestration import ExecutionPlan


def build_execution_plan(user_message: str, intent: str) -> ExecutionPlan:
    if intent == "search":
        return ExecutionPlan(
            intent=intent,
            primary_agent="serpapi",
            fallback_agents=["openai", "claude"],
            use_memory=True,
            use_web=True,
            use_multi_agent=False,
            store_memory=True,
            response_mode="factual"
        )

    if intent == "creative":
        return ExecutionPlan(
            intent=intent,
            primary_agent="claude",
            fallback_agents=["openai"],
            use_memory=True,
            use_web=False,
            use_multi_agent=False,
            store_memory=True,
            response_mode="creative"
        )

    if intent == "code":
        return ExecutionPlan(
            intent=intent,
            primary_agent="openai",
            fallback_agents=["claude", "gemini"],
            use_memory=True,
            use_web=False,
            use_multi_agent=False,
            store_memory=True,
            response_mode="technical"
        )

    if intent == "memory":
        return ExecutionPlan(
            intent=intent,
            primary_agent="openai",
            fallback_agents=["claude"],
            use_memory=True,
            use_web=False,
            use_multi_agent=False,
            store_memory=False,
            response_mode="contextual"
        )

    if intent == "agent_builder":
        return ExecutionPlan(
            intent=intent,
            primary_agent="claude",
            fallback_agents=["openai"],
            use_memory=True,
            use_web=False,
            use_multi_agent=False,
            store_memory=True,
            response_mode="agent_creation"
        )

    if intent == "agent_management":
        return ExecutionPlan(
            intent=intent,
            primary_agent="claude",
            fallback_agents=["openai"],
            use_memory=True,
            use_web=False,
            use_multi_agent=False,
            store_memory=True,
            response_mode="strategic"
        )

    if intent == "quick_chat":
        return ExecutionPlan(
            intent=intent,
            primary_agent="openai",
            fallback_agents=["claude"],
            use_memory=True,
            use_web=False,
            use_multi_agent=False,
            store_memory=True,
            response_mode="short"
        )

    return ExecutionPlan(
        intent="general",
        primary_agent="openai",
        fallback_agents=["claude", "gemini"],
        use_memory=True,
        use_web=False,
        use_multi_agent=False,
        store_memory=True,
        response_mode="default"
    )