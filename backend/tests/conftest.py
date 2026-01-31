"""Pytest Configuration and Fixtures"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock

from app.main import app
from app.config import Settings
from app.services.vision.frame_extractor import ExtractedFrame
from app.services.vision.scene_detector import DetectedSlide
from app.services.vision.ocr_processor import OCRResult
from app.services.audio.stt_processor import TranscriptSegment
from app.services.synthesis.segment_mapper import MappedSegment


@pytest.fixture
def client():
    """FastAPI 테스트 클라이언트"""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_settings():
    """테스트용 설정"""
    return Settings(
        OPENAI_API_KEY="test-key",
        AWS_ACCESS_KEY_ID="test-access-key",
        AWS_SECRET_ACCESS_KEY="test-secret-key",
        S3_BUCKET_NAME="test-bucket",
    )


@pytest.fixture
def sample_task_id():
    """샘플 태스크 ID"""
    return "test-task-id-12345"


@pytest.fixture
def mock_storage_client():
    """Mock S3 Storage 클라이언트"""
    client = MagicMock()
    client.generate_presigned_upload_url = AsyncMock(
        return_value="https://s3.amazonaws.com/bucket/presigned-url"
    )
    client.generate_presigned_download_url = AsyncMock(
        return_value="https://s3.amazonaws.com/bucket/download-url"
    )
    client.object_exists = AsyncMock(return_value=True)
    client.upload = AsyncMock(return_value="s3://bucket/key")
    client.download = AsyncMock(return_value=b"file content")
    return client


@pytest.fixture
def mock_llm_client():
    """Mock LLM 클라이언트"""
    client = MagicMock()
    client.chat = AsyncMock(return_value="LLM response")
    client.analyze_image = AsyncMock(return_value="# Slide\n\n$E = mc^2$")
    client.analyze_image_url = AsyncMock(return_value="# Slide from URL")
    return client


@pytest.fixture
def sample_frame():
    """샘플 ExtractedFrame"""
    return ExtractedFrame(
        frame_number=1,
        timestamp_sec=0.0,
        image_bytes=b"fake image data",
    )


@pytest.fixture
def sample_slides(sample_frame):
    """샘플 DetectedSlide 목록"""
    return [
        DetectedSlide(
            slide_number=1,
            timestamp_start=0.0,
            timestamp_end=60.0,
            frame=sample_frame,
        ),
        DetectedSlide(
            slide_number=2,
            timestamp_start=60.0,
            timestamp_end=120.0,
            frame=sample_frame,
        ),
    ]


@pytest.fixture
def sample_ocr_results():
    """샘플 OCRResult 목록"""
    return [
        OCRResult(
            slide_number=1,
            raw_text="Slide 1 content",
            structured_markdown="# Slide 1\n\n$E = mc^2$",
            latex_expressions=["E = mc^2"],
        ),
        OCRResult(
            slide_number=2,
            raw_text="Slide 2 content",
            structured_markdown="# Slide 2\n\n본문 내용",
            latex_expressions=[],
        ),
    ]


@pytest.fixture
def sample_transcript_segments():
    """샘플 TranscriptSegment 목록"""
    return [
        TranscriptSegment(start=0.0, end=30.0, text="첫 번째 설명입니다."),
        TranscriptSegment(start=30.0, end=60.0, text="두 번째 설명입니다."),
        TranscriptSegment(start=60.0, end=90.0, text="세 번째 설명입니다."),
        TranscriptSegment(start=90.0, end=120.0, text="네 번째 설명입니다."),
    ]


@pytest.fixture
def sample_mapped_segments():
    """샘플 MappedSegment 목록"""
    return [
        MappedSegment(
            slide_number=1,
            timestamp_start=0.0,
            timestamp_end=60.0,
            ocr_content="# Slide 1\n\n$E = mc^2$",
            audio_transcript="첫 번째 설명입니다. 두 번째 설명입니다.",
            sos_requested=False,
        ),
        MappedSegment(
            slide_number=2,
            timestamp_start=60.0,
            timestamp_end=120.0,
            ocr_content="# Slide 2",
            audio_transcript="세 번째 설명입니다. 네 번째 설명입니다.",
            sos_requested=True,
        ),
    ]

