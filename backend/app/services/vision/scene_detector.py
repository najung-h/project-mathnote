"""Scene Detector - 슬라이드 전환 감지"""

from dataclasses import dataclass

from app.services.vision.frame_extractor import ExtractedFrame


@dataclass
class DetectedSlide:
    """감지된 고유 슬라이드 정보"""

    slide_number: int
    timestamp_start: float
    timestamp_end: float
    frame: ExtractedFrame
    ssim_score: float | None = None  # 이전 슬라이드와의 유사도


class SceneDetector:
    """
    프레임 간 유사도 비교를 통해 슬라이드 전환 감지

    SSIM (Structural Similarity Index) 사용
    """

    def __init__(self, ssim_threshold: float = 0.85):
        """
        Args:
            ssim_threshold: 슬라이드 전환 감지 임계값
                           - 유사도가 이 값보다 낮으면 새 슬라이드로 판정
        """
        self.ssim_threshold = ssim_threshold

    async def detect_slides(
        self,
        frames: list[ExtractedFrame],
    ) -> list[DetectedSlide]:
        """
        프레임 목록에서 고유 슬라이드 추출

        Args:
            frames: 추출된 프레임 목록

        Returns:
            고유 슬라이드 목록 (타임스탬프 포함)
        """
        # TODO: SSIM 기반 구현
        # from skimage.metrics import structural_similarity as ssim
        # import cv2
        #
        # slides = []
        # prev_frame = None
        # slide_number = 0
        #
        # for frame in frames:
        #     if prev_frame is None:
        #         # 첫 프레임은 무조건 새 슬라이드
        #         slide_number += 1
        #         slides.append(DetectedSlide(
        #             slide_number=slide_number,
        #             timestamp_start=frame.timestamp_sec,
        #             timestamp_end=frame.timestamp_sec,
        #             frame=frame,
        #         ))
        #     else:
        #         # SSIM 계산
        #         score = ssim(prev_frame, current_frame, ...)
        #         if score < self.ssim_threshold:
        #             # 새 슬라이드 감지
        #             slides[-1].timestamp_end = frame.timestamp_sec
        #             slide_number += 1
        #             slides.append(DetectedSlide(...))
        #
        #     prev_frame = current_frame
        #
        # return slides

        raise NotImplementedError("Scene detection not yet implemented")

    def _calculate_ssim(
        self,
        frame1: bytes,
        frame2: bytes,
    ) -> float:
        """
        두 프레임 간 SSIM 계산

        Args:
            frame1: 첫 번째 프레임 이미지 바이트
            frame2: 두 번째 프레임 이미지 바이트

        Returns:
            SSIM 점수 (0.0 ~ 1.0)
        """
        raise NotImplementedError("SSIM calculation not yet implemented")
