from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class WorkflowStep:
    id: str
    type: str
    config: dict[str, Any]


class WorkflowEngine:
    """Minimal deterministic workflow runner used as the Phase 1 execution core."""

    async def run(self, steps: list[WorkflowStep], context: dict[str, Any] | None = None) -> dict[str, Any]:
        state = dict(context or {})
        history: list[dict[str, Any]] = []
        for step in steps:
            if step.type == "set":
                key = step.config.get("key")
                if not key:
                    raise ValueError("set step requires key")
                state[key] = step.config.get("value")
            elif step.type == "template":
                key = step.config.get("key", "output")
                template = str(step.config.get("template", ""))
                state[key] = template.format(**state)
            elif step.type == "log":
                history.append({"step": step.id, "message": step.config.get("message", "")})
            else:
                raise ValueError(f"Unsupported workflow step type: {step.type}")
            history.append({"step": step.id, "type": step.type, "status": "completed"})
        return {"state": state, "history": history}
