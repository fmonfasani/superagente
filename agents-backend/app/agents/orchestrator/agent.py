from app.agents.task.agent import task_agent
from app.agents.code.agent import code_agent

def orchestrator(state: dict):
    results = []

    for step in state["plan"]:
        agent = step["agent"]
        goal = step["goal"]

        if agent == "code":
            out = code_agent({"input": goal})
        else:
            out = task_agent({"input": goal})

        results.append({
            "step": step["step"],
            "agent": agent,
            "goal": goal,
            "output": out["output"]
        })

    return {
        "input": state["input"],
        "results": results
    }
