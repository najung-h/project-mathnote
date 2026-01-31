"""Application Configuration using Pydantic Settings"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # ==================== API Keys ====================
    OPENAI_API_KEY: str = ""
    GOOGLE_API_KEY: str | None = None

    # ==================== AWS S3 설정 ====================
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "ap-northeast-2"
    S3_BUCKET_NAME: str = ""
    S3_PRESIGNED_URL_EXPIRY: int = 3600  # 1시간

    # ==================== Processing Options ====================
    FRAME_INTERVAL_SEC: float = 1.0  # 프레임 추출 간격 (초)
    SSIM_THRESHOLD: float = 0.85  # 슬라이드 전환 감지 임계값
    AUDIO_PADDING_SEC: float = 5.0  # 오디오 싱크 패딩 (초)

    # ==================== LLM Settings ====================
    LLM_PROVIDER: Literal["openai", "gemini"] = "openai"
    LLM_MODEL: str = "gpt-4o"
    LLM_VISION_MODEL: str = "gpt-4o"  # Vision LLM for OCR
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 4096

    # ==================== Whisper Settings ====================
    WHISPER_MODEL: str = "base"  # tiny, base, small, medium, large

    # ==================== CORS ====================
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()


settings = get_settings()
