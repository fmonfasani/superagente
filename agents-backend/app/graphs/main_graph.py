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
