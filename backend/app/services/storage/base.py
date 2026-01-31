"""Base Storage Client - 추상 인터페이스"""

from abc import ABC, abstractmethod


class BaseStorageClient(ABC):
    """
    스토리지 클라이언트 추상 인터페이스

    S3, GCS 등 다양한 클라우드 스토리지를 추상화
    """

    @abstractmethod
    async def upload(
        self,
        key: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> str:
        """
        파일 업로드

        Args:
            key: 저장 경로 (S3 key)
            data: 파일 데이터
            content_type: MIME 타입

        Returns:
            업로드된 파일의 URL
        """
        pass

    @abstractmethod
    async def download(self, key: str) -> bytes:
        """
        파일 다운로드

        Args:
            key: 파일 경로

        Returns:
            파일 데이터
        """
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """
        파일 삭제

        Args:
            key: 파일 경로
        """
        pass

    @abstractmethod
    async def object_exists(self, key: str) -> bool:
        """
        객체 존재 여부 확인

        Args:
            key: 파일 경로

        Returns:
            존재 여부
        """
        pass

    @abstractmethod
    async def generate_presigned_upload_url(
        self,
        key: str,
        content_type: str,
        expires_in: int = 3600,
    ) -> str:
        """
        Presigned Upload URL 생성

        Args:
            key: 업로드할 파일 경로
            content_type: MIME 타입
            expires_in: 만료 시간 (초)

        Returns:
            Presigned URL
        """
        pass

    @abstractmethod
    async def generate_presigned_download_url(
        self,
        key: str,
        expires_in: int = 3600,
    ) -> str:
        """
        Presigned Download URL 생성

        Args:
            key: 다운로드할 파일 경로
            expires_in: 만료 시간 (초)

        Returns:
            Presigned URL
        """
        pass
