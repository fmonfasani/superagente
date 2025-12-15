from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def code_agent(state: dict):
    prompt = f"""
Generá código de calidad producción para la siguiente tarea:

{state["input"]}
"""
    res = llm.invoke(prompt)
    return {"output": res.content}
