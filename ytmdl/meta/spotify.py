"""
Handle extracting metadata from Spotify

We will use Spotify's API to search for tracks and show them
to the user to be used accordingly.
"""

from spotipy import SpotifyClientCredentials
from spotipy import Spotify

from typing import Dict, List

# Yeah I know, this is not a good idea but
# asking the users for their own credentials is jus
# not good enough.
# NOTE: Raise an issue if you have a better idea
# and NO, I don't wanna ask the user to enter these
# creds.
CLIENT_ID = "a166f23a5637429e8bd819df46fa034e"
CLIENT_SECRET = "bbad17df3cde471ab969f081f2ea8bbb"


class SpotifySong(object):
    """
    Class to store data about the songs fetched from
    Spotify.

    We need to clean the data into an object that can
    be utilized if the user choses to add this song as
    metadata.
    """

    def __init__(self, song: Dict) -> None:
        self.track_name = song["name"]
        self.release_date = song["album"]["release_date"]
        self.artist_name = song["artists"][0]["name"]
        self.provider = "spotify"
        self.collection_name = song["album"]["name"]
        self.primary_genre_name = ""  # Seems spotify doesn't provide genre
        self.track_number = song["track_number"]
        self.artwork_url_100 = song["album"]["images"][0]["url"]
        self.track_time = song["duration_ms"]


def search_song(
    query,
    country: str = "US",
    limit: int = 25
) -> List[SpotifySong]:
    """
    Search the song using the API through spotipy
    and accordingly return the results.
    """
    spotify = Spotify(auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

    response = spotify.search(
        f"track:{query}", limit=limit, type="track", market=country)
    items = [SpotifySong(item) for item in response["tracks"]["items"]]

    return items


def get_track_from_spotify(id, country: str = "US"):
    """
    Lookup the metadata by using the ID on spotify
    """
    spotify = Spotify(auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

    track = spotify.track(id, market=country)
    return SpotifySong(track)
