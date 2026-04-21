from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from app.core.database import Base


class AgentMemory(Base):
    __tablename__ = "agent_memories"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False, index=True)
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AgentMemorySummary(Base):
    __tablename__ = "agent_memory_summaries"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False, unique=True, index=True)
    summary = Column(Text, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AgentMemoryTag(Base):
    __tablename__ = "agent_memory_tags"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False, index=True)
    tag = Column(String(100), nullable=False)


class AgentObjective(Base):
    __tablename__ = "agent_objectives"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False, index=True)
    objective = Column(Text, nullable=False)