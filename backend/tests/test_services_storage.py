"""Storage Service Tests"""

import pytest
from unittest.mock import MagicMock, patch

from app.services.storage.base import BaseStorageClient
from app.services.storage.s3_client import S3StorageClient


class TestS3StorageClient:
    """S3 스토리지 클라이언트 테스트"""

    @pytest.fixture
    def client(self):
        """S3 클라이언트 인스턴스"""
        return S3StorageClient(
            access_key_id="test-access-key",
            secret_access_key="test-secret-key",
            region="ap-northeast-2",
            bucket_name="test-bucket",
        )

    def test_inherits_base_client(self, client):
        """BaseStorageClient 상속 확인"""
        assert isinstance(client, BaseStorageClient)

    def test_initialization(self, client):
        """초기화 설정 확인"""
        assert client.access_key_id == "test-access-key"
        assert client.region == "ap-northeast-2"
        assert client.bucket_name == "test-bucket"

    def test_lazy_client_initialization(self, client):
        """지연 초기화 확인"""
        assert client._client is None

    @patch.object(S3StorageClient, "_get_client")
    def test_get_client_mocked(self, mock_get_client, client):
        """_get_client 호출 테스트 (mocked)"""
        mock_s3 = MagicMock()
        mock_get_client.return_value = mock_s3

        result = client._get_client()
        assert result == mock_s3

    @pytest.mark.asyncio
    @patch.object(S3StorageClient, "_get_client")
    async def test_upload(self, mock_get_client, client):
        """파일 업로드 테스트"""
        mock_s3 = MagicMock()
        mock_get_client.return_value = mock_s3

        result = await client.upload(
            key="test/file.txt",
            data=b"Hello, World!",
            content_type="text/plain",
        )

        mock_s3.put_object.assert_called_once_with(
            Bucket="test-bucket",
            Key="test/file.txt",
            Body=b"Hello, World!",
            ContentType="text/plain",
        )
        assert result == "s3://test-bucket/test/file.txt"

    @pytest.mark.asyncio
    @patch.object(S3StorageClient, "_get_client")
    async def test_download(self, mock_get_client, client):
        """파일 다운로드 테스트"""
        mock_s3 = MagicMock()
        mock_response = {"Body": MagicMock()}
        mock_response["Body"].read.return_value = b"Hello, World!"
        mock_s3.get_object.return_value = mock_response
        mock_get_client.return_value = mock_s3

        result = await client.download("test/file.txt")

        mock_s3.get_object.assert_called_once_with(
            Bucket="test-bucket",
            Key="test/file.txt",
        )
        assert result == b"Hello, World!"

    @pytest.mark.asyncio
    @patch.object(S3StorageClient, "_get_client")
    async def test_delete(self, mock_get_client, client):
        """파일 삭제 테스트"""
        mock_s3 = MagicMock()
        mock_get_client.return_value = mock_s3

        await client.delete("test/file.txt")

        mock_s3.delete_object.assert_called_once_with(
            Bucket="test-bucket",
            Key="test/file.txt",
        )

    @pytest.mark.asyncio
    @patch.object(S3StorageClient, "_get_client")
    async def test_generate_presigned_upload_url(self, mock_get_client, client):
        """Presigned Upload URL 생성 테스트"""
        mock_s3 = MagicMock()
        mock_s3.generate_presigned_url.return_value = "https://presigned-url"
        mock_get_client.return_value = mock_s3

        result = await client.generate_presigned_upload_url(
            key="test/file.mp4",
            content_type="video/mp4",
            expires_in=3600,
        )

        mock_s3.generate_presigned_url.assert_called_once_with(
            ClientMethod="put_object",
            Params={
                "Bucket": "test-bucket",
                "Key": "test/file.mp4",
                "ContentType": "video/mp4",
            },
            ExpiresIn=3600,
        )
        assert result == "https://presigned-url"

    @pytest.mark.asyncio
    @patch.object(S3StorageClient, "_get_client")
    async def test_generate_presigned_download_url(self, mock_get_client, client):
        """Presigned Download URL 생성 테스트"""
        mock_s3 = MagicMock()
        mock_s3.generate_presigned_url.return_value = "https://presigned-download-url"
        mock_get_client.return_value = mock_s3

        result = await client.generate_presigned_download_url(
            key="test/file.mp4",
            expires_in=3600,
        )

        mock_s3.generate_presigned_url.assert_called_once_with(
            ClientMethod="get_object",
            Params={
                "Bucket": "test-bucket",
                "Key": "test/file.mp4",
            },
            ExpiresIn=3600,
        )
        assert result == "https://presigned-download-url"

    @pytest.mark.asyncio
    @patch.object(S3StorageClient, "_get_client")
    async def test_list_objects(self, mock_get_client, client):
        """객체 목록 조회 테스트"""
        mock_s3 = MagicMock()
        mock_s3.list_objects_v2.return_value = {
            "Contents": [
                {"Key": "test/file1.txt"},
                {"Key": "test/file2.txt"},
            ]
        }
        mock_get_client.return_value = mock_s3

        result = await client.list_objects("test/", max_keys=100)

        assert result == ["test/file1.txt", "test/file2.txt"]

    @pytest.mark.asyncio
    @patch.object(S3StorageClient, "_get_client")
    async def test_list_objects_empty(self, mock_get_client, client):
        """빈 객체 목록 조회 테스트"""
        mock_s3 = MagicMock()
        mock_s3.list_objects_v2.return_value = {}
        mock_get_client.return_value = mock_s3

        result = await client.list_objects("empty/")

        assert result == []
