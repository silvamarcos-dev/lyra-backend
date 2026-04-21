from sqlalchemy import Column, String, Text
from app.core.database import Base
import uuid

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    role = Column(String, nullable=True)
    specialty = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    goal = Column(Text, nullable=False)