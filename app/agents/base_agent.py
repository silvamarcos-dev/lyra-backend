from abc import ABC, abstractmethod
from app.schemas.agent import AgentInput, AgentOutput


class BaseAgent(ABC):
    name: str = "base"

    @abstractmethod
    def run(self, agent_input: AgentInput) -> AgentOutput:
        raise NotImplementedError