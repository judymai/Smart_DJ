from spotipy.oauth2 import SpotifyClientCredentials

import spotipy
import os

SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

client_credentials = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials)

def get_artist_hits(artist_name):
    results = sp.search(q=artist_name,limit=1,offset=0,type='artist')
    artist_uri = results['artists']['items'][0]['uri']
    return [i['uri'] for i in sp.artist_top_tracks(artist_uri)]
