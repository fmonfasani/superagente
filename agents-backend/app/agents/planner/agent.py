from langchain_openai import ChatOpenAI
import json

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

SYSTEM_PROMPT = """
Sos un Planner Agent.
Tu única tarea es dividir una tarea en pasos ordenados.
NO ejecutes código.
NO expliques nada.
Respondé SOLO JSON válido.
"""

def planner_agent(state: dict):
    user_task = state["input"]

    prompt = f"""
Tarea:
{user_task}

Formato de salida:
[
  { "step": 1, "agent": "architect", "task": "definir estructura de proyecto" },
  { "step": 2, "agent": "backend", "task": "definir modelos SQLAlchemy" },
  { "step": 3, "agent": "backend", "task": "definir esquemas Pydantic" },
  { "step": 4, "agent": "backend", "task": "crear endpoints CRUD FastAPI" },
  { "step": 5, "agent": "reviewer", "task": "validar stack y coherencia" }
]

"""

    res = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ])

    try:
        plan = json.loads(res.content)
    except json.JSONDecodeError:
        # fallback seguro
        plan = [
            {
                "step": 1,
                "agent": "task",
                "goal": user_task
            }
        ]

    return {
        "input": user_task,   # 🔴 siempre preservar
        "plan": plan
    }
