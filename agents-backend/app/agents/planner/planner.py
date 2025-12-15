# planner/planner.py
from typing import Dict, List
from planner.models import PlannerInput, PlanStep, PlanResult
from planner.logger import log_step, timeit

# 👇 agentes registrados
from agents.architect import ArchitectAgent
from agents.backend import BackendAgent

AGENTS = {
    "architect": ArchitectAgent(),
    "backend": BackendAgent(),
}


class Planner:

    def __init__(self, agents: Dict):
        self.agents = agents

    def build_plan(self, input: PlannerInput) -> List[PlanStep]:
        # ⚠️ planner SOLO arma el plan
        return [
            PlanStep(1, "architect", "definir estructura"),
            PlanStep(2, "backend", "crear modelo"),
        ]

    def execute(self, input: PlannerInput) -> List[PlanResult]:
        plan = self.build_plan(input)
        results: List[PlanResult] = []

        for step in plan:
            agent = self.agents.get(step.agent)
            if not agent:
                raise ValueError(f"Agente no encontrado: {step.agent}")

            log_step(step.agent, step.task)

            @timeit
            def run_agent():
                return agent.run(step.task, context=input.constraints)

            output, duration = run_agent()

            results.append(
                PlanResult(
                    step_id=step.step_id,
                    agent=step.agent,
                    task=step.task,
                    output=output,
                    duration_ms=duration
                )
            )

        return results
