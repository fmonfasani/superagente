from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def reasoning_agent(state: dict):
    prompt = f"""
Rol: {state.get("context", {}).get("agent")}

Contexto del problema:
{state.get("context", {}).get("request")}

Resultados previos:
{state.get("memory")}

Tarea actual:
{state["input"]}
"""

    res = llm.invoke(prompt)
    return {"output": res.content}
