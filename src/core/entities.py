from pydantic import BaseModel
from typing import Optional
from enum import Enum


class ProductionMetadata(BaseModel):
    target_duration_seconds: int
    platform: str
    voiceover_style: str
    bgm_mood: str


class DistributionAssets(BaseModel):
    suggested_title: str
    primary_keywords: list[str]
    recommended_hashtags: list[str]


class Scene(BaseModel):
    scene_number: int
    estimated_duration_sec: float
    visual_prompt: str
    audio_narration: str
    on_screen_text: str


class ScriptDocument(BaseModel):
    document_id: str
    topic: str
    production_metadata: ProductionMetadata
    distribution_assets: DistributionAssets
    scenes: list[Scene]


class ScriptFile(BaseModel):
    region: str
    date: str
    generated_at: str
    scripts: list[ScriptDocument]


class RenderStatus(str, Enum):
    PENDING = "pending"
    GENERATING_ASSETS = "generating_assets"
    ASSEMBLING = "assembling"
    COMPLETED = "completed"
    FAILED = "failed"


class RenderJob(BaseModel):
    job_id: str
    document_id: str
    filename: str
    voice: str
    status: RenderStatus = RenderStatus.PENDING
    output_path: Optional[str] = None
    error_message: Optional[str] = None
    total_scenes: int = 0
    completed_scenes: int = 0