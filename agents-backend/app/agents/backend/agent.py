from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

SYSTEM_PROMPT = """
Sos un Backend Agent.
Tu tarea es definir CONTRATOS técnicos:
- Modelos de datos
- Schemas (Pydantic)
- Endpoints (paths, métodos, inputs/outputs)
NO escribas implementación completa.
NO frontend.
"""

def backend_agent(state: dict):
    res = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": state["input"]},
    ])
    return {"output": res.content}
