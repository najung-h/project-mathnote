"""Note API routes - 노트 조회 및 다운로드"""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter

from app.api.deps import StorageClientDep, SettingsDep
from app.schemas.responses import (
    NoteResponse,
    NoteDownloadResponse,
    SlideImageResponse,
    SlideDetail,
)

router = APIRouter()

# video.py와 공유하는 task store (MVP용)
from app.api.routes.video import _task_store


@router.get("/{task_id}", response_model=NoteResponse)
async def get_note(
    task_id: str,
    storage: StorageClientDep,
    settings: SettingsDep,
):
    """생성된 노트 조회 (JSON)"""
    from app.core.exceptions import task_not_found_exception

    if task_id not in _task_store:
        raise task_not_found_exception(task_id)

    task = _task_store[task_id]

    if task["status"] != "completed":
        raise task_not_found_exception(task_id)

    # S3에서 노트 데이터 조회
    note_data = task.get("note_data", {})

    # 슬라이드 이미지 URL 생성
    slides = []
    for slide in note_data.get("slides", []):
        image_url = await storage.generate_presigned_download_url(
            key=slide["image_s3_key"],
            expires_in=settings.S3_PRESIGNED_URL_EXPIRY,
        )
        slides.append(
            SlideDetail(
                slide_number=slide["slide_number"],
                timestamp_start=slide["timestamp_start"],
                timestamp_end=slide["timestamp_end"],
                image_url=image_url,
                ocr_content=slide["ocr_content"],
                audio_summary=slide["audio_summary"],
                sos_explanation=slide.get("sos_explanation"),
            )
        )

    return NoteResponse(
        task_id=task_id,
        title=note_data.get("title", "Untitled Note"),
        slides=slides,
        created_at=task["created_at"],
    )


@router.get("/{task_id}/download", response_model=NoteDownloadResponse)
async def download_note(
    task_id: str,
    storage: StorageClientDep,
    settings: SettingsDep,
):
    """마크다운 파일 다운로드 URL"""
    from app.core.exceptions import task_not_found_exception

    if task_id not in _task_store:
        raise task_not_found_exception(task_id)

    task = _task_store[task_id]

    if task["status"] != "completed":
        raise task_not_found_exception(task_id)

    s3_key = f"outputs/{task_id}/note.md"
    download_url = await storage.generate_presigned_download_url(
        key=s3_key,
        expires_in=settings.S3_PRESIGNED_URL_EXPIRY,
    )

    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=settings.S3_PRESIGNED_URL_EXPIRY
    )

    return NoteDownloadResponse(
        download_url=download_url,
        filename=f"note_{task_id}.md",
        expires_at=expires_at,
    )


@router.get("/{task_id}/slides/{slide_number}/image", response_model=SlideImageResponse)
async def get_slide_image(
    task_id: str,
    slide_number: int,
    storage: StorageClientDep,
    settings: SettingsDep,
):
    """특정 슬라이드 이미지 URL"""
    from app.core.exceptions import task_not_found_exception

    if task_id not in _task_store:
        raise task_not_found_exception(task_id)

    s3_key = f"processing/{task_id}/slides/slide_{slide_number:03d}.jpg"
    image_url = await storage.generate_presigned_download_url(
        key=s3_key,
        expires_in=settings.S3_PRESIGNED_URL_EXPIRY,
    )

    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=settings.S3_PRESIGNED_URL_EXPIRY
    )

    return SlideImageResponse(
        image_url=image_url,
        expires_at=expires_at,
    )
