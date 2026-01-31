"""Audio Extractor - 비디오에서 오디오 추출"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExtractedAudio:
    """추출된 오디오 정보"""

    audio_path: Path | None = None
    audio_bytes: bytes | None = None
    duration_sec: float = 0.0
    sample_rate: int = 16000
    format: str = "wav"


class AudioExtractor:
    """
    비디오에서 오디오 트랙 추출

    FFmpeg 사용
    """

    def __init__(
        self,
        output_format: str = "wav",
        sample_rate: int = 16000,
    ):
        """
        Args:
            output_format: 출력 오디오 포맷 (wav, mp3 등)
            sample_rate: 샘플링 레이트 (Whisper는 16kHz 권장)
        """
        self.output_format = output_format
        self.sample_rate = sample_rate

    async def extract_audio(
        self,
        video_path: str | Path,
        output_path: str | Path | None = None,
    ) -> ExtractedAudio:
        """
        비디오에서 오디오 추출

        Args:
            video_path: 비디오 파일 경로
            output_path: 오디오 저장 경로 (None이면 bytes로 반환)

        Returns:
            추출된 오디오 정보
        """
        # TODO: FFmpeg 구현
        # import subprocess
        #
        # cmd = [
        #     "ffmpeg",
        #     "-i", str(video_path),
        #     "-vn",  # 비디오 제외
        #     "-acodec", "pcm_s16le",  # WAV 코덱
        #     "-ar", str(self.sample_rate),  # 샘플레이트
        #     "-ac", "1",  # 모노
        #     str(output_path)
        # ]
        # subprocess.run(cmd, check=True)

        raise NotImplementedError("Audio extraction not yet implemented")

    async def extract_audio_from_bytes(
        self,
        video_bytes: bytes,
    ) -> ExtractedAudio:
        """
        바이트 데이터에서 오디오 추출

        Args:
            video_bytes: 비디오 바이트 데이터

        Returns:
            추출된 오디오 정보
        """
        raise NotImplementedError("Audio extraction from bytes not yet implemented")
