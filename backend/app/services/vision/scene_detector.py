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
    edge_count: int = 0  # 엣지 픽셀 수 (정보량)


class SceneDetector:
    """
    프레임 간 유사도 비교를 통해 슬라이드 전환 감지
    SSIM (Structural Similarity Index) 사용
    """

    def __init__(self, ssim_threshold: float = 0.85, edge_change_threshold: float = 1.2):
        """
        Args:
            ssim_threshold: 슬라이드 전환 감지 임계값
            edge_change_threshold: 정보량(엣지) 변화 감지 비율 (1.2 = 20% 증가 시 캡처)
        """
        self.ssim_threshold = ssim_threshold
        self.edge_change_threshold = edge_change_threshold

    async def detect_slides(
        self,
        frames: list[ExtractedFrame],
        video_duration: float | None = None,
    ) -> list[DetectedSlide]:
        """
        프레임 목록에서 고유 슬라이드 추출 (Peak Detection 방식 적용)
        """
        if not frames:
            return []

        slides = []
        prev_image_gray = None
        slide_counter = 1
        
        # Peak Detection을 위한 상태 변수들
        prev_edge_count = 0
        is_increasing = False
        
        # 현재 슬라이드 구간의 프레임 버퍼 (Peak 판단 후 저장용)
        current_slide_frames = []

        for i, frame in enumerate(frames):
            # 현재 프레임 이미지 로드
            current_image = self._load_image(frame)
            if current_image is None:
                continue
            
            # 그레이스케일 변환
            current_image_gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
            
            # 엣지 계산 (정보량 측정)
            edges = cv2.Canny(current_image_gray, 100, 200)
            current_edge_count = np.count_nonzero(edges)

            if prev_image_gray is None:
                # 첫 번째 프레임 (무조건 저장)
                slides.append(DetectedSlide(
                    slide_number=slide_counter,
                    timestamp_start=0.0,
                    timestamp_end=frame.timestamp_sec,
                    frame=frame,
                    ssim_score=None,
                    edge_count=current_edge_count
                ))
                prev_image_gray = current_image_gray
                prev_edge_count = current_edge_count
                continue

            # 이전 *기준* 프레임과 SSIM 비교 (슬라이드 전환 감지용)
            if prev_image_gray.shape != current_image_gray.shape:
                current_image_gray = cv2.resize(current_image_gray, (prev_image_gray.shape[1], prev_image_gray.shape[0]))

            score, _ = ssim(prev_image_gray, current_image_gray, full=True)

            if score < self.ssim_threshold:
                # [CASE 1] 완전히 새로운 슬라이드 등장
                
                # 이전 슬라이드 마무리 (Peak 처리 되지 않은 마지막 상태가 있다면?)
                # 보통 Peak가 아니면(감소 중이거나 증가 중) 굳이 저장 안 해도 됨.
                # 단, 증가하다가 슬라이드가 확 바뀌었다면 그 직전이 Peak일 수 있음.
                if is_increasing:
                    # 마지막 프레임을 Peak로 간주하여 저장
                    last_frame = frames[i-1]
                    slides.append(DetectedSlide(
                        slide_number=slide_counter, # 같은 번호 (서브)
                        timestamp_start=last_frame.timestamp_sec,
                        timestamp_end=last_frame.timestamp_sec,
                        frame=last_frame,
                        ssim_score=score,
                        edge_count=prev_edge_count
                    ))

                # 새 슬라이드 등록
                slide_counter += 1
                slides.append(DetectedSlide(
                    slide_number=slide_counter,
                    timestamp_start=frame.timestamp_sec,
                    timestamp_end=frame.timestamp_sec,
                    frame=frame,
                    ssim_score=score,
                    edge_count=current_edge_count
                ))
                
                # 상태 초기화
                prev_image_gray = current_image_gray
                prev_edge_count = current_edge_count
                is_increasing = False
                slides[-1].timestamp_end = frames[i-1].timestamp_sec if i > 0 else 0
                
            else:
                # [CASE 2] 같은 슬라이드 (Peak 감지 로직)
                slides[-1].timestamp_end = frame.timestamp_sec
                
                # 노이즈 필터링 (엣지 수 차이가 5% 이상일 때만 변화로 인정)
                edge_diff = current_edge_count - prev_edge_count
                # 최소 100픽셀 변화는 있어야 유의미하다고 판단 (빈 화면에서의 노이즈 방지)
                noise_threshold = max(prev_edge_count * 0.05, 100)
                
                if abs(edge_diff) > noise_threshold:
                    if edge_diff > 0:
                        # 증가 중
                        is_increasing = True
                    else:
                        # 감소 중
                        if is_increasing:
                            # 증가하다가 감소함 -> Peak 발생!
                            # 직전 프레임(prev_frame)이 Peak였음.
                            # 하지만 루프 구조상 prev_frame 객체를 들고 있진 않으므로 frame[i-1] 사용
                            peak_frame = frames[i-1]
                            
                            # 중복 저장 방지 (너무 가까운 시간 제외)
                            if peak_frame.timestamp_sec - slides[-1].timestamp_start > 1.0:
                                slides.append(DetectedSlide(
                                    slide_number=slide_counter,
                                    timestamp_start=peak_frame.timestamp_sec,
                                    timestamp_end=peak_frame.timestamp_sec,
                                    frame=peak_frame,
                                    ssim_score=score,
                                    edge_count=prev_edge_count
                                ))
                            
                            is_increasing = False # Peak 찍고 내려가는 중
                        
                    prev_edge_count = current_edge_count

        # 마지막 슬라이드 종료 시간 보정
        if slides and video_duration:
            slides[-1].timestamp_end = max(slides[-1].timestamp_end, video_duration)

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