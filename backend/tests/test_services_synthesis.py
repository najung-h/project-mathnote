"""Synthesis Service Tests"""

import pytest

from app.services.synthesis.segment_mapper import SegmentMapper, MappedSegment
from app.services.synthesis.prompt_engine import PromptEngine
from app.services.vision.scene_detector import DetectedSlide
from app.services.vision.ocr_processor import OCRResult
from app.services.vision.frame_extractor import ExtractedFrame
from app.services.audio.stt_processor import TranscriptSegment


class TestSegmentMapper:
    """SegmentMapper 테스트"""

    @pytest.fixture
    def mapper(self):
        """SegmentMapper 인스턴스"""
        return SegmentMapper(padding_sec=5.0)

    @pytest.fixture
    def sample_slides(self):
        """샘플 슬라이드 목록"""
        frame = ExtractedFrame(frame_number=1, timestamp_sec=0.0)
        return [
            DetectedSlide(
                slide_number=1,
                timestamp_start=0.0,
                timestamp_end=60.0,
                frame=frame,
            ),
            DetectedSlide(
                slide_number=2,
                timestamp_start=60.0,
                timestamp_end=120.0,
                frame=frame,
            ),
        ]

    @pytest.fixture
    def sample_ocr_results(self):
        """샘플 OCR 결과"""
        return [
            OCRResult(
                slide_number=1,
                raw_text="Slide 1",
                structured_markdown="# Slide 1\n\n$E = mc^2$",
                latex_expressions=["E = mc^2"],
            ),
            OCRResult(
                slide_number=2,
                raw_text="Slide 2",
                structured_markdown="# Slide 2\n\n본문 내용",
                latex_expressions=[],
            ),
        ]

    @pytest.fixture
    def sample_transcript(self):
        """샘플 전사 세그먼트"""
        return [
            TranscriptSegment(start=0.0, end=30.0, text="첫 번째 설명입니다."),
            TranscriptSegment(start=30.0, end=60.0, text="두 번째 설명입니다."),
            TranscriptSegment(start=60.0, end=90.0, text="세 번째 설명입니다."),
            TranscriptSegment(start=90.0, end=120.0, text="네 번째 설명입니다."),
        ]

    def test_map_segments_basic(
        self, mapper, sample_slides, sample_ocr_results, sample_transcript
    ):
        """기본 세그먼트 매핑"""
        result = mapper.map_segments(
            slides=sample_slides,
            ocr_results=sample_ocr_results,
            transcript_segments=sample_transcript,
        )

        assert len(result) == 2
        assert result[0].slide_number == 1
        assert result[1].slide_number == 2

    def test_map_segments_with_sos(
        self, mapper, sample_slides, sample_ocr_results, sample_transcript
    ):
        """SOS 타임스탬프 포함 매핑"""
        result = mapper.map_segments(
            slides=sample_slides,
            ocr_results=sample_ocr_results,
            transcript_segments=sample_transcript,
            sos_timestamps=[45.0],  # 첫 번째 슬라이드 구간
        )

        assert result[0].sos_requested is True
        assert result[1].sos_requested is False

    def test_map_segments_audio_transcript_merged(
        self, mapper, sample_slides, sample_ocr_results, sample_transcript
    ):
        """오디오 전사 병합 확인"""
        result = mapper.map_segments(
            slides=sample_slides,
            ocr_results=sample_ocr_results,
            transcript_segments=sample_transcript,
        )

        # 첫 번째 슬라이드: 0-60초 + 패딩 → 0-65초
        assert "첫 번째 설명" in result[0].audio_transcript
        assert "두 번째 설명" in result[0].audio_transcript

    def test_overlaps(self, mapper):
        """구간 겹침 확인 함수"""
        # 완전 겹침
        assert mapper._overlaps(10, 20, 5, 25) is True
        # 부분 겹침
        assert mapper._overlaps(10, 20, 15, 30) is True
        # 안 겹침
        assert mapper._overlaps(10, 20, 25, 35) is False
        # 경계 (끝과 시작이 같음)
        assert mapper._overlaps(10, 20, 20, 30) is False


class TestPromptEngine:
    """PromptEngine 테스트"""

    @pytest.fixture
    def engine(self):
        """PromptEngine 인스턴스"""
        return PromptEngine()

    @pytest.fixture
    def sample_segment(self):
        """샘플 매핑된 세그먼트"""
        return MappedSegment(
            slide_number=1,
            timestamp_start=0.0,
            timestamp_end=60.0,
            ocr_content="# Slide 1\n\n$E = mc^2$",
            audio_transcript="아인슈타인의 공식에 대해 설명하겠습니다.",
            sos_requested=False,
        )

    @pytest.fixture
    def sample_sos_segment(self):
        """SOS가 요청된 세그먼트"""
        return MappedSegment(
            slide_number=2,
            timestamp_start=60.0,
            timestamp_end=120.0,
            ocr_content="# Slide 2\n\n$$\\int_0^1 f(x)dx$$",
            audio_transcript="적분에 대해 설명하겠습니다.",
            sos_requested=True,
        )

    def test_build_summary_prompt(self, engine, sample_segment):
        """요약 프롬프트 생성"""
        result = engine.build_summary_prompt(sample_segment)

        assert result.slide_number == 1
        assert "슬라이드" in result.user_prompt
        assert "OCR" in result.user_prompt
        assert "STT" in result.user_prompt
        assert result.requires_sos_explanation is False

    def test_build_sos_prompt(self, engine, sample_sos_segment):
        """SOS 프롬프트 생성"""
        result = engine.build_sos_prompt(sample_sos_segment)

        assert result.slide_number == 2
        assert "이해하기 어려워" in result.user_prompt
        assert result.requires_sos_explanation is True
        assert "과외 선생님" in result.system_prompt

    def test_build_prompts_without_sos(self, engine, sample_segment):
        """SOS 없는 세그먼트 프롬프트 목록"""
        result = engine.build_prompts([sample_segment])

        assert len(result) == 1  # 요약 프롬프트만

    def test_build_prompts_with_sos(self, engine, sample_sos_segment):
        """SOS 있는 세그먼트 프롬프트 목록"""
        result = engine.build_prompts([sample_sos_segment])

        assert len(result) == 2  # 요약 + SOS 프롬프트

    def test_system_prompts_exist(self, engine):
        """시스템 프롬프트 상수 확인"""
        assert engine.SYSTEM_PROMPT_SUMMARY is not None
        assert engine.SYSTEM_PROMPT_SOS is not None
        assert "대학원생 조교" in engine.SYSTEM_PROMPT_SUMMARY
        assert "과외 선생님" in engine.SYSTEM_PROMPT_SOS
