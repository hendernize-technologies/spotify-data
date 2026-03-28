from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from google.api_core.exceptions import Forbidden, NotFound
from modules.client.gcs import GCSErrorTypes, GCSUtils, GCSUtilsError


class TestGCSUtils:
    @pytest.fixture
    def gcs_client(self):
        with patch("modules.client.gcs.storage.Client") as mock_client:
            mock_client.return_value = MagicMock()
            client = GCSUtils()
            yield client

    def test_bucket_found(self, gcs_client):
        bucket_name = "test_bucket_name"
        bucket = gcs_client._GCSUtils__get_bucket(bucket_name)
        assert bucket is not None

    def test_bucket_not_found(self, gcs_client):
        gcs_client.gcs_client.bucket.side_effect = NotFound("not found")
        with pytest.raises(GCSUtilsError) as exc_info:
            gcs_client._GCSUtils__get_bucket("fake_bucket")
            assert exc_info.value.error_type == GCSErrorTypes.BUCKET_NOT_FOUND

    def test_bucket_forbidden(self, gcs_client):
        gcs_client.gcs_client.bucket.side_effect = Forbidden("forbidden")
        with pytest.raises(GCSUtilsError) as exc_info:
            gcs_client._GCSUtils__get_bucket("forbidden_bucket")
            assert exc_info.value.error_type == GCSErrorTypes.PERMISSION_DENIED

    def test_valid_invalid_blob_names(self, gcs_client):
        valid_names = ["thisName_is-Valid", "AlsoValid", "Valid123"]
        valid_set = set()
        for name in valid_names:
            result = gcs_client._GCSUtils__is_valid_blob(name)
            valid_set.add(result)

        invalid_names = [":invalid", "<invalid", ">invalid", "|invalid"]
        invalid_set = set()
        for name in invalid_names:
            result = gcs_client._GCSUtils__is_valid_blob(name)
            invalid_set.add(result)

        assert True in valid_set
        assert len(valid_set) == 1
        assert False in invalid_set
        assert len(invalid_set) == 1

    def test_path_builder(self, gcs_client):
        path_combinations = [
            ("songs", "songs_3_28_2026.parquet", "3_28_2026"),
            ("songs", "songs_3_28_2026.parquet", "3-28-2026"),
            ("songs", "songs_3_28_2026.parquet", "3/28/2026"),
            ("songs", "songs_3_28_2026.parquet"),
        ]

        for path in path_combinations:
            endpoint = path[0]
            destination_filename = path[1]
            current_date = path[2] if len(path) == 3 else None
            result = gcs_client._GCSUtils__path_builder(
                endpoint, destination_filename, current_date
            )
            if not current_date:
                assert result == "songs/2026-03-28/songs_3_28_2026.parquet"
            else:
                formatted = date.today().strftime("%Y-%m-%d")
                assert result == f"songs/{formatted}/songs_3_28_2026.parquet"
