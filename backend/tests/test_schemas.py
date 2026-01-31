"""Schema Validation Tests"""

import pytest
from pydantic import ValidationError

from app.schemas.requests import (
    UploadUrlRequest,
    ProcessVideoRequest,
    ProcessingOptions,
)
from app.schemas.responses import (
    UploadUrlResponse,
    ConfirmUploadResponse,
    ProcessVideoResponse,
    TaskStatusResponse,
    ProgressDetail,
    NoteResponse,
    SlideDetail,
)


class TestUploadUrlRequest:
    """UploadUrlRequest 스키마 테스트"""

    def test_valid_request(self):
        """정상 요청"""
        request = UploadUrlRequest(
            filename="lecture.mp4",
            content_type="video/mp4",
        )
        assert request.filename == "lecture.mp4"
        assert request.content_type == "video/mp4"

    def test_default_content_type(self):
        """content_type 기본값"""
        request = UploadUrlRequest(filename="lecture.mp4")
        assert request.content_type == "video/mp4"

    def test_missing_filename(self):
        """filename 누락"""
        with pytest.raises(ValidationError):
            UploadUrlRequest()


class TestProcessingOptions:
    """ProcessingOptions 스키마 테스트"""

    def test_valid_options(self):
        """정상 옵션"""
        options = ProcessingOptions(
            frame_interval_sec=2.0,
            ssim_threshold=0.9,
        )
        assert options.frame_interval_sec == 2.0
        assert options.ssim_threshold == 0.9

    def test_frame_interval_range(self):
        """frame_interval_sec 범위 검증"""
        # 최소값 미만
        with pytest.raises(ValidationError):
            ProcessingOptions(frame_interval_sec=0.05)

        # 최대값 초과
        with pytest.raises(ValidationError):
            ProcessingOptions(frame_interval_sec=15.0)

    def test_ssim_threshold_range(self):
        """ssim_threshold 범위 검증"""
        # 최소값 미만
        with pytest.raises(ValidationError):
            ProcessingOptions(ssim_threshold=0.3)

        # 최대값 초과
        with pytest.raises(ValidationError):
            ProcessingOptions(ssim_threshold=1.5)


class TestProcessVideoRequest:
    """ProcessVideoRequest 스키마 테스트"""

    def test_valid_request(self):
        """정상 요청"""
        request = ProcessVideoRequest(
            sos_timestamps=[123.5, 456.2],
            options=ProcessingOptions(frame_interval_sec=2.0),
        )
        assert len(request.sos_timestamps) == 2
        assert request.options.frame_interval_sec == 2.0

    def test_empty_sos_timestamps(self):
        """빈 SOS 타임스탬프 (기본값)"""
        request = ProcessVideoRequest()
        assert request.sos_timestamps == []
        assert request.options is None


class TestProgressDetail:
    """ProgressDetail 스키마 테스트"""

    def test_valid_progress(self):
        """정상 진행률"""
        progress = ProgressDetail(
            vision=0.5,
            audio=0.3,
            synthesis=0.0,
        )
        assert progress.vision == 0.5

    def test_progress_range(self):
        """진행률 범위 (0.0 ~ 1.0)"""
        with pytest.raises(ValidationError):
            ProgressDetail(vision=1.5, audio=0.0, synthesis=0.0)

        with pytest.raises(ValidationError):
            ProgressDetail(vision=-0.1, audio=0.0, synthesis=0.0)


class TestTaskStatusResponse:
    """TaskStatusResponse 스키마 테스트"""

    def test_valid_response(self):
        """정상 응답"""
        response = TaskStatusResponse(
            task_id="abc-123",
            status="processing",
            progress=ProgressDetail(vision=0.5, audio=0.3, synthesis=0.0),
            error_message=None,
        )
        assert response.task_id == "abc-123"
        assert response.status == "processing"

    def test_failed_status_with_error(self):
        """실패 상태 + 에러 메시지"""
        response = TaskStatusResponse(
            task_id="abc-123",
            status="failed",
            progress=ProgressDetail(vision=0.5, audio=0.0, synthesis=0.0),
            error_message="FFmpeg not found",
        )
        assert response.status == "failed"
        assert response.error_message == "FFmpeg not found"

    def test_invalid_status(self):
        """유효하지 않은 상태값"""
        with pytest.raises(ValidationError):
            TaskStatusResponse(
                task_id="abc-123",
                status="unknown",  # 유효하지 않은 상태
                progress=ProgressDetail(vision=0.0, audio=0.0, synthesis=0.0),
            )


class TestSlideDetail:
    """SlideDetail 스키마 테스트"""

    def test_valid_slide(self):
        """정상 슬라이드"""
        slide = SlideDetail(
            slide_number=1,
            timestamp_start=0.0,
            timestamp_end=60.0,
            image_url="https://s3.amazonaws.com/bucket/slide.jpg",
            ocr_content="# Title\n\n$E = mc^2$",
            audio_summary="아인슈타인의 공식 설명",
            sos_explanation=None,
        )
        assert slide.slide_number == 1
        assert slide.sos_explanation is None

    def test_slide_with_sos(self):
        """SOS 해설 포함 슬라이드"""
        slide = SlideDetail(
            slide_number=1,
            timestamp_start=0.0,
            timestamp_end=60.0,
            image_url="https://example.com/slide.jpg",
            ocr_content="# Title",
            audio_summary="설명",
            sos_explanation="💡 심층 해설: ...",
        )
        assert slide.sos_explanation is not None
