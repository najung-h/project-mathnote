"""Video API routes - 영상 업로드 및 처리"""

import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, BackgroundTasks

from app.api.deps import StorageClientDep, SettingsDep
from app.schemas.requests import UploadUrlRequest, ProcessVideoRequest
from app.schemas.responses import (
    UploadUrlResponse,
    ConfirmUploadResponse,
    ProcessVideoResponse,
    TaskStatusResponse,
    ProgressDetail,
)
from app.services.video_service import VideoProcessingService

router = APIRouter()

# In-memory task storage (MVP용 - 추후 Redis/DB로 교체)
_task_store: dict[str, dict] = {}


@router.post("/upload-url", response_model=UploadUrlResponse)
async def get_upload_url(
    request: UploadUrlRequest,
    storage: StorageClientDep,
    settings: SettingsDep,
):
    """S3 Presigned Upload URL 발급"""
    task_id = str(uuid.uuid4())
    s3_key = f"videos/{task_id}/original.mp4"

    upload_url = await storage.generate_presigned_upload_url(
        key=s3_key,
        content_type=request.content_type,
        expires_in=settings.S3_PRESIGNED_URL_EXPIRY,
    )

    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=settings.S3_PRESIGNED_URL_EXPIRY
    )

    # 태스크 초기화
    _task_store[task_id] = {
        "status": "pending",
        "s3_key": s3_key,
        "filename": request.filename,
        "created_at": datetime.now(timezone.utc),
        "progress": {"vision": 0.0, "audio": 0.0, "synthesis": 0.0},
        "error_message": None,
    }

    return UploadUrlResponse(
        task_id=task_id,
        upload_url=upload_url,
        expires_at=expires_at,
    )


@router.post("/{task_id}/confirm-upload", response_model=ConfirmUploadResponse)
async def confirm_upload(
    task_id: str,
    storage: StorageClientDep,
):
    """업로드 완료 확인 및 S3 객체 검증"""
    from app.core.exceptions import task_not_found_exception

    if task_id not in _task_store:
        raise task_not_found_exception(task_id)

    task = _task_store[task_id]
    s3_key = task["s3_key"]

    # S3 객체 존재 확인
    exists = await storage.object_exists(s3_key)
    if not exists:
        raise task_not_found_exception(task_id)

    task["status"] = "uploaded"

    return ConfirmUploadResponse(
        task_id=task_id,
        s3_key=s3_key,
        status="uploaded",
    )


@router.post("/{task_id}/process", response_model=ProcessVideoResponse)
async def process_video(
    task_id: str,
    request: ProcessVideoRequest,
    background_tasks: BackgroundTasks,
    settings: SettingsDep,
):
    """처리 시작 (BackgroundTasks)"""
    from app.core.exceptions import task_not_found_exception

    if task_id not in _task_store:
        raise task_not_found_exception(task_id)

    task = _task_store[task_id]
    task["status"] = "processing"
    task["sos_timestamps"] = request.sos_timestamps

    # 처리 옵션 병합 (요청 > 기본값)
    options = {
        "frame_interval_sec": (
            request.options.frame_interval_sec
            if request.options and request.options.frame_interval_sec
            else settings.FRAME_INTERVAL_SEC
        ),
        "ssim_threshold": (
            request.options.ssim_threshold
            if request.options and request.options.ssim_threshold
            else settings.SSIM_THRESHOLD
        ),
    }
    task["options"] = options

    # 백그라운드 처리 시작
    background_tasks.add_task(
        VideoProcessingService.process_video_task,
        task_id=task_id,
        task_store=_task_store,
    )

    # 추정 처리 시간 (임시값)
    estimated_time_sec = 120

    return ProcessVideoResponse(
        task_id=task_id,
        status="processing",
        estimated_time_sec=estimated_time_sec,
    )


@router.get("/{task_id}/status", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """처리 상태 조회"""
    from app.core.exceptions import task_not_found_exception

    if task_id not in _task_store:
        raise task_not_found_exception(task_id)

    task = _task_store[task_id]

    return TaskStatusResponse(
        task_id=task_id,
        status=task["status"],
        progress=ProgressDetail(**task["progress"]),
        error_message=task.get("error_message"),
    )
