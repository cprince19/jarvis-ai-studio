from dataclasses import dataclass


@dataclass(slots=True)
class SubtitleCue:
    scene_number: int
    start_seconds: float
    end_seconds: float
    text: str


class SubtitleBuilder:
    def build(self, clips: list[dict], max_words: int = 12) -> list[SubtitleCue]:
        cues: list[SubtitleCue] = []
        for clip in clips:
            start = float(clip.get("start_seconds", 0))
            duration = float(clip.get("duration_seconds", 0))
            text = str(clip.get("narration", "")).strip()
            if not text or duration <= 0:
                continue
            words = text.split()
            chunks = [words[i:i + max_words] for i in range(0, len(words), max_words)]
            step = duration / len(chunks)
            for index, chunk in enumerate(chunks):
                cues.append(SubtitleCue(int(clip.get("scene_number", 0)), start + index * step, start + (index + 1) * step, " ".join(chunk)))
        return cues

    @staticmethod
    def to_srt(cues: list[SubtitleCue]) -> str:
        def stamp(seconds: float) -> str:
            ms = int(round((seconds - int(seconds)) * 1000))
            total = int(seconds)
            h, total = divmod(total, 3600)
            m, s = divmod(total, 60)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
        return "\n\n".join(f"{i}\n{stamp(c.start_seconds)} --> {stamp(c.end_seconds)}\n{c.text}" for i, c in enumerate(cues, 1)) + ("\n" if cues else "")
