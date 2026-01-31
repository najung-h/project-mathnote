"""Note API Tests"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """FastAPI 테스트 클라이언트"""
    with TestClient(app) as c:
        yield c


class TestGetNote:
    """노트 조회 테스트"""

    def test_get_note_task_not_found(self, client):
        """존재하지 않는 task_id로 노트 조회 시 404"""
        response = client.get("/api/v1/notes/nonexistent-task-id")

        assert response.status_code == 404

    def test_get_note_processing_not_completed(self, client):
        """처리 완료되지 않은 task의 노트 조회 시 404"""
        # task가 있지만 completed가 아닌 경우
        response = client.get("/api/v1/notes/processing-task-id")

        assert response.status_code == 404


class TestDownloadNote:
    """노트 다운로드 테스트"""

    def test_download_note_task_not_found(self, client):
        """존재하지 않는 task_id로 다운로드 시 404"""
        response = client.get("/api/v1/notes/nonexistent-task-id/download")

        assert response.status_code == 404


class TestSlideImage:
    """슬라이드 이미지 URL 테스트"""

    def test_get_slide_image_task_not_found(self, client):
        """존재하지 않는 task_id의 슬라이드 이미지 조회 시 404"""
        response = client.get("/api/v1/notes/nonexistent-task-id/slides/1/image")

        assert response.status_code == 404

    def test_get_slide_image_invalid_slide_number(self, client):
        """유효하지 않은 슬라이드 번호"""
        response = client.get("/api/v1/notes/some-task-id/slides/abc/image")

        assert response.status_code == 422
