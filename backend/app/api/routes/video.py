"""Video API routes - 영상 업로드 및 처리"""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, File, UploadFile

from app.api.deps import StorageClientDep, SettingsDep
from app.schemas.requests import ProcessVideoRequest
from app.schemas.responses import (
    UploadResponse,
    ProcessVideoResponse,
    TaskStatusResponse,
    ProgressDetail,
)
from app.services.video_service import VideoProcessingService

router = APIRouter()

# In-memory task storage (MVP용 - 추후 Redis/DB로 교체)
_task_store: dict[str, dict] = {}


@router.post("/upload", response_model=UploadResponse)
async def upload_video(
    storage: StorageClientDep,
    file: UploadFile = File(...),
):
    """비디오 파일 업로드 (Multipart)"""
    task_id = str(uuid.uuid4())
    # 파일 확장자 추출
    extension = file.filename.split(".")[-1] if file.filename else "mp4"
    file_key = f"videos/{task_id}/original.{extension}"

    # 파일 읽기 및 저장
    file_data = await file.read()
    file_url = await storage.upload(key=file_key, data=file_data, content_type=file.content_type or "video/mp4")

    # 태스크 초기화
    _task_store[task_id] = {
        "status": "uploaded",
        "s3_key": file_key, # 로컬에서는 파일 경로 키 역할
        "filename": file.filename,
        "created_at": datetime.now(timezone.utc),
        "progress": {"vision": 0.0, "audio": 0.0, "synthesis": 0.0},
        "error_message": None,
    }

    return UploadResponse(
        task_id=task_id,
        file_url=file_url,
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
