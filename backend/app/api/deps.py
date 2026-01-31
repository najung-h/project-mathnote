"""Dependency Injection for API routes"""

from typing import Annotated

from fastapi import Depends

from app.config import Settings, get_settings
from app.services.storage.s3_client import S3StorageClient
from app.services.llm.base import BaseLLMClient
from app.services.llm.openai_client import OpenAIClient
from app.services.llm.gemini_client import GeminiClient


def get_storage_client(
    settings: Annotated[Settings, Depends(get_settings)]
) -> S3StorageClient:
    """Get S3 storage client"""
    return S3StorageClient(
        access_key_id=settings.AWS_ACCESS_KEY_ID,
        secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region=settings.AWS_REGION,
        bucket_name=settings.S3_BUCKET_NAME,
    )


def get_llm_client(
    settings: Annotated[Settings, Depends(get_settings)]
) -> BaseLLMClient:
    """Get LLM client based on configuration"""
    if settings.LLM_PROVIDER == "openai":
        return OpenAIClient(
            api_key=settings.OPENAI_API_KEY,
            model=settings.LLM_MODEL,
            vision_model=settings.LLM_VISION_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
        )
    elif settings.LLM_PROVIDER == "gemini":
        return GeminiClient(
            api_key=settings.GOOGLE_API_KEY or "",
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
        )
    else:
        raise ValueError(f"Unknown LLM provider: {settings.LLM_PROVIDER}")


# Type aliases for dependency injection
StorageClientDep = Annotated[S3StorageClient, Depends(get_storage_client)]
LLMClientDep = Annotated[BaseLLMClient, Depends(get_llm_client)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
