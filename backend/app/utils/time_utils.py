"""Time Utilities - 타임스탬프 관련 유틸리티"""


def seconds_to_timestamp(seconds: float) -> str:
    """
    초를 HH:MM:SS 형식으로 변환

    Args:
        seconds: 초

    Returns:
        HH:MM:SS 형식 문자열
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def timestamp_to_seconds(timestamp: str) -> float:
    """
    HH:MM:SS 또는 MM:SS 형식을 초로 변환

    Args:
        timestamp: 타임스탬프 문자열

    Returns:
        초 단위 float
    """
    parts = timestamp.split(":")
    if len(parts) == 3:
        hours, minutes, seconds = map(float, parts)
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:
        minutes, seconds = map(float, parts)
        return minutes * 60 + seconds
    else:
        return float(parts[0])


def format_duration(seconds: float) -> str:
    """
    초를 읽기 쉬운 형식으로 변환

    Args:
        seconds: 초

    Returns:
        "1h 23m 45s" 형식 문자열
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")

    return " ".join(parts)


def find_segment_for_timestamp(
    timestamp: float,
    segments: list[tuple[float, float]],
) -> int | None:
    """
    특정 타임스탬프가 속한 세그먼트 인덱스 찾기

    Args:
        timestamp: 찾을 타임스탬프 (초)
        segments: (start, end) 튜플 리스트

    Returns:
        세그먼트 인덱스 또는 None
    """
    for i, (start, end) in enumerate(segments):
        if start <= timestamp <= end:
            return i
    return None
