from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

SYSTEM_PROMPT = """
Sos un Architect Agent.
Tu tarea es DISEÑAR la solución.
- Definí estructura de carpetas
- Entidades principales
- Decisiones técnicas
NO escribas código.
Respondé en texto claro y estructurado.
"""

def architect_agent(state: dict):
    res = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": state["input"]},
    ])
    return {"output": res.content}
