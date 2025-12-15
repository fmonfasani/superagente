# app/agents/planner/planner.py

from app.agents.planner.schema import PlannerInput, Plan, PlanStep

class Planner:
    """
    Planner determinístico.
    - NO ejecuta agentes
    - NO usa LLM
    - SOLO define el plan
    """

    def plan(self, req: PlannerInput) -> Plan:
        text = req.input.lower()
        steps: list[PlanStep] = []

        # Regla base: backend / CRUD
        if "crud" in text or "api" in text or "fastapi" in text:
            steps = [
                PlanStep(
                    id=1,
                    agent="architect",
                    goal="Definir arquitectura del proyecto y estructura de carpetas"
                ),
                PlanStep(
                    id=2,
                    agent="backend",
                    goal="Definir modelos de datos y contratos (ORM + schemas)"
                ),
                PlanStep(
                    id=3,
                    agent="code",
                    goal="Implementar endpoints CRUD con FastAPI"
                ),
                PlanStep(
                    id=4,
                    agent="reviewer",
                    goal="Revisar coherencia, calidad y buenas prácticas"
                ),
            ]

        # Fallback seguro
        if not steps:
            steps = [
                PlanStep(
                    id=1,
                    agent="architect",
                    goal=f"Analizar requerimiento: {req.input}"
                )
            ]

        return Plan(
            input=req.input,
            steps=steps
        )
