import os
from google.oauth2 import service_account
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging


class SpotifyExtractLoad:
    """
    This is the main class for the Spotify Extract Load (ELT) pipeline.

    This class is responsible for fetching data from the Spotify API, processing the data, and importing it to BigQuery.

    Class methods:
        __init__: Initializes the class and sets up the logger.
        __set_logger: Sets up the logger.
        get_api_conn: Gets the Spotify API connection.
        fetch_data: Fetches data from the Spotify API.
        process_data: Processes the data.
        import_to_bq: Imports the data to BigQuery.

    Class attributes:
        logger: The logger for the class.
        api_conn: The Spotify API connection.
    """

    def __init__(self) -> None:
        self.logger = self.__set_logger()
        self.logger.debug('Logger initialized for %s', self.__class__.__name__)

        try:
            self.api_conn = self.get_api_conn()
        except:
            self.logger.debug(
                'Could not initialize connection to Spotify API. Please check API creds.')

    def __set_logger(self):
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.DEBUG)

        """Add StreamHandler and Formatter"""
        if not logger.handlers:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            stream_handler.setFormatter(formatter)

            logger.addHandler(stream_handler)

        return logger

    def _get_api_conn(self):
        # TODO - in progress, being refactored
        # Get auth token from env
        try:
            SPOTIPY_TOKEN = os.getenv('SPOTIPY_TOKEN')
            api_conn = spotipy.Spotify(auth=SPOTIPY_TOKEN)
        except:
            print('Could not get API token for auth flow - refreshing token...')
            # logic for refresh?

        return api_conn

    def _fetch_data(self):

        # Logic for pulling listening data from Spotify
        results = self.api_conn.current_user_saved_tracks()
        for idx, item in enumerate(results['items']):
            track = item['track']
            print(idx, track['artists'][0]['name'], " – ", track['name'])

        track = self.api_conn.current_user_top_tracks(
            limit=20,
            offset=0,
            time_range='medium_term'
        )

        print(track)

    def _process_data(self):
        # Logic for formatting listening data
        pass

    def import_to_bq(self):
        # Logic for importing to BQ
        pass


if __name__ == "__main__":
    spotify = SpotifyExtractLoad()
    spotify.fetch_data()
