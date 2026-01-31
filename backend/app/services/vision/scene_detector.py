"""Scene Detector - 슬라이드 전환 감지"""

from dataclasses import dataclass

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

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
        if not frames:
            return []

        slides = []
        prev_image_gray = None
        current_slide_start = frames[0].timestamp_sec
        slide_counter = 1

        # 첫 번째 프레임은 무조건 첫 슬라이드의 시작
        # 그러나 실제 Scene Detection을 위해 루프 내에서 처리

        for i, frame in enumerate(frames):
            # 현재 프레임 이미지 로드 (경로 또는 바이트에서)
            current_image = self._load_image(frame)
            if current_image is None:
                continue
            
            # 그레이스케일 변환 (SSIM 성능 향상)
            current_image_gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)

            if prev_image_gray is None:
                # 첫 번째 프레임 처리
                slides.append(DetectedSlide(
                    slide_number=slide_counter,
                    timestamp_start=frame.timestamp_sec,
                    timestamp_end=frame.timestamp_sec, # 임시
                    frame=frame,
                    ssim_score=None
                ))
                prev_image_gray = current_image_gray
                continue

            # 이전 프레임과 SSIM 비교
            # 이미지 크기가 다르면 리사이즈
            if prev_image_gray.shape != current_image_gray.shape:
                current_image_gray = cv2.resize(current_image_gray, (prev_image_gray.shape[1], prev_image_gray.shape[0]))

            score, _ = ssim(prev_image_gray, current_image_gray, full=True)

            if score < self.ssim_threshold:
                # 유사도가 낮음 -> 새로운 슬라이드 등장
                # 이전 슬라이드 종료 시간 업데이트
                slides[-1].timestamp_end = frames[i-1].timestamp_sec
                
                # 새 슬라이드 등록
                slide_counter += 1
                slides.append(DetectedSlide(
                    slide_number=slide_counter,
                    timestamp_start=frame.timestamp_sec,
                    timestamp_end=frame.timestamp_sec, # 임시
                    frame=frame,
                    ssim_score=score
                ))
                
                # 기준 이미지 업데이트 (새 슬라이드의 첫 프레임)
                prev_image_gray = current_image_gray
            else:
                # 유사도가 높음 -> 같은 슬라이드 유지
                # 종료 시간만 계속 업데이트 (마지막 프레임까지)
                slides[-1].timestamp_end = frame.timestamp_sec

        return slides

    def _load_image(self, frame: ExtractedFrame) -> np.ndarray | None:
        """ExtractedFrame에서 OpenCV 이미지 로드"""
        if frame.image_bytes:
            nparr = np.frombuffer(frame.image_bytes, np.uint8)
            return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        elif frame.image_path:
            return cv2.imread(str(frame.image_path))
        return None

    def _calculate_ssim(
        self,
        frame1: bytes,
        frame2: bytes,
    ) -> float:
        """(Deprecated) 내부 메서드 사용 권장"""
        nparr1 = np.frombuffer(frame1, np.uint8)
        img1 = cv2.imdecode(nparr1, cv2.IMREAD_GRAYSCALE)
        
        nparr2 = np.frombuffer(frame2, np.uint8)
        img2 = cv2.imdecode(nparr2, cv2.IMREAD_GRAYSCALE)
        
        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
            
        score, _ = ssim(img1, img2, full=True)
        return score