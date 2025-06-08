import json
from typing import Optional

import requests
from utils.helpers import Utils


class SpotifyAPIError(Exception):
    ERROR_TYPES = {
        "400": "Invalid Request",
        "401": "Authentication Error",
        "403": "Authorization Error",
        "404": "Resource Not Found",
        "429": "Rate Limit Exceeded",
        "500": "Internal Server Error",
        "502": "Bad Gateway",
        "503": "Service Not Available",
    }

    def __init__(self, message: str = None, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        self.api_url = "https://api.spotify.com/"
        self.logger = Utils.__set_logger()
        self.credentials = {}
        super().__init__()


class SpotifyClient:
    def __init__(
        self, credential_path: str = None, api_url: str = "https://api.spotify.com/"
    ):
        self.api_url = api_url
        self.credentials = self._load_credential_path(credential_path=credential_path)

    def _load_credential_path(self, credential_path: str):
        try:
            with open(file=credential_path, mode="r") as f:
                self.credentials = json.load(f)

            required_keys = [
                "spotify_client_id",
                "spotify_client_secret",
                "spotify_refresh_token",
                "client_scope",
            ]
            missing_keys = [key for key in required_keys if key not in self.credentials]

            if missing_keys:
                raise ValueError(
                    f"The following required keys are missing: {', '.join(missing_keys)}"
                )
        except (json.JSONDecodeError, IOError) as e:
            self.logger.error("Failed to load credentials from path")
            raise SpotifyAPIError(f"Failed to load {credential_path}: {str(e)}")

    def _call_api(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> dict:
        """
        Generic method for calling any Spotify API endpoint.

        Args:
            method (str): The REST API method being used (GET, POST, etc.).
            endpoint (str): The Spotify API endpoint to be called.
            params (dict, optional): The query parameters passed with the API call.
            data (dict, optional): The data passed during the API call.

        Returns:
            JSON object of results.

        Raises:
            TBD
        """
        api_url = self.api_url + endpoint
        try:
            response = requests.request(
                method=method, url=api_url, params=params, data=data
            )

            if response.status_code >= 400:
                raise SpotifyAPIError("TBD")

        except requests.RequestException:
            self.logger.error("ERror")
            raise SpotifyAPIError(
                f"Exception while making request to {endpoint}: (str)"
            )


# TODO retry logic, handle error response
