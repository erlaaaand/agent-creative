import asyncio
import uuid
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from src.core.entities import ScriptFile, RenderJob, RenderStatus
from src.core.ports import StoragePort, TextToSpeechPort, VisualGeneratorPort, VideoEditorPort
from src.core.exceptions import AgentCreativeError


class RenderUseCase:
    def __init__(
        self,
        storage: StoragePort,
        tts: TextToSpeechPort,
        visual: VisualGeneratorPort,
        video: VideoEditorPort,
        console: Console | None = None,
    ):
        self._storage = storage
        self._tts = tts
        self._visual = visual
        self._video = video
        self._console = console or Console()

    def list_available_files(self) -> list[Path]:
        return self._storage.list_input_files()

    def load_script_file(self, filepath: Path) -> ScriptFile:
        raw = self._storage.read_json(filepath)
        return ScriptFile(**raw)

    def execute(self, filepath: Path, document_id: str, voice: str) -> RenderJob:
        script_file = self.load_script_file(filepath)

        target_doc = None
        for doc in script_file.scripts:
            if doc.document_id == document_id:
                target_doc = doc
                break

        if not target_doc:
            raise AgentCreativeError(f"Document ID '{document_id}' tidak ditemukan.")

        job_id = str(uuid.uuid4())[:8]
        job = RenderJob(
            job_id=job_id,
            document_id=document_id,
            filename=filepath.name,
            voice=voice,
            status=RenderStatus.PENDING,
            total_scenes=len(target_doc.scenes),
        )

        workspace = self._storage.setup_workspace(job_id)
        job.status = RenderStatus.GENERATING_ASSETS

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold cyan]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=self._console,
                transient=True,
            ) as progress:
                task = progress.add_task(
                    f"Generating assets untuk [bold]{target_doc.topic}[/bold]...",
                    total=len(target_doc.scenes) * 2,
                )

                for scene in target_doc.scenes:
                    num = scene.scene_number
                    image_path = str(workspace / f"scene_{num}.png")
                    audio_path = str(workspace / f"scene_{num}.mp3")

                    progress.update(task, description=f"🎨 Scene {num}: Generate gambar...")
                    self._visual.generate_image(scene.visual_prompt, image_path)
                    progress.advance(task)

                    progress.update(task, description=f"🎙️ Scene {num}: Generate audio...")
                    asyncio.run(self._tts.generate_audio(scene.audio_narration, voice, audio_path))
                    progress.advance(task)

                    job.completed_scenes += 1

            job.status = RenderStatus.ASSEMBLING
            self._console.print("[bold yellow]🎬 Merakit video...[/bold yellow]")

            output_filename = f"{document_id}.mp4"
            output_path = str(self._storage.get_output_path() / output_filename)

            scenes_data = [s.model_dump() for s in target_doc.scenes]
            self._video.assemble_video(str(workspace), scenes_data, output_path)

            self._storage.cleanup_workspace(workspace)
            self._storage.move_to_processed(filepath)

            job.status = RenderStatus.COMPLETED
            job.output_path = output_path
            self._console.print(f"[bold green]✅ Video selesai: {output_path}[/bold green]")

        except Exception as e:
            job.status = RenderStatus.FAILED
            job.error_message = str(e)
            self._storage.cleanup_workspace(workspace)
            raise

        return job