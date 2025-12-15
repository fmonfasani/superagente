from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def planner_agent(state: dict):
    prompt = f"Divide esta tarea en pasos:\n{state['input']}"
    res = llm.invoke(prompt)

    return {
        "input": state["input"],   # 🔴 PRESERVAR
        "plan": res.content
    }
