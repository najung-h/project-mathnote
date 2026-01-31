"""Video Downloader Utility using yt-dlp"""

import asyncio
from pathlib import Path
from typing import Any

import yt_dlp
from app.core.exceptions import VideoProcessingError


async def download_video(url: str, output_dir: Path, filename: str | None = None) -> Path:
    """
    비디오 다운로드 (비동기 래퍼)

    Args:
        url: 유튜브 비디오 URL
        output_dir: 저장할 디렉토리 경로
        filename: 저장할 파일명 (옵션). None이면 yt-dlp 기본값 사용.

    Returns:
        다운로드된 파일의 절대 경로
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # yt-dlp 옵션
    ydl_opts: dict[str, Any] = {
        "format": "bv*+ba/b",  # 최고 화질
        "merge_output_format": "mp4",
        "outtmpl": str(output_dir / "%(title)s [%(id)s].%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4",
        }],
    }

    if filename:
        ydl_opts["outtmpl"] = str(output_dir / filename)

    try:
        # 비동기 실행을 위해 run_in_executor 또는 to_thread 사용
        return await asyncio.to_thread(_run_yt_dlp, url, ydl_opts)
    except Exception as e:
        raise VideoProcessingError(f"Video download failed: {str(e)}")


def _run_yt_dlp(url: str, ydl_opts: dict[str, Any]) -> Path:
    """yt-dlp 동기 실행 함수"""
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        
        if "requested_downloads" in info:
            downloaded_file = info["requested_downloads"][0]["filepath"]
        else:
            filename = ydl.prepare_filename(info)
            downloaded_file = filename
            
            # mp4 변환 확인
            p = Path(downloaded_file)
            if p.suffix != ".mp4":
                mp4_path = p.with_suffix(".mp4")
                if mp4_path.exists():
                    downloaded_file = str(mp4_path)
        
        return Path(downloaded_file)
