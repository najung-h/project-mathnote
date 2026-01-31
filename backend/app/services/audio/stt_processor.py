import os
from dataclasses import dataclass
from pathlib import Path
import riva.client
from app.config import settings

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
    NVIDIA Riva를 사용한 음성 인식 (Speech-to-Text)
    Whisper Large v3 모델 사용
    """

    def __init__(self):
        """
        Riva 클라이언트 초기화
        """
        self.auth = riva.client.Auth(
            None,
            use_ssl=True,
            uri="grpc.nvcf.nvidia.com:443",
            metadata_args=[
                ("function-id", "b702f636-f60c-4a3d-a6f4-f3568c13bd7d"), # Whisper Large v3 ID
                ("authorization", f"Bearer {settings.NVIDIA_API_KEY}")
            ]
        )
        self.asr_service = riva.client.ASRService(self.auth)
        
        # 인식 설정
        self.config = riva.client.RecognitionConfig(
            encoding=riva.client.AudioEncoding.LINEAR_PCM,
            sample_rate_hertz=16000,
            language_code="ko-KR",
            max_alternatives=1,
            enable_automatic_punctuation=True,
            verbatim_transcripts=False,
            # [중요] 타임스탬프를 받기 위한 필수 설정
            enable_word_time_offsets=True, 
        )

    async def transcribe(
        self,
        audio_path: str | Path,
        language: str | None = None,
    ) -> TranscriptResult:
        """
        오디오 파일 전사
        """
        audio_path = Path(audio_path)
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        return await self.transcribe_bytes(audio_bytes, language)

    async def transcribe_bytes(
        self,
        audio_bytes: bytes,
        language: str | None = None,
    ) -> TranscriptResult:
        """
        오디오 바이트 데이터 전사
        """
        import asyncio
        
        # Riva gRPC 호출 (Blocking I/O이므로 별도 스레드에서 실행)
        response = await asyncio.to_thread(
            self.asr_service.offline_recognize, 
            audio_bytes, 
            self.config
        )
        
        full_text = ""
        segments = []
        
        if not response.results:
            return TranscriptResult("", [], "ko-KR", 0.0)

        # 결과 파싱
        for result in response.results:
            if not result.alternatives:
                continue
            
            # 가장 신뢰도 높은 결과(alternatives[0]) 선택
            alt = result.alternatives[0]
            text_chunk = alt.transcript
            full_text += text_chunk + " "

            # [중요] 단어 단위 타임스탬프 정보가 있는지 확인
            if alt.words:
                # 첫 단어의 시작 시간과 마지막 단어의 끝 시간을 가져옴
                # Riva는 시간을 밀리초(ms)로 반환하므로 1000.0으로 나누어 초(sec)로 변환
                start_time = alt.words[0].start_time / 1000.0
                end_time = alt.words[-1].end_time / 1000.0
                
                segments.append(TranscriptSegment(
                    start=start_time,
                    end=end_time,
                    text=text_chunk.strip()
                ))
            else:
                # 타임스탬프 정보가 없을 경우 (매우 짧은 잡음 등)
                pass

        # 전체 길이 계산 (마지막 세그먼트의 끝 시간)
        total_duration = segments[-1].end if segments else 0.0
        
        return TranscriptResult(
            full_text=full_text.strip(),
            segments=segments,
            language="ko-KR",
            duration_sec=total_duration
        )