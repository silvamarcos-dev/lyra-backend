from app.agents.base_agent import BaseAgent
from app.schemas.agent import AgentInput, AgentOutput


class SerpAgent(BaseAgent):
    name = "serp"

    def __init__(self, web_search_service):
        self.web_search_service = web_search_service

    def run(self, agent_input: AgentInput) -> AgentOutput:
        result = self.web_search_service.search_web(agent_input.user_message)

        return AgentOutput(
            content=result,
            source_agent=self.name,
            success=True
        )