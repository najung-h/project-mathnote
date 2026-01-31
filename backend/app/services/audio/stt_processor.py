"""STT Processor - Whisper 기반 음성 인식"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class TranscriptSegment:
    """전사 세그먼트"""

    start: float  # 시작 시간 (초)
    end: float  # 종료 시간 (초)
    text: str  # 전사 텍스트


@dataclass
class TranscriptResult:
    """전체 전사 결과"""

    full_text: str  # 전체 텍스트
    segments: list[TranscriptSegment]  # 타임스탬프별 세그먼트
    language: str  # 감지된 언어
    duration_sec: float  # 총 길이


class STTProcessor:
    """
    Whisper를 사용한 음성 인식 (Speech-to-Text)

    OpenAI Whisper 또는 faster-whisper 사용
    """

    def __init__(
        self,
        model_name: str = "base",
        device: str = "auto",
    ):
        """
        Args:
            model_name: Whisper 모델 (tiny, base, small, medium, large)
            device: 처리 디바이스 (cpu, cuda, auto)
        """
        self.model_name = model_name
        self.device = device
        self._model = None

    async def transcribe(
        self,
        audio_path: str | Path,
        language: str | None = None,
    ) -> TranscriptResult:
        """
        오디오 파일 전사

        Args:
            audio_path: 오디오 파일 경로
            language: 언어 코드 (None이면 자동 감지)

        Returns:
            전사 결과 (타임스탬프 포함)
        """
        # TODO: Whisper 구현
        # import whisper
        #
        # if self._model is None:
        #     self._model = whisper.load_model(self.model_name)
        #
        # result = self._model.transcribe(
        #     str(audio_path),
        #     language=language,
        #     word_timestamps=True,
        # )
        #
        # segments = [
        #     TranscriptSegment(
        #         start=seg["start"],
        #         end=seg["end"],
        #         text=seg["text"],
        #     )
        #     for seg in result["segments"]
        # ]
        #
        # return TranscriptResult(
        #     full_text=result["text"],
        #     segments=segments,
        #     language=result["language"],
        #     duration_sec=segments[-1].end if segments else 0.0,
        # )

        raise NotImplementedError("STT processing not yet implemented")

    async def transcribe_bytes(
        self,
        audio_bytes: bytes,
        language: str | None = None,
    ) -> TranscriptResult:
        """
        오디오 바이트 데이터 전사

        Args:
            audio_bytes: 오디오 바이트 데이터
            language: 언어 코드

        Returns:
            전사 결과
        """
        raise NotImplementedError("STT from bytes not yet implemented")
