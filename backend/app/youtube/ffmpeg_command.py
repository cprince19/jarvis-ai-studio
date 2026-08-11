from pathlib import Path


def build_render_command(ffmpeg_bin: str, clips: list[dict], output_path: str) -> list[str]:
    """Build a deterministic FFmpeg command for timeline clips.

    Media/audio/subtitle paths are passed as input arguments rather than shell
    strings, avoiding shell interpolation and keeping the worker in control of
    execution. Missing optional assets fall back to generated black video and
    silent audio.
    """
    if not clips:
        raise ValueError("Timeline cannot be empty")

    duration = sum(max(0.1, float(c.get("duration_seconds", 0))) for c in clips)
    if duration <= 0:
        raise ValueError("Timeline duration must be greater than zero")

    args = [ffmpeg_bin, "-y"]
    filters: list[str] = []
    video_labels: list[str] = []
    audio_labels: list[str] = []
    input_index = 0

    for i, clip in enumerate(clips):
        seconds = max(0.1, float(clip.get("duration_seconds", 0)))
        media = str(clip.get("media_path") or "")
        audio = str(clip.get("audio_path") or "")
        subtitle = str(clip.get("subtitle_path") or "")

        if media and Path(media).is_file():
            args += ["-i", media]
            filters.append(f"[{input_index}:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=30,trim=duration={seconds},setpts=PTS-STARTPTS[v{i}]")
            input_index += 1
        else:
            filters.append(f"color=c=black:s=1280x720:r=30:d={seconds}[v{i}]")

        video_label = f"[v{i}]"
        if subtitle and Path(subtitle).is_file():
            escaped = subtitle.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
            filters.append(f"{video_label}subtitles='{escaped}'[vs{i}]")
            video_label = f"[vs{i}]"
        video_labels.append(video_label)

        if audio and Path(audio).is_file():
            args += ["-i", audio]
            filters.append(f"[{input_index}:a]atrim=duration={seconds},asetpts=PTS-STARTPTS[a{i}]")
            audio_labels.append(f"[a{i}]")
            input_index += 1
        else:
            filters.append(f"anullsrc=r=48000:cl=stereo:d={seconds}[a{i}]")
            audio_labels.append(f"[a{i}]")

    filters.append("".join(video_labels) + f"concat=n={len(clips)}:v=1:a=0[vout]")
    filters.append("".join(audio_labels) + f"concat=n={len(clips)}:v=0:a=1[aout]")

    args += [
        "-filter_complex", ";".join(filters),
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest", output_path,
    ]
    return args
