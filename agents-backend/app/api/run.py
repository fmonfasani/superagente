from fastapi import APIRouter
from app.graphs.main_graph import build_graph
from app.schemas.task import TaskRequest

router = APIRouter()
graph = build_graph()

@router.post("/run")
def run(task: TaskRequest):
    return graph.invoke({"input": task.input})
