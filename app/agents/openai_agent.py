from app.agents.base_agent import BaseAgent
from app.schemas.agent import AgentInput, AgentOutput


class OpenAIAgent(BaseAgent):
    name = "openai"

    def __init__(self, openai_client):
        self.openai_client = openai_client

    def run(self, agent_input: AgentInput) -> AgentOutput:
        content = self.openai_client.generate_response(
            message=agent_input.user_message,
            memory_context=agent_input.memory_context,
            metadata=agent_input.metadata,
        )

        return AgentOutput(
            content=content,
            source_agent=self.name,
            success=True
        )