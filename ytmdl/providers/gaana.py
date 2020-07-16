"""
Python module to search gaana.com using their API.

Uses api.gaana.com to get search results.
"""

import requests
from .provider_base import Song, Provider

# Define the base url
base_url = "http://api.gaana.com/?type=search&subtype=search_song&key={}&token=b2e6d7fbc136547a940516e9b77e5990&format=JSON"


class Gaana(Provider):
    URL = base_url

    def __init__(self):
        super().__init__(name='gaana')

    def search_song(self, query, lim=40):
        """Nanan."""
        url = base_url.format(query)
        r = requests.get(url)
        data = r.json()
        data = data['tracks']
        return [GaanaSong(song, self) for song in data]
        

class GaanaSong(Song):
    """Class to store gaana song tags."""

    def __init__(self, SONG, provider):
        """SONG is supposed to be a dict."""
        track_name = SONG['track_title']
        release_date = SONG['release_date']
        artist_name = SONG['artist'][0]['name']
        collection_name = SONG['album_title']
        primary_genre_name = SONG['gener'][0]['name']
        track_number = '1'
        artwork_url_100 = SONG['artwork_large']
        duration = SONG['duration']
        super().__init__(track_name, artist_name, artwork_url_100, duration, provider,
                         release_date=release_date, collection_name=collection_name,
                         primary_genre_name=primary_genre_name, track_number=track_number)

    # we don't need more data for this
    def get_more_data(self):
        pass


if __name__ == '__main__':
    q = input("Enter the query: ")
    dat = Gaana.search_song(q)
    for i in range(0, len(dat)):
        print(dat[i].collection_name)
