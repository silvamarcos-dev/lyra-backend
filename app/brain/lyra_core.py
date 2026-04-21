from typing import Any, Dict

from app.agents.registry import AgentRegistry
from app.brain.decision_engine import build_execution_plan
from app.brain.fallback_engine import execute_with_fallback
from app.brain.intent_engine import detect_intent
from app.brain.response_engine import finalize_response
from app.schemas.agent import AgentInput
from app.schemas.orchestration import LyraResult


class LyraCore:
    def __init__(
        self,
        registry: AgentRegistry,
        memory_service: Any | None = None,
        trace_service: Any | None = None,
    ) -> None:
        self.registry = registry
        self.memory_service = memory_service
        self.trace_service = trace_service

    def _load_memory_context(self, user_message: str) -> Dict[str, Any]:
        if self.memory_service and hasattr(self.memory_service, "load_memory_context"):
            try:
                return self.memory_service.load_memory_context(user_message)
            except Exception:
                return {}
        return {}

    def _save_interaction(
        self,
        user_message: str,
        assistant_response: str,
        intent: str,
        metadata: Dict[str, Any]
    ) -> None:
        if self.memory_service and hasattr(self.memory_service, "save_interaction"):
            try:
                self.memory_service.save_interaction(
                    user_message=user_message,
                    assistant_response=assistant_response,
                    intent=intent,
                    metadata=metadata,
                )
            except Exception:
                pass

    def process_message(self, user_message: str) -> LyraResult:
        if self.trace_service and hasattr(self.trace_service, "log"):
            self.trace_service.log("message_received", {"message": user_message})

        memory_context = self._load_memory_context(user_message)

        intent = detect_intent(user_message, memory_context)

        if self.trace_service and hasattr(self.trace_service, "log"):
            self.trace_service.log("intent_detected", {"intent": intent})

        plan = build_execution_plan(user_message, intent)

        if self.trace_service and hasattr(self.trace_service, "log"):
            self.trace_service.log("execution_plan_built", plan.model_dump())

        agent_input = AgentInput(
            user_message=user_message,
            memory_context=memory_context if plan.use_memory else {},
            metadata={
                "intent": intent,
                "use_web": plan.use_web,
                "response_mode": plan.response_mode,
            },
        )

        raw_output, used_fallback = execute_with_fallback(
            registry=self.registry,
            plan=plan,
            agent_input=agent_input
        )

        final_response = finalize_response(
            user_message=user_message,
            output=raw_output,
            response_mode=plan.response_mode,
        )

        if plan.store_memory:
            self._save_interaction(
                user_message=user_message,
                assistant_response=final_response,
                intent=intent,
                metadata={
                    "agent_used": raw_output.source_agent,
                    "used_fallback": used_fallback,
                    "plan": plan.model_dump(),
                },
            )

        if self.trace_service and hasattr(self.trace_service, "log"):
            self.trace_service.log(
                "response_generated",
                {
                    "agent_used": raw_output.source_agent,
                    "used_fallback": used_fallback,
                    "success": raw_output.success,
                },
            )

        return LyraResult(
            response=final_response,
            intent=intent,
            agent_used=raw_output.source_agent,
            success=raw_output.success,
            used_fallback=used_fallback,
            metadata=raw_output.metadata,
        )