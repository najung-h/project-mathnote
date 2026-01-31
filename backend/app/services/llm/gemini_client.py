"""Google Gemini LLM Client"""

import base64
from typing import Any

from app.services.llm.base import BaseLLMClient


class GeminiClient(BaseLLMClient):
    """
    Google Gemini API 클라이언트

    Gemini Pro (텍스트) 및 Gemini Pro Vision (이미지 분석) 지원
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-1.5-pro",
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ):
        """
        Args:
            api_key: Google API 키
            model: Gemini 모델
            temperature: 생성 온도
            max_tokens: 최대 토큰 수
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._client = None

    def _get_client(self):
        """Lazy initialization of Gemini client"""
        if self._client is None:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            self._client = genai.GenerativeModel(self.model)
        return self._client

    async def chat(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> str:
        """채팅 완성 요청"""
        client = self._get_client()

        # 메시지 형식 변환
        prompt_parts = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")

        prompt = "\n\n".join(prompt_parts)

        response = await client.generate_content_async(
            prompt,
            generation_config={
                "temperature": kwargs.get("temperature", self.temperature),
                "max_output_tokens": kwargs.get("max_tokens", self.max_tokens),
            },
        )

        return response.text

    async def analyze_image(
        self,
        image_bytes: bytes,
        prompt: str,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> str:
        """Vision LLM으로 이미지 분석 (바이트 데이터)"""
        client = self._get_client()

        # 이미지 데이터 준비
        image_part = {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(image_bytes).decode("utf-8"),
        }

        # 프롬프트 구성
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        response = await client.generate_content_async(
            [image_part, full_prompt],
            generation_config={
                "temperature": kwargs.get("temperature", self.temperature),
                "max_output_tokens": kwargs.get("max_tokens", self.max_tokens),
            },
        )

        return response.text

    async def analyze_image_url(
        self,
        image_url: str,
        prompt: str,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> str:
        """Vision LLM으로 URL 이미지 분석"""
        # URL에서 이미지 다운로드 후 분석
        import aiohttp

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                image_bytes = await response.read()

        return await self.analyze_image(
            image_bytes=image_bytes,
            prompt=prompt,
            system_prompt=system_prompt,
            **kwargs,
        )
