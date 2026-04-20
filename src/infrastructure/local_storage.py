import json
import shutil
from pathlib import Path
from config import settings
from src.core.ports import StoragePort
from src.core.exceptions import StorageError


class LocalStorageAdapter(StoragePort):
    def __init__(self):
        self._input_path = settings.get_input_path()
        self._output_path = settings.get_output_path()
        self._temp_path = settings.get_temp_path()
        self._processed_path = self._input_path / "_processed"

        for path in [self._input_path, self._output_path, self._temp_path, self._processed_path]:
            path.mkdir(parents=True, exist_ok=True)

    def list_input_files(self) -> list[Path]:
        try:
            return sorted(self._input_path.glob("*.json"))
        except Exception as e:
            raise StorageError(f"Gagal membaca folder input: {e}") from e

    def read_json(self, filepath: Path) -> dict:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise StorageError(f"Gagal membaca file JSON: {e}") from e

    def move_to_processed(self, filepath: Path) -> Path:
        try:
            dest = self._processed_path / filepath.name
            shutil.move(str(filepath), str(dest))
            return dest
        except Exception as e:
            raise StorageError(f"Gagal memindahkan file: {e}") from e

    def setup_workspace(self, job_id: str) -> Path:
        try:
            workspace = self._temp_path / job_id
            workspace.mkdir(parents=True, exist_ok=True)
            return workspace
        except Exception as e:
            raise StorageError(f"Gagal membuat workspace: {e}") from e

    def cleanup_workspace(self, workspace_path: Path) -> None:
        try:
            if workspace_path.exists():
                shutil.rmtree(workspace_path)
        except Exception as e:
            raise StorageError(f"Gagal membersihkan workspace: {e}") from e

    def get_output_path(self) -> Path:
        return self._output_path