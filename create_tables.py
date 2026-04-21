from app.core.database import Base, engine
from app.models.user import User
from app.models.whatsapp_log import WhatsAppMessageLog
from app.models.legal import LegalDocument, UserLegalAcceptance
from app.models.agent import Agent
from app.models.lyra_chat import LyraChatMessage
from app.models.agent_memory import (
    AgentMemory,
    AgentMemorySummary,
    AgentMemoryTag,
    AgentObjective,
)
from app.models.reminder import Reminder
from app.models.calendar_connection import CalendarConnection

Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso 🚀")