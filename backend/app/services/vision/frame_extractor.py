"""Frame Extractor - 비디오에서 프레임 추출"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExtractedFrame:
    """추출된 프레임 정보"""

    frame_number: int
    timestamp_sec: float
    image_path: Path | None = None
    image_bytes: bytes | None = None


class FrameExtractor:
    """
    비디오에서 프레임을 추출하는 서비스

    OpenCV 또는 FFmpeg을 사용하여 N초 간격으로 프레임 추출
    """

    def __init__(self, interval_sec: float = 1.0):
        """
        Args:
            interval_sec: 프레임 추출 간격 (초)
        """
        self.interval_sec = interval_sec

    async def extract_frames(
        self,
        video_path: str | Path,
        output_dir: str | Path | None = None,
    ) -> list[ExtractedFrame]:
        """
        비디오에서 프레임 추출

        Args:
            video_path: 비디오 파일 경로
            output_dir: 프레임 이미지 저장 경로 (None이면 bytes로 반환)

        Returns:
            추출된 프레임 목록
        """
        # TODO: OpenCV 또는 FFmpeg 구현
        # import cv2
        #
        # cap = cv2.VideoCapture(str(video_path))
        # fps = cap.get(cv2.CAP_PROP_FPS)
        # frame_interval = int(fps * self.interval_sec)
        #
        # frames = []
        # frame_count = 0
        #
        # while True:
        #     ret, frame = cap.read()
        #     if not ret:
        #         break
        #
        #     if frame_count % frame_interval == 0:
        #         timestamp = frame_count / fps
        #         # Save or encode frame
        #         frames.append(ExtractedFrame(...))
        #
        #     frame_count += 1
        #
        # cap.release()
        # return frames

        raise NotImplementedError("Frame extraction not yet implemented")

    async def extract_frames_from_bytes(
        self,
        video_bytes: bytes,
    ) -> list[ExtractedFrame]:
        """
        바이트 데이터에서 프레임 추출 (S3에서 다운로드한 경우)

        Args:
            video_bytes: 비디오 바이트 데이터

        Returns:
            추출된 프레임 목록
        """
        # TODO: 구현
        raise NotImplementedError("Frame extraction from bytes not yet implemented")
