from dataclasses import dataclass

from app.ai.registry import get_provider


@dataclass(slots=True)
class YouTubePackage:
    research: str
    script: str
    title: str
    description: str
    tags: list[str]


class YouTubeContentGenerator:
    async def generate(self, topic: str, audience: str, language: str, tone: str, provider_name: str = "mock", model: str | None = None) -> YouTubePackage:
        provider = get_provider(provider_name)
        base = f"Topic: {topic}\nAudience: {audience}\nLanguage: {language}\nTone: {tone}"
        research = (await provider.generate(f"Research and organize factual talking points for a YouTube video.\n{base}", model)).content
        script = (await provider.generate(f"Write a structured YouTube script using these inputs. Include hook, sections, transitions and CTA.\n{base}\nResearch:\n{research}", model)).content
        metadata = (await provider.generate(f"Create YouTube metadata. Return exactly three labeled sections: TITLE, DESCRIPTION, TAGS.\n{base}\nScript:\n{script}", model)).content
        title, description, tags = self._parse_metadata(metadata)
        return YouTubePackage(research=research, script=script, title=title, description=description, tags=tags)

    @staticmethod
    def _parse_metadata(text: str) -> tuple[str, str, list[str]]:
        sections: dict[str, str] = {}
        current = None
        for line in text.splitlines():
            label = line.strip().rstrip(":").upper()
            if label in {"TITLE", "DESCRIPTION", "TAGS"}:
                current = label
                sections[current] = ""
            elif current:
                sections[current] += ("\n" if sections[current] else "") + line.strip()
        title = sections.get("TITLE", "YouTube Video")
        description = sections.get("DESCRIPTION", "")
        tags = [tag.strip().lstrip("#") for tag in sections.get("TAGS", "").replace(",", "\n").splitlines() if tag.strip()]
        return title, description, tags
