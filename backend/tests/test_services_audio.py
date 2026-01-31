"""Audio Service Tests"""

import pytest

from app.services.audio.audio_extractor import AudioExtractor, ExtractedAudio
from app.services.audio.stt_processor import STTProcessor, TranscriptSegment, TranscriptResult


class TestAudioExtractor:
    """AudioExtractor 테스트"""

    @pytest.fixture
    def extractor(self):
        """AudioExtractor 인스턴스"""
        return AudioExtractor(output_format="wav", sample_rate=16000)

    def test_initialization(self, extractor):
        """초기화 설정 확인"""
        assert extractor.output_format == "wav"
        assert extractor.sample_rate == 16000

    def test_custom_settings(self):
        """커스텀 설정"""
        extractor = AudioExtractor(output_format="mp3", sample_rate=44100)
        assert extractor.output_format == "mp3"
        assert extractor.sample_rate == 44100

    @pytest.mark.asyncio
    async def test_extract_audio_not_implemented(self, extractor):
        """미구현 메서드 확인"""
        with pytest.raises(NotImplementedError):
            await extractor.extract_audio("test.mp4")

    @pytest.mark.asyncio
    async def test_extract_audio_from_bytes_not_implemented(self, extractor):
        """미구현 메서드 확인"""
        with pytest.raises(NotImplementedError):
            await extractor.extract_audio_from_bytes(b"video data")


class TestSTTProcessor:
    """STTProcessor 테스트"""

    @pytest.fixture
    def processor(self):
        """STTProcessor 인스턴스"""
        return STTProcessor(model_name="base", device="auto")

    def test_initialization(self, processor):
        """초기화 설정 확인"""
        assert processor.model_name == "base"
        assert processor.device == "auto"
        assert processor._model is None

    def test_custom_model(self):
        """커스텀 모델 설정"""
        processor = STTProcessor(model_name="large", device="cuda")
        assert processor.model_name == "large"
        assert processor.device == "cuda"

    @pytest.mark.asyncio
    async def test_transcribe_not_implemented(self, processor):
        """미구현 메서드 확인"""
        with pytest.raises(NotImplementedError):
            await processor.transcribe("test.wav")

    @pytest.mark.asyncio
    async def test_transcribe_bytes_not_implemented(self, processor):
        """미구현 메서드 확인"""
        with pytest.raises(NotImplementedError):
            await processor.transcribe_bytes(b"audio data")


class TestExtractedAudio:
    """ExtractedAudio 데이터클래스 테스트"""

    def test_creation(self):
        """인스턴스 생성"""
        audio = ExtractedAudio(
            duration_sec=120.0,
            sample_rate=16000,
            format="wav",
        )
        assert audio.duration_sec == 120.0
        assert audio.sample_rate == 16000
        assert audio.format == "wav"
        assert audio.audio_path is None
        assert audio.audio_bytes is None

    def test_default_values(self):
        """기본값 확인"""
        audio = ExtractedAudio()
        assert audio.duration_sec == 0.0
        assert audio.sample_rate == 16000
        assert audio.format == "wav"


class TestTranscriptSegment:
    """TranscriptSegment 데이터클래스 테스트"""

    def test_creation(self):
        """인스턴스 생성"""
        segment = TranscriptSegment(
            start=10.5,
            end=20.3,
            text="Hello, world!",
        )
        assert segment.start == 10.5
        assert segment.end == 20.3
        assert segment.text == "Hello, world!"


class TestTranscriptResult:
    """TranscriptResult 데이터클래스 테스트"""

    def test_creation(self):
        """인스턴스 생성"""
        segments = [
            TranscriptSegment(start=0.0, end=5.0, text="First"),
            TranscriptSegment(start=5.0, end=10.0, text="Second"),
        ]
        result = TranscriptResult(
            full_text="First Second",
            segments=segments,
            language="ko",
            duration_sec=10.0,
        )
        assert result.full_text == "First Second"
        assert len(result.segments) == 2
        assert result.language == "ko"
        assert result.duration_sec == 10.0
