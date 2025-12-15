from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def agent(state: dict):
    res = llm.invoke(state["input"])
    return {"output": res.content}

def build_graph():
    graph = StateGraph(dict)
    graph.add_node("agent", agent)
    graph.set_entry_point("agent")
    graph.set_finish_point("agent")
    return graph.compile()
