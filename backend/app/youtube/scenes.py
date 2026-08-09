from dataclasses import dataclass
import re


@dataclass(slots=True)
class Scene:
    number: int
    heading: str
    narration: str
    visual_prompt: str
    duration_seconds: int


class ScenePlanner:
    """Turns an approved script into a deterministic shot list for the renderer."""

    def plan(self, script: str, default_duration: int = 8) -> list[Scene]:
        if not script.strip():
            raise ValueError("Script cannot be empty")
        blocks = [b.strip() for b in re.split(r"\n\s*\n", script) if b.strip()]
        scenes: list[Scene] = []
        for index, block in enumerate(blocks, 1):
            lines = [line.strip() for line in block.splitlines() if line.strip()]
            heading = lines[0][:120] if lines else f"Scene {index}"
            narration = " ".join(lines)
            scenes.append(Scene(index, heading, narration, f"Cinematic YouTube visual illustrating: {heading}", default_duration))
        return scenes
