from google.cloud import storage
from typing import Optional
from google.oauth2 import service_account
from utils.utils import Utils
from enum import Enum, StrEnum
from google.api_core.exceptions import NotFound, Forbidden, TooManyRequests, GoogleAPIError
from google.auth.exceptions import DefaultCredentialsError
import re

class GCSUtils:
    def __init__(self):
        self.gcs_client = self.__create_gcs_client()
    
    def upload_to_gcs(self, bucket_name: str, destination_blob_name: Optional[str], source_file_path: str):
        bucket = self.__get_bucket(bucket_name)
        if not destination_blob_name:
            destination_blob_name = self.__path_builder()
        if not self.__is_valid_blob(destination_blob_name):
            raise GCSUtilsError(GCSErrorTypes.INVALID_OBJECT_NAME)
        try:
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_path)
        except Forbidden:
            raise GCSUtilsError(GCSErrorTypes.PERMISSION_DENIED)
        except GoogleAPIError:
            raise GCSUtilsError(GCSErrorTypes.STORAGE_ERROR)
        
    def __create_gcs_client(self) -> storage.Client:
        """Creates a GCS client via creds from Google Secret Manager.
        
        Credentials are injected via apache-airflow-providers-google.

        Returns:
            storage.Client: A GCS client object.

        Raises:
            GCSUtilsError: If there is an authentication error when creating the GCS client.
        """
        try:
            gcs_client = storage.Client()
            # Create client with creds from secret manager, todo
        except DefaultCredentialsError:
            raise GCSUtilsError(GCSErrorTypes.AUTHENTICATION_ERROR)
        
        return gcs_client
    
    def __get_bucket(self, bucket_name: str) -> storage.Bucket:
        """Fetch a GCS bucket by name.
        
        Args:
            bucket_name (str): The name of the GCS bucket to fetch.
        
        Returns:
            storage.Bucket: The GCS bucket object.

        Raises:
            GCSUtilsError: If the bucket is not found or there is a permission issue.
        """
        try:
            bucket = self.gcs_client.bucket(bucket_name)
            return bucket
        except NotFound:
            raise GCSUtilsError(GCSErrorTypes.BUCKET_NOT_FOUND)
        except Forbidden:
            raise GCSUtilsError(GCSErrorTypes.PERMISSION_DENIED)

    def __is_valid_blob(self, blob_name: str):
        """Validate blob name against GCS naming conventions.
        
        Args:
            blob_name (str): The name of the blob to validate.

        Returns:
            bool: True if the blob name is valid, False otherwise.
        """
        valid_pattern = r'[:"<>|]'
        is_valid = not re.search(valid_pattern, blob_name)

        return is_valid

    def __path_builder(self):
        """Build a GCS path for the blob based on current date and time.
        
        
        """
        pass
        
    
class GCSErrorTypes(StrEnum):
    BUCKET_NOT_FOUND = "BucketNotFound"
    INVALID_OBJECT_NAME = "InvalidObjectName"
    PERMISSION_DENIED = "PermissionDenied"
    AUTHENTICATION_ERROR = "AuthenticationError"
    RATE_LIMIT_EXCEEDED = "RateLimitExceeded"
    STORAGE_ERROR = "StorageError"


class GCSUtilsError(Exception):
    ERROR_TYPES = {
        "BucketNotFound": "The specified bucket does not exist",
        "InvalidObjectName": "The specified object name is invalid",
        "PermissionDenied": "Insufficient permissions for this operation",
        "AuthenticationError": "Failed to authenticate with GCS",
        "RateLimitExceeded": "Too many requests to GCS, please try again later",
        "StorageError": "An error occurred while interacting with GCS",
    }

    def __init__(self, error_type: GCSErrorTypes):
        self.error_type = error_type
        self.message = self.ERROR_TYPES.get(error_type, "An unknown error occurred")
        super().__init__(f"{self.error_type}: {self.message}")