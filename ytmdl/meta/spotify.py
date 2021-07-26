"""
Handle extracting metadata from Spotify

We will use Spotify's API to search for tracks and show them
to the user to be used accordingly.
"""

from spotipy import SpotifyClientCredentials
from spotipy import Spotify

from typing import Dict


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
