"""Vision Service Tests"""

import pytest

from app.services.vision.frame_extractor import FrameExtractor, ExtractedFrame
from app.services.vision.scene_detector import SceneDetector, DetectedSlide
from app.services.vision.ocr_processor import OCRProcessor


class TestFrameExtractor:
    """FrameExtractor 테스트"""

    @pytest.fixture
    def extractor(self):
        """FrameExtractor 인스턴스"""
        return FrameExtractor(interval_sec=1.0)

    def test_initialization(self, extractor):
        """초기화 설정 확인"""
        assert extractor.interval_sec == 1.0

    def test_custom_interval(self):
        """커스텀 간격 설정"""
        extractor = FrameExtractor(interval_sec=2.5)
        assert extractor.interval_sec == 2.5

    @pytest.mark.asyncio
    async def test_extract_frames_not_implemented(self, extractor):
        """미구현 메서드 확인"""
        with pytest.raises(NotImplementedError):
            await extractor.extract_frames("test.mp4")

    @pytest.mark.asyncio
    async def test_extract_frames_from_bytes_not_implemented(self, extractor):
        """미구현 메서드 확인"""
        with pytest.raises(NotImplementedError):
            await extractor.extract_frames_from_bytes(b"video data")


class TestSceneDetector:
    """SceneDetector 테스트"""

    @pytest.fixture
    def detector(self):
        """SceneDetector 인스턴스"""
        return SceneDetector(ssim_threshold=0.85)

    def test_initialization(self, detector):
        """초기화 설정 확인"""
        assert detector.ssim_threshold == 0.85

    def test_custom_threshold(self):
        """커스텀 임계값 설정"""
        detector = SceneDetector(ssim_threshold=0.9)
        assert detector.ssim_threshold == 0.9

    @pytest.mark.asyncio
    async def test_detect_slides_not_implemented(self, detector):
        """미구현 메서드 확인"""
        with pytest.raises(NotImplementedError):
            await detector.detect_slides([])

    def test_calculate_ssim_not_implemented(self, detector):
        """미구현 메서드 확인"""
        with pytest.raises(NotImplementedError):
            detector._calculate_ssim(b"frame1", b"frame2")


class TestOCRProcessor:
    """OCRProcessor 테스트"""

    def test_system_prompt_exists(self):
        """시스템 프롬프트 상수 확인"""
        assert OCRProcessor.SYSTEM_PROMPT is not None
        assert "수학 강의" in OCRProcessor.SYSTEM_PROMPT
        assert "LaTeX" in OCRProcessor.SYSTEM_PROMPT

    def test_extract_latex_block(self):
        """블록 LaTeX 추출"""
        from unittest.mock import MagicMock
        
        mock_llm = MagicMock()
        processor = OCRProcessor(llm_client=mock_llm)

        text = """
        # Title
        
        $$E = mc^2$$
        
        Some text
        
        $$\\int_0^1 f(x) dx$$
        """

        result = processor._extract_latex(text)

        assert len(result) == 2
        assert "E = mc^2" in result[0]
        assert "int" in result[1]

    def test_extract_latex_inline(self):
        """인라인 LaTeX 추출"""
        from unittest.mock import MagicMock
        
        mock_llm = MagicMock()
        processor = OCRProcessor(llm_client=mock_llm)

        text = "The formula $E = mc^2$ is famous. Also $a^2 + b^2 = c^2$."

        result = processor._extract_latex(text)

        assert len(result) >= 2

    def test_extract_latex_mixed(self):
        """혼합 LaTeX 추출"""
        from unittest.mock import MagicMock
        
        mock_llm = MagicMock()
        processor = OCRProcessor(llm_client=mock_llm)

        text = """
        Inline: $x = 1$
        
        Block:
        $$y = 2x + 3$$
        """

        result = processor._extract_latex(text)

        assert len(result) >= 2


class TestExtractedFrame:
    """ExtractedFrame 데이터클래스 테스트"""

    def test_creation(self):
        """인스턴스 생성"""
        frame = ExtractedFrame(
            frame_number=1,
            timestamp_sec=1.5,
        )
        assert frame.frame_number == 1
        assert frame.timestamp_sec == 1.5
        assert frame.image_path is None
        assert frame.image_bytes is None


class TestDetectedSlide:
    """DetectedSlide 데이터클래스 테스트"""

    def test_creation(self):
        """인스턴스 생성"""
        frame = ExtractedFrame(frame_number=1, timestamp_sec=0.0)
        slide = DetectedSlide(
            slide_number=1,
            timestamp_start=0.0,
            timestamp_end=60.0,
            frame=frame,
        )
        assert slide.slide_number == 1
        assert slide.timestamp_start == 0.0
        assert slide.timestamp_end == 60.0
        assert slide.ssim_score is None
