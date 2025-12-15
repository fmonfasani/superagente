# app/schemas/task.py
from pydantic import BaseModel
from typing import Optional, Dict, Any


class TaskRequest(BaseModel):
    input: str
    constraints: Optional[Dict[str, Any]] = None
