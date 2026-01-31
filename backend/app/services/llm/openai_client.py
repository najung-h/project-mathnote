"""OpenAI LLM Client - GPT-4o / GPT-4o-vision"""

import base64
from typing import Any

from app.services.llm.base import BaseLLMClient


class OpenAIClient(BaseLLMClient):
    """
    OpenAI API 클라이언트

    GPT-4o (텍스트) 및 GPT-4o-vision (이미지 분석) 지원
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        vision_model: str = "gpt-4o",
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ):
        """
        Args:
            api_key: OpenAI API 키
            model: 텍스트 모델
            vision_model: Vision 모델
            temperature: 생성 온도
            max_tokens: 최대 토큰 수
        """
        self.api_key = api_key
        self.model = model
        self.vision_model = vision_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._client = None

    def _get_client(self):
        """Lazy initialization of OpenAI client"""
        if self._client is None:
            from openai import AsyncOpenAI

            self._client = AsyncOpenAI(api_key=self.api_key)
        return self._client

    async def chat(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> str:
        """채팅 완성 요청"""
        client = self._get_client()

        response = await client.chat.completions.create(
            model=kwargs.get("model", self.model),
            messages=messages,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
        )

        return response.choices[0].message.content or ""

    async def analyze_image(
        self,
        image_bytes: bytes,
        prompt: str,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> str:
        """Vision LLM으로 이미지 분석 (바이트 데이터)"""
        client = self._get_client()

        # Base64 인코딩
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": kwargs.get("detail", "high"),
                    },
                },
                {
                    "type": "text",
                    "text": prompt,
                },
            ],
        })

        response = await client.chat.completions.create(
            model=kwargs.get("model", self.vision_model),
            messages=messages,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
        )

        return response.choices[0].message.content or ""

    async def analyze_image_url(
        self,
        image_url: str,
        prompt: str,
        system_prompt: str | None = None,
        **kwargs: Any,
    ) -> str:
        """Vision LLM으로 URL 이미지 분석"""
        client = self._get_client()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                        "detail": kwargs.get("detail", "high"),
                    },
                },
                {
                    "type": "text",
                    "text": prompt,
                },
            ],
        })

        response = await client.chat.completions.create(
            model=kwargs.get("model", self.vision_model),
            messages=messages,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
        )

        return response.choices[0].message.content or ""
