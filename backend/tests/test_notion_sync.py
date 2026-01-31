import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_sync_to_notion_not_found():
    """존재하지 않는 태스크에 대한 노션 동기화 시도"""
    response = client.post("/api/v1/notes/non-existent-id/notion")
    assert response.status_code == 404

@patch("app.api.routes.note.get_note")
@patch("app.api.routes.note.notion_service.create_lecture_page")
def test_sync_to_notion_success(mock_create_page, mock_get_note):
    """노션 동기화 성공 케이스"""
    from app.api.routes.video import _task_store
    from datetime import datetime, timezone
    
    task_id = "test-task-id"
    _task_store[task_id] = {
        "status": "completed",
        "created_at": datetime.now(timezone.utc),
        "note_data": {"title": "Test Title", "slides": []}
    }
    
    # Mock 설정
    mock_get_note.return_value = MagicMock()
    mock_create_page.return_value = "https://notion.so/test-page"
    
    response = client.post(f"/api/v1/notes/{task_id}/notion")
    
    assert response.status_code == 200
    assert response.json() == {"notion_page_url": "https://notion.so/test-page"}
    
    # 클린업
    del _task_store[task_id]
