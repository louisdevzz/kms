from minio import Minio
from minio.error import S3Error
from typing import Optional, BinaryIO
import logging
from datetime import timedelta


class MinIOStorage:
    def __init__(self, endpoint: str, access_key: str, secret_key: str,bucket_name: str, secure: bool = False):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self.bucket_name = bucket_name
        self.logger = logging.getLogger(__name__)
        self.ensure_bucket_exists()

    def ensure_bucket_exists(self):
        # ensure the bucket exists, create if not
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                self.logger.info(f"Created bucket: {self.bucket_name}")
        except S3Error as e:
            self.logger.error(f"Error ensuring bucket exists: {e}")
            raise

    def addDoc(self, object_name: str, data: BinaryIO, length: int,
               content_type: str = "application/octet-stream") -> bool:
        try:
            self.logger.info(f"Attempting to upload document: {object_name}, length: {length}")
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=data,
                length=length,
                content_type=content_type
            )
            self.logger.info(f"Successfully uploaded document: {object_name}")
            return True
        except S3Error as e:
            self.logger.error(f"S3Error adding document {object_name}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error adding document {object_name}: {e}")
            return False

    def getDoc(self, object_name: str) -> Optional[BinaryIO]:
        try:
            self.logger.info(f"Attempting to get document: {object_name}")
            response = self.client.get_object(
                bucket_name=self.bucket_name,
                object_name=object_name
            )
            self.logger.info(f"Successfully retrieved document: {object_name}")
            return response
        except S3Error as e:
            self.logger.error(f"S3Error getting document {object_name}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error getting document {object_name}: {e}")
            return None

    def getDocUrl(self, object_name: str, expires: timedelta) -> Optional[str]:
        try:
            return self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                expires=expires
            )
        except S3Error as e:
            self.logger.error(f"Error generating URL for {object_name}: {e}")
            return None

    def deleteDoc(self, object_name: str) -> bool:
        try:
            self.client.remove_object(
                bucket_name=self.bucket_name,
                object_name=object_name
            )
            return True
        except S3Error as e:
            self.logger.error(f"Error deleting document {object_name}: {e}")
            return False