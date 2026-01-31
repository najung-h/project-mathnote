"""LLM Service Tests"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.services.llm.base import BaseLLMClient
from app.services.llm.openai_client import OpenAIClient
from app.services.llm.gemini_client import GeminiClient


class TestOpenAIClient:
    """OpenAI 클라이언트 테스트"""

    @pytest.fixture
    def client(self):
        """OpenAI 클라이언트 인스턴스"""
        return OpenAIClient(
            api_key="test-api-key",
            model="gpt-4o",
            vision_model="gpt-4o",
            temperature=0.3,
            max_tokens=4096,
        )

    def test_inherits_base_client(self, client):
        """BaseLLMClient 상속 확인"""
        assert isinstance(client, BaseLLMClient)

    def test_initialization(self, client):
        """초기화 설정 확인"""
        assert client.api_key == "test-api-key"
        assert client.model == "gpt-4o"
        assert client.temperature == 0.3

    @pytest.mark.asyncio
    @patch.object(OpenAIClient, "_get_client")
    async def test_chat(self, mock_get_client, client):
        """채팅 완성 테스트"""
        # Mock 설정
        mock_openai = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hello, world!"
        
        mock_openai.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_get_client.return_value = mock_openai

        # 테스트
        result = await client.chat(
            messages=[{"role": "user", "content": "Hi"}]
        )

        assert result == "Hello, world!"

    def test_lazy_client_initialization(self, client):
        """지연 초기화 확인"""
        assert client._client is None


class TestGeminiClient:
    """Gemini 클라이언트 테스트"""

    @pytest.fixture
    def client(self):
        """Gemini 클라이언트 인스턴스"""
        return GeminiClient(
            api_key="test-api-key",
            model="gemini-1.5-pro",
            temperature=0.3,
            max_tokens=4096,
        )

    def test_inherits_base_client(self, client):
        """BaseLLMClient 상속 확인"""
        assert isinstance(client, BaseLLMClient)

    def test_initialization(self, client):
        """초기화 설정 확인"""
        assert client.api_key == "test-api-key"
        assert client.model == "gemini-1.5-pro"

    def test_lazy_client_initialization(self, client):
        """지연 초기화 확인"""
        assert client._client is None
