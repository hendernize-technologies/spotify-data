import os
import requests
from google.cloud import language_v1
import spacy
from spacy.matcher import Matcher
from google.oauth2 import service_account
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import grequests

class SpotifyTool:
    def __init__(self) -> None:
        try:
            self.api_conn = self.get_api()
            self.endpoint_url = 'https://api.spotify.com'
        except:
            print("Could not initialize Spotify tool class - check API creds")

    def get_api(self):

        redirect_uri = 'tbd'
        access_id = os.environ.get('SPOTIFY_ID')
        access_secret = os.environ.get('SPOTIFY_SECRET')
        auth = SpotifyOAuth(
            client_id = access_id,
            client_secret = access_secret,
            redirect_uri = redirect_uri
        )

        api = spotipy.Spotify(auth)
        return api

    def fetch_data(self):
        # Logic for pulling listening datafrom Spotify
        pass

    def process_data(self):
        # Logic for formatting listening data
        pass

    def import_to_bq(self):
        # Logic for importing to BQ
        pass

    


