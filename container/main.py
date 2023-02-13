import os
from google.oauth2 import service_account
import requests

class SpotifyTool:
    def __init__(self) -> None:
        try:
            self.api_conn = self.get_api()
            self.endpoint_url = 'https://api.spotify.com'
        except:
            print("Could not initialize Spotify tool class - check API creds")

    def get_api(self):

        redirect_uri = 'http://localhost'
        access_id = os.getenv('SPOTIPY_CLIENT_ID')
        access_secret = os.getenv('SPOTIFY_SECRET')
        scopes = 'user-read-private user-read-email'
        try:
            AUTH_URL = 'https://accounts.spotify.com/api/token'
            auth_resp = requests.post(AUTH_URL, {
                'grant_type': 'client_credentials',
                'client_id': access_id,
                'client_secret': access_secret
            })

            data = auth_resp.json()
            print(data)
            # resp = requests.request(
            #     'GET',
            #     'https://accounts.spotify.com/authorize',
            #     {
            #         'response_type': 'code',
            #         'client_id': access_id,

            #     }
            # )
            # print(resp.status_code)
        except:
            print("Could not get bearer token")
        
        
        header = {

        }
        
        
        # return api

    def fetch_data(self):
        # Logic for pulling listening datafrom Spotify
        results = self.api_conn.current_user_saved_tracks()
        for idx, item in enumerate(results['items']):
            track = item['track']
            print(idx, track['artists'][0]['name'], " – ", track['name'])
        # pass

    def process_data(self):
        # Logic for formatting listening data
        pass

    def import_to_bq(self):
        # Logic for importing to BQ
        pass

if __name__ == "__main__":
    spotify = SpotifyTool()
    spotify.get_api()


