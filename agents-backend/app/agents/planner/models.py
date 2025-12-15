# planner/models.py
from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class PlannerInput:
    user_request: str
    constraints: Dict[str, Any]


@dataclass
class PlanStep:
    step_id: int
    agent: str
    task: str


@dataclass
class PlanResult:
    step_id: int
    agent: str
    task: str
    output: Dict[str, Any]
    duration_ms: float
