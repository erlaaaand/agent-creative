import os
from pathlib import Path
from moviepy import (
    ImageClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
from src.core.ports import VideoEditorPort
from src.core.exceptions import VideoAssemblyError


class MoviePyAdapter(VideoEditorPort):
    def assemble_video(
        self,
        workspace_path: str,
        scenes: list[dict],
        output_path: str,
    ) -> None:
        try:
            clips = []
            workspace = Path(workspace_path)

            for scene in scenes:
                num = scene["scene_number"]
                image_file = workspace / f"scene_{num}.png"
                audio_file = workspace / f"scene_{num}.mp3"
                on_screen_text = scene.get("on_screen_text", "")

                if not image_file.exists() or not audio_file.exists():
                    continue

                audio_clip = AudioFileClip(str(audio_file))
                actual_duration = audio_clip.duration

                image_clip = (
                    ImageClip(str(image_file), duration=actual_duration)
                    .with_audio(audio_clip)
                )

                if on_screen_text:
                    txt_clip = (
                        TextClip(
                            text=on_screen_text,
                            font_size=48,
                            color="white",
                            font="Arial-Bold",
                            stroke_color="black",
                            stroke_width=2,
                            method="caption",
                            size=(image_clip.w - 80, None),
                            duration=actual_duration,
                        )
                        .with_position(("center", "center"))
                    )
                    scene_clip = CompositeVideoClip([image_clip, txt_clip])
                else:
                    scene_clip = image_clip

                clips.append(scene_clip)

            if not clips:
                raise VideoAssemblyError("Tidak ada scene yang valid untuk dirakit.")

            final_video = concatenate_videoclips(clips, method="compose")
            final_video.write_videofile(
                output_path,
                fps=24,
                codec="libx264",
                audio_codec="aac",
                logger=None,
            )

            for clip in clips:
                clip.close()
            final_video.close()

        except VideoAssemblyError:
            raise
        except Exception as e:
            raise VideoAssemblyError(f"Gagal merakit video: {e}") from e