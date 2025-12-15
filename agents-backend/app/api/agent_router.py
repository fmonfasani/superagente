from fastapi import APIRouter
from app.graphs.code_graph import build_graph
from app.schemas.agent import AgentRequest

router = APIRouter()
graph = build_graph()

@router.post("/run")
def run(payload: AgentRequest):
    return graph.invoke({"input": payload.input})
