"""Base LLM Client - 추상 인터페이스"""

from abc import ABC, abstractmethod
from typing import Any


class BaseLLMClient(ABC):
    """
    LLM 클라이언트 추상 인터페이스

    OpenAI, Gemini 등 다양한 LLM 제공자를 추상화
    """

    @abstractmethod
    async def chat(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> str:
        """
        채팅 완성 요청

        Args:
            messages: 메시지 목록 [{"role": "user", "content": "..."}]
            **kwargs: 추가 옵션

        Returns:
            LLM 응답 텍스트
        """
        pass

    @abstractmethod
    async def analyze_image(
        self,
        image_bytes: bytes,
        prompt: str,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> str:
        """
        Vision LLM으로 이미지 분석

        Args:
            image_bytes: 이미지 바이트 데이터
            prompt: 분석 요청 프롬프트
            system_prompt: 시스템 프롬프트
            **kwargs: 추가 옵션

        Returns:
            분석 결과 텍스트
        """
        pass

    @abstractmethod
    async def analyze_image_url(
        self,
        image_url: str,
        prompt: str,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> str:
        """
        Vision LLM으로 URL 이미지 분석

        Args:
            image_url: 이미지 URL
            prompt: 분석 요청 프롬프트
            system_prompt: 시스템 프롬프트
            **kwargs: 추가 옵션

        Returns:
            분석 결과 텍스트
        """
        pass
