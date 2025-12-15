#!/bin/bash
set -e

PROJECT=agents-backend

echo "🚀 Creando backend de agentes: $PROJECT"

mkdir -p $PROJECT/app/{api,agents,graphs,schemas}
mkdir -p $PROJECT/app/agents/{task,code,planner,orchestrator}
mkdir -p $PROJECT/tests

# ---------- requirements ----------
cat <<EOF > $PROJECT/requirements.txt
fastapi
uvicorn[standard]
langgraph
langchain
langchain-openai
pydantic
python-dotenv
EOF

# ---------- schema ----------
cat <<EOF > $PROJECT/app/schemas/task.py
from pydantic import BaseModel

class TaskRequest(BaseModel):
    input: str
EOF

# ---------- TASK AGENT ----------
cat <<EOF > $PROJECT/app/agents/task/agent.py
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def task_agent(state):
    res = llm.invoke(state["input"])
    return {"output": res.content}
EOF

# ---------- CODE AGENT ----------
cat <<EOF > $PROJECT/app/agents/code/agent.py
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def code_agent(state):
    prompt = f"Generate clean production code for:\\n{state['input']}"
    res = llm.invoke(prompt)
    return {"output": res.content}
EOF

# ---------- PLANNER AGENT ----------
cat <<EOF > $PROJECT/app/agents/planner/agent.py
from langchain_openai import ChatOpenAI
import json

llm = ChatOpenAI(model="gpt-4o-mini")

def planner_agent(state):
    prompt = f"""
Divide this task into ordered steps.
Respond ONLY as JSON array.

Task:
{state["input"]}
"""
    res = llm.invoke(prompt)
    return {"plan": res.content}
EOF

# ---------- ORCHESTRATOR ----------
cat <<EOF > $PROJECT/app/agents/orchestrator/agent.py
from app.agents.task.agent import task_agent
from app.agents.code.agent import code_agent

def orchestrator(state):
    # simple strategy: code if mentions code, else task
    if "code" in state["input"].lower():
        return code_agent(state)
    return task_agent(state)
EOF

# ---------- LANGGRAPH ----------
cat <<EOF > $PROJECT/app/graphs/main_graph.py
from langgraph.graph import StateGraph
from app.agents.planner.agent import planner_agent
from app.agents.orchestrator.agent import orchestrator

def build_graph():
    g = StateGraph(dict)

    g.add_node("planner", planner_agent)
    g.add_node("orchestrator", orchestrator)

    g.set_entry_point("planner")
    g.add_edge("planner", "orchestrator")
    g.set_finish_point("orchestrator")

    return g.compile()
EOF

# ---------- API ----------
cat <<EOF > $PROJECT/app/api/run.py
from fastapi import APIRouter
from app.graphs.main_graph import build_graph
from app.schemas.task import TaskRequest

router = APIRouter()
graph = build_graph()

@router.post("/run")
def run(task: TaskRequest):
    return graph.invoke({"input": task.input})
EOF

# ---------- MAIN ----------
cat <<EOF > $PROJECT/app/main.py
from fastapi import FastAPI
from app.api.run import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Agent System")
app.include_router(router, prefix="/agent")
EOF

echo "✅ Estructura creada"
echo ""
echo "▶️ Siguiente:"
echo "cd $PROJECT"
echo "python -m venv .venv"
echo "source .venv/Scripts/activate  (PowerShell)"
echo "pip install -r requirements.txt"
echo "uvicorn app.main:app --reload"
