from langgraph.graph import StateGraph
from app.agents.planner.planner import Planner
from app.agents.planner.schema import PlannerInput
from app.agents.orchestrator.agent import orchestrator


planner = Planner()


def planner_node(state: dict):
    req = PlannerInput(**state)
    plan = planner.plan(req)
    return {"plan": plan}


def build_graph():
    g = StateGraph(dict)

    g.add_node("planner", planner_node)
    g.add_node("orchestrator", orchestrator)

    g.set_entry_point("planner")
    g.add_edge("planner", "orchestrator")
    g.set_finish_point("orchestrator")

    return g.compile()
