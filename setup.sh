#!/bin/bash
set -e

PROJECT_NAME=agents-backend
PYTHON_VERSION=3.11

echo "🚀 Creando proyecto $PROJECT_NAME"

mkdir $PROJECT_NAME
cd $PROJECT_NAME

# ---------- entorno ----------
python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip

# ---------- dependencias ----------
pip install \
  fastapi \
  uvicorn[standard] \
  langgraph \
  langchain \
  langchain-openai \
  python-dotenv \
  pydantic \
  redis \
  httpx

# ---------- estructura ----------
mkdir -p app/{api,agents,graphs,core,schemas,utils}
mkdir -p app/agents/{generator,reviewer,debugger}
mkdir -p tests

touch app/main.py
touch app/core/{config.py,logging.py}
touch app/api/agent_router.py
touch app/graphs/code_graph.py
touch app/utils/llm.py
touch .env
touch README.md

# ---------- agentes ----------
cat <<EOF > app/agents/generator/agent.py
from langchain_openai import ChatOpenAI

def generator_agent(state):
    llm = ChatOpenAI(model="gpt-4o-mini")
    result = llm.invoke(state["input"])
    return {"output": result.content}
EOF

cat <<EOF > app/agents/reviewer/agent.py
from langchain_openai import ChatOpenAI

def reviewer_agent(state):
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = f"Review this code:\\n{state['output']}"
    result = llm.invoke(prompt)
    return {"output": result.content}
EOF

cat <<EOF > app/agents/debugger/agent.py
from langchain_openai import ChatOpenAI

def debugger_agent(state):
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = f"Debug this code:\\n{state['output']}"
    result = llm.invoke(prompt)
    return {"output": result.content}
EOF

# ---------- LangGraph ----------
cat <<EOF > app/graphs/code_graph.py
from langgraph.graph import StateGraph
from app.agents.generator.agent import generator_agent
from app.agents.reviewer.agent import reviewer_agent
from app.agents.debugger.agent import debugger_agent

def build_graph():
    graph = StateGraph(dict)

    graph.add_node("generator", generator_agent)
    graph.add_node("reviewer", reviewer_agent)
    graph.add_node("debugger", debugger_agent)

    graph.set_entry_point("generator")
    graph.add_edge("generator", "reviewer")
    graph.add_edge("reviewer", "debugger")
    graph.set_finish_point("debugger")

    return graph.compile()
EOF

# ---------- API ----------
cat <<EOF > app/api/agent_router.py
from fastapi import APIRouter
from app.graphs.code_graph import build_graph

router = APIRouter()
graph = build_graph()

@router.post("/run")
def run_agent(payload: dict):
    return graph.invoke({"input": payload["input"]})
EOF

# ---------- main ----------
cat <<EOF > app/main.py
from fastapi import FastAPI
from app.api.agent_router import router

app = FastAPI(title="Multi-Agent Backend")

app.include_router(router, prefix="/agent")
EOF

# ---------- config ----------
cat <<EOF > app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EOF

# ---------- env ----------
cat <<EOF > .env
OPENAI_API_KEY=sk-xxxxxxxx
EOF

echo "✅ Backend creado"
echo "▶️ Ejecutar:"
echo "source .venv/bin/activate"
echo "uvicorn app.main:app --reload"
