from sqlalchemy.orm import Session
from app.models.agent import Agent


def create_agent(
    db: Session,
    name: str,
    role: str,
    specialty: str,
    goal: str,
    description: str,
):
    agent = Agent(
        name=name,
        role=role,
        specialty=specialty,
        goal=goal,
        description=description,
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent


def list_agents(db: Session):
    return db.query(Agent).order_by(Agent.name.asc()).all()


def get_agent_by_name(db: Session, agent_name: str):
    return db.query(Agent).filter(Agent.name == agent_name).first()