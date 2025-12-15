from app.agents.task.agent import task_agent

def orchestrator(state: dict):
    return task_agent({
        "input": state["input"]
    })
