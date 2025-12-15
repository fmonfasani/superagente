from typing import Dict, List, Literal
from pydantic import BaseModel, Field


AgentType = Literal[
    "architect",
    "backend",
    "code",
    "reviewer"
]


class PlannerInput(BaseModel):
    input: str = Field(..., description="Pedido del usuario")
    constraints: Dict = Field(default_factory=dict)


class PlanStep(BaseModel):
    id: int
    agent: AgentType
    goal: str


class Plan(BaseModel):
    input: str
    steps: List[PlanStep]
