from dataclasses import dataclass
from typing import Any

from app.workflows.engine import WorkflowStep


@dataclass(frozen=True, slots=True)
class YouTubeContentRequest:
    topic: str
    audience: str = "general audience"
    language: str = "English"
    tone: str = "professional and engaging"


def build_youtube_workflow(request: YouTubeContentRequest) -> list[WorkflowStep]:
    return [
        WorkflowStep("topic", "set", {"key": "topic", "value": request.topic}),
        WorkflowStep("audience", "set", {"key": "audience", "value": request.audience}),
        WorkflowStep("language", "set", {"key": "language", "value": request.language}),
        WorkflowStep("tone", "set", {"key": "tone", "value": request.tone}),
        WorkflowStep(
            "research_prompt",
            "template",
            {"key": "research_prompt", "template": "Research {topic} for {audience} in {language}."},
        ),
        WorkflowStep(
            "script_prompt",
            "template",
            {"key": "script_prompt", "template": "Create a {tone} YouTube script about {topic} for {audience}."},
        ),
        WorkflowStep(
            "metadata_prompt",
            "template",
            {"key": "metadata_prompt", "template": "Create a YouTube title, description and tags for {topic}."},
        ),
    ]
