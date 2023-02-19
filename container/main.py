import os
from google.oauth2 import service_account
import spotipy
import spotipy.util as util

class SpotifyTool:
    def __init__(self) -> None:
        try:
            self.api_conn = self.get_api_conn()
        except:
            print("Could not initialize Spotify tool class - check API creds")

    def get_api_conn(self):

        # Get auth token from env
        try:
            SPOTIPY_TOKEN = os.getenv('SPOTIPY_TOKEN')
            api_conn = spotipy.Spotify(auth=SPOTIPY_TOKEN)
        except:
            print('Could not get API token for auth flow - refreshing token...')
            # logic for refresh?
        
        return api_conn

    def fetch_data(self):
        
        # Logic for pulling listening data from Spotify
        results = self.api_conn.current_user_saved_tracks()
        for idx, item in enumerate(results['items']):
            track = item['track']
            print(idx, track['artists'][0]['name'], " – ", track['name'])

    def process_data(self):
        # Logic for formatting listening data
        pass

    def import_to_bq(self):
        # Logic for importing to BQ
        pass

if __name__ == "__main__":
    spotify = SpotifyTool()
    spotify.fetch_data()
