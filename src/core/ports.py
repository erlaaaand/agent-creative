from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class StoragePort(ABC):
    @abstractmethod
    def list_input_files(self) -> list[Path]:
        pass

    @abstractmethod
    def read_json(self, filepath: Path) -> dict:
        pass

    @abstractmethod
    def move_to_processed(self, filepath: Path) -> Path:
        pass

    @abstractmethod
    def setup_workspace(self, job_id: str) -> Path:
        pass

    @abstractmethod
    def cleanup_workspace(self, workspace_path: Path) -> None:
        pass


class TextToSpeechPort(ABC):
    @abstractmethod
    async def generate_audio(self, text: str, voice: str, output_path: str) -> None:
        pass

    @abstractmethod
    async def get_available_id_voices(self) -> list[str]:
        pass

    @abstractmethod
    async def preview_voice(self, voice_name: str, temp_path: str) -> None:
        pass


class VisualGeneratorPort(ABC):
    @abstractmethod
    def generate_image(self, prompt: str, output_path: str) -> None:
        pass


class VideoEditorPort(ABC):
    @abstractmethod
    def assemble_video(
        self,
        workspace_path: str,
        scenes: list[dict],
        output_path: str,
    ) -> None:
        pass