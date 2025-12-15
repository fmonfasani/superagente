from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def task_agent(state):
    res = llm.invoke(state["input"])
    return {"output": res.content}
