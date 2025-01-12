import os
from google.oauth2 import service_account
from helpers import Helpers


class SpotifyExtractLoad(Helpers):
    """
    This is the main class for the Spotify Extract Load (ELT) pipeline.

    This class is responsible for fetching data from the Spotify API, processing the data, and importing it to BigQuery.

    Class methods:
        __init__: Initializes the class and sets up the logger.
        _fetch_data: Fetches data from the Spotify API.
        _process_data: Processes the data.
        _import_to_bq: Imports the data to BigQuery.

    Class attributes:
        api_conn: The Spotify API connection.
    """

    def __init__(self) -> None:
        super().__init__()

        try:
            self.api_conn = self._get_api_conn(
                client_id=self.client_id,
                client_secret=self.client_secret,
                scope=self.scope
            )
        except:
            self.logger.debug(
                'Could not initialize connection to Spotify API. Please check API creds.')

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

        user_profile = self.api_conn.current_user()
        print(user_profile)

    def _process_data(self):
        # Logic for formatting listening data
        pass

    def import_to_bq(self):
        # Logic for importing to BQ
        pass


if __name__ == "__main__":
    spotify = SpotifyExtractLoad()
    spotify._fetch_data()
