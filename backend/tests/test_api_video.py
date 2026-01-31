"""Video API Tests"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock

from app.main import app
from app.api.deps import get_storage_client, get_settings
from app.config import Settings


@pytest.fixture
def mock_storage_client():
    """Mock S3 스토리지 클라이언트"""
    mock = MagicMock()
    mock.generate_presigned_upload_url = AsyncMock(
        return_value="https://s3.amazonaws.com/bucket/test-presigned-url"
    )
    mock.object_exists = AsyncMock(return_value=True)
    return mock


@pytest.fixture
def mock_settings():
    """Mock Settings"""
    return Settings(
        OPENAI_API_KEY="test-key",
        AWS_ACCESS_KEY_ID="test-access-key",
        AWS_SECRET_ACCESS_KEY="test-secret-key",
        S3_BUCKET_NAME="test-bucket",
        S3_PRESIGNED_URL_EXPIRY=3600,
    )


@pytest.fixture
def client(mock_storage_client, mock_settings):
    """FastAPI 테스트 클라이언트 (의존성 주입 오버라이드)"""
    app.dependency_overrides[get_storage_client] = lambda: mock_storage_client
    app.dependency_overrides[get_settings] = lambda: mock_settings
    
    with TestClient(app) as c:
        yield c
    
    # 테스트 후 정리
    app.dependency_overrides.clear()


class TestHealthCheck:
    """헬스체크 엔드포인트 테스트"""

    def test_health_check(self, client):
        """헬스체크가 정상 응답하는지 확인"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestUploadUrl:
    """S3 Presigned Upload URL 발급 테스트"""

    def test_get_upload_url_success(self, client):
        """정상적인 업로드 URL 발급"""
        response = client.post(
            "/api/v1/videos/upload-url",
            json={"filename": "lecture.mp4", "content_type": "video/mp4"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data
        assert "upload_url" in data
        assert "expires_at" in data

    def test_get_upload_url_default_content_type(self, client):
        """content_type 미지정 시 기본값 사용"""
        response = client.post(
            "/api/v1/videos/upload-url",
            json={"filename": "lecture.mp4"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data

    def test_get_upload_url_missing_filename(self, client):
        """filename 누락 시 422 에러"""
        response = client.post(
            "/api/v1/videos/upload-url",
            json={},
        )

        assert response.status_code == 422


class TestConfirmUpload:
    """업로드 완료 확인 테스트"""

    def test_confirm_upload_task_not_found(self, client):
        """존재하지 않는 task_id로 확인 시 404"""
        response = client.post(
            "/api/v1/videos/nonexistent-task-id/confirm-upload"
        )

        assert response.status_code == 404


class TestProcessVideo:
    """비디오 처리 시작 테스트"""

    def test_process_video_task_not_found(self, client):
        """존재하지 않는 task_id로 처리 시작 시 404"""
        response = client.post(
            "/api/v1/videos/nonexistent-task-id/process",
            json={"sos_timestamps": []},
        )

        assert response.status_code == 404

    def test_process_video_with_sos_timestamps(self, client):
        """SOS 타임스탬프 포함 요청 검증"""
        # task가 없어서 404가 나지만, 요청 형식은 유효
        response = client.post(
            "/api/v1/videos/some-task-id/process",
            json={
                "sos_timestamps": [123.5, 456.2],
                "options": {
                    "frame_interval_sec": 2.0,
                    "ssim_threshold": 0.9,
                },
            },
        )

        assert response.status_code == 404

    def test_process_video_invalid_options(self, client):
        """잘못된 옵션 값 검증"""
        response = client.post(
            "/api/v1/videos/some-task-id/process",
            json={
                "options": {
                    "frame_interval_sec": 100.0,  # 최대 10.0
                },
            },
        )

        assert response.status_code == 422


class TestTaskStatus:
    """태스크 상태 조회 테스트"""

    def test_get_status_task_not_found(self, client):
        """존재하지 않는 task_id 상태 조회 시 404"""
        response = client.get("/api/v1/videos/nonexistent-task-id/status")

        assert response.status_code == 404
