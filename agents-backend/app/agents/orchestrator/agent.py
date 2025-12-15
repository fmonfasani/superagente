from app.agents.planner.schema import Plan
from app.agents.architect.agent import architect_agent
from app.agents.backend.agent import backend_agent
from app.agents.code.agent import code_agent

AGENTS = {
    "architect": architect_agent,
    "backend": backend_agent,
    "code": code_agent,
    "reviewer": architect_agent,  # temporal
}

def orchestrator(state: dict):
    plan: Plan = state["plan"]
    results = []

    for step in plan.steps:
        agent_fn = AGENTS[step.agent]
        out = agent_fn({"input": step.goal})

        results.append({
            "step": step.id,
            "agent": step.agent,
            "goal": step.goal,
            "output": out["output"]
        })

    return {
        "input": plan.input,
        "results": results
    }
