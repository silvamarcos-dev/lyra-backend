from typing import Dict
from app.agents.base_agent import BaseAgent


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: Dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        self._agents[agent.name] = agent

    def get(self, agent_name: str) -> BaseAgent:
        if agent_name not in self._agents:
            raise ValueError(f"Agente '{agent_name}' não registrado.")
        return self._agents[agent_name]

    def has(self, agent_name: str) -> bool:
        return agent_name in self._agents

    def list_agents(self) -> list[str]:
        return list(self._agents.keys())