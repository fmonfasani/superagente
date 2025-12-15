from app.agents.planner.schema import Plan
from app.agents.reasoning.agent import reasoning_agent
from app.agents.code.agent import code_agent

AGENTS = {
    "architect": reasoning_agent,
    "backend": reasoning_agent,
    "reviewer": reasoning_agent,
    "code": code_agent,
}

def orchestrator(state: dict):
    plan: Plan = state["plan"]

    results = []
    memory = []

    for step in plan.steps:
        if step.agent not in AGENTS:
            raise ValueError(f"Agente no registrado: {step.agent}")

        agent_fn = AGENTS[step.agent]

        out = agent_fn({
            "input": step.goal,
            "memory": memory,
            "context": {
                "request": plan.input,
                "agent": step.agent,
                "step": step.id,
            }
        })

        result = {
            "step": step.id,
            "agent": step.agent,
            "goal": step.goal,
            "output": out["output"]
        }

        results.append(result)
        memory.append(result)

    return {
        "input": plan.input,
        "results": results,
        "memory": memory
    }
