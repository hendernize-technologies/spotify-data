import os
from google.oauth2 import service_account
import requests
import base64

class SpotifyTool:
    def __init__(self) -> None:
        try:
            self.api_conn = self.get_api()
            self.endpoint_url = 'https://api.spotify.com'
        except:
            print("Could not initialize Spotify tool class - check API creds")

    def get_api(self):

        access_id = os.getenv('SPOTIFY_CLIENT_ID')
        access_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
        scopes = "user-read-private user-read-email"
        
        try:
            auth_url = "https://accounts.spotify.com/api/token"
            headers = {}
            data = {}

            message = f"{access_id}:{access_secret}"
            messageBytes = message.encode('ascii')
            base64Bytes = base64.b64encode(messageBytes)
            base64Message = base64Bytes.decode('ascii')

            headers['Authorization'] = f"Basic {base64Message}"
            data['grant_type'] = "client_credentials"

            r = requests.post(url=auth_url, headers=headers, data=data)
        except:
            print("Could not get bearer token")
        
        
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


