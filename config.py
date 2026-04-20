from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    HF_API_TOKEN: str = ""
    INPUT_DATA_PATH: str = "data/input"
    OUTPUT_DATA_PATH: str = "data/output"
    TEMP_DATA_PATH: str = "data/temp"
    HF_IMAGE_MODEL: str = "black-forest-labs/FLUX.1-schnell"

    def get_input_path(self) -> Path:
        return Path(self.INPUT_DATA_PATH)

    def get_output_path(self) -> Path:
        return Path(self.OUTPUT_DATA_PATH)

    def get_temp_path(self) -> Path:
        return Path(self.TEMP_DATA_PATH)


settings = Settings()