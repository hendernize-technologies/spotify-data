import logging
import datetime
import spotipy
from google.cloud import secretmanager
from google.api_core import exceptions as google_exceptions
from google.api_core import retry


class Helpers():
    """
    Utility package for the Spotify Extract Load (ELT) pipeline.

    This class contains all the helper functions for interacting with the Spotify API, Cloud Storage, and BigQuery.

    Class methods:
        __init__: Initializes the class and sets up the logger.
        _get_secret: Fetches a secret from Google Secret Manager.
        _get_api_conn: Fetches an API connection to the Spotify API.
        _initial_auth_setup: Logic to generate refresh token.
        upload_to_gcs: Uploads data to Google Cloud Storage.
        download_from_gcs: Downloads data from Google Cloud Storage.
        __set_logger: Sets up the logger.

    Class attributes:
        logger: The logger for the class.
        scope: The scope for the Spotify API.
        secret_client: The client for the Google Secret Manager.
        client_id: The client ID for the Spotify API.
        client_secret: The client secret for the Spotify API.
        refresh_token: The refresh token for the Spotify API.
    """

    def __init__(self):
        try:
            self.logger = self.__set_logger()
            self.logger.debug('Logger initialized for %s',
                              self.__class__.__name__)
        except:
            raise ValueError(
                'Could not initialize logger for %s', self.__class__.__name__)

        self.scope = "user-library-read user-read-private user-read-email user-top-read"
        self.secret_client = "secretmanager.SecretManagerServiceClient()"

        self.client_id = self._get_secret('SPOTIFY_CLIENT_ID')
        self.client_secret = self._get_secret('SPOTIFY_CLIENT_SECRET')
        self.refresh_token = self._get_secret('SPOTIFY_REFRESH_TOKEN')

    # TODO - implement retry logic
    def _get_secret(self, secret_name: str):
        """
        Gets a secret from Google Secret Manager.

        Args:
            secret_name: The name of the secret to fetch.

        Returns:
            str: The secret value.

        Raises:
            ValueError: If the secret is not found or there is an unexpected error. 
        """

        try:
            name = f"projects/{os.getenv('GCP_PROJECT')}/secrets/{secret_name}/versions/latest"
            response = self.secret_client.access_secret_version(
                request={"name": name})
            return response.payload.data.decode("UTF-8")

        except google_exceptions.PermissionDenied:
            self.logger.error(
                f"Permission denied accessing secret: {secret_name}")
            raise ValueError(f"No permission to access secret: {secret_name}")

        except google_exceptions.NotFound:
            self.logger.error(f"Secret not found: {secret_name}")
            raise ValueError(f"Secret does not exist: {secret_name}")

        except google_exceptions.ResourceExhausted:
            self.logger.error(
                f"Rate limit exceeded when accessing secret: {secret_name}")
            raise ValueError("Too many requests to Secret Manager")

        except Exception as e:
            self.logger.error(
                f"An unexpected error occurred while attempting to fetch {secret_name}: {str(e)}")
            raise ValueError(
                f"Failed to retrieve secret {secret_name} due to unexpected error {str(e)}")

    def _get_api_conn(
        self,
        client_id: str,
        client_secret: str,
        scope: str
    ):
        sp_oauth = spotipy.oauth2.SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://localhost/callback",
            scope=scope
        )

        token_info = sp_oauth.refresh_access_token(self.refresh_token)
        token = token_info['access_token']

        if not token:
            raise ConnectionError('Could not get an API token for Spotify')

        sp = spotipy.Spotify(auth=token)

        return sp

    def _initial_auth_setup(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope: str
    ):
        """
        Logic to generate refresh token.

        This is a one-time setup to get the refresh token needed for the Authorization Code Flow.
        """
        auth_manager = spotipy.oauth2.SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://localhost/callback",
            scope=scope
        )

        """This generates the URL to visit in the browser"""
        auth_url = auth_manager.get_authorize_url()
        self.logger.info(f"\nVisit this URL to authorize: {auth_url}\n")

        """After browser authorization, you'll be redirected to localhost with a code"""
        response = input("Enter the URL you were redirected to: ")
        code = auth_manager.parse_response_code(response)
        token_info = auth_manager.get_access_token(code)

        """Save the refresh token"""
        refresh_token = token_info['refresh_token']
        return refresh_token

    def upload_to_gcs(self):
        pass

    def download_from_gcs(self):
        pass

    def __set_logger(self):
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            stream_handler.setFormatter(formatter)

            logger.addHandler(stream_handler)

        return logger
