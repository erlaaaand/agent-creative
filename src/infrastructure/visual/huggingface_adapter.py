import requests
from config import settings
from src.core.ports import VisualGeneratorPort
from src.core.exceptions import ImageGenerationError


class HuggingFaceAdapter(VisualGeneratorPort):
    def __init__(self):
        self._api_url = f"https://api-inference.huggingface.co/models/{settings.HF_IMAGE_MODEL}"
        self._headers = {"Authorization": f"Bearer {settings.HF_API_TOKEN}"}

    def generate_image(self, prompt: str, output_path: str) -> None:
        try:
            payload = {"inputs": prompt}
            response = requests.post(self._api_url, headers=self._headers, json=payload, timeout=120)

            if response.status_code != 200:
                raise ImageGenerationError(
                    f"HuggingFace API error [{response.status_code}]: {response.text}"
                )

            with open(output_path, "wb") as f:
                f.write(response.content)

        except ImageGenerationError:
            raise
        except Exception as e:
            raise ImageGenerationError(f"Gagal generate gambar: {e}") from e