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
        pass


def search_song(query, limit: int = 25) -> List[SpotifySong]:
    """
    Search the song using the API through spotipy
    and accordingly return the results.
    """
    spotify = Spotify(SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

    response = spotify.search(f"track:{query}", limit=limit, type="track")
    items = [SpotifySong(item) for item in response["tracks"]["items"]]

    return items
