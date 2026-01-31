"""AWS S3 Storage Client"""

from app.services.storage.base import BaseStorageClient


class S3StorageClient(BaseStorageClient):
    """
    AWS S3 스토리지 클라이언트

    Presigned URL을 통한 직접 업로드/다운로드 지원
    """

    def __init__(
        self,
        access_key_id: str,
        secret_access_key: str,
        region: str,
        bucket_name: str,
    ):
        """
        Args:
            access_key_id: AWS Access Key ID
            secret_access_key: AWS Secret Access Key
            region: AWS 리전
            bucket_name: S3 버킷 이름
        """
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region = region
        self.bucket_name = bucket_name
        self._client = None

    def _get_client(self):
        """Lazy initialization of S3 client"""
        if self._client is None:
            import boto3

            self._client = boto3.client(
                "s3",
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key,
                region_name=self.region,
            )
        return self._client

    async def upload(
        self,
        key: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> str:
        """파일 업로드"""
        client = self._get_client()

        client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=data,
            ContentType=content_type,
        )

        return f"s3://{self.bucket_name}/{key}"

    async def download(self, key: str) -> bytes:
        """파일 다운로드"""
        client = self._get_client()

        response = client.get_object(
            Bucket=self.bucket_name,
            Key=key,
        )

        return response["Body"].read()

    async def delete(self, key: str) -> None:
        """파일 삭제"""
        client = self._get_client()

        client.delete_object(
            Bucket=self.bucket_name,
            Key=key,
        )

    async def object_exists(self, key: str) -> bool:
        """객체 존재 여부 확인"""
        client = self._get_client()

        try:
            client.head_object(
                Bucket=self.bucket_name,
                Key=key,
            )
            return True
        except client.exceptions.ClientError:
            return False

    async def generate_presigned_upload_url(
        self,
        key: str,
        content_type: str,
        expires_in: int = 3600,
    ) -> str:
        """Presigned Upload URL 생성"""
        client = self._get_client()

        url = client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=expires_in,
        )

        return url

    async def generate_presigned_download_url(
        self,
        key: str,
        expires_in: int = 3600,
    ) -> str:
        """Presigned Download URL 생성"""
        client = self._get_client()

        url = client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": key,
            },
            ExpiresIn=expires_in,
        )

        return url

    async def list_objects(
        self,
        prefix: str,
        max_keys: int = 1000,
    ) -> list[str]:
        """
        특정 prefix의 객체 목록 조회

        Args:
            prefix: 경로 prefix
            max_keys: 최대 조회 개수

        Returns:
            객체 키 목록
        """
        client = self._get_client()

        response = client.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix=prefix,
            MaxKeys=max_keys,
        )

        if "Contents" not in response:
            return []

        return [obj["Key"] for obj in response["Contents"]]
