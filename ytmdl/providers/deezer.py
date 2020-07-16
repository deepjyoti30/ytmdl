"""
Python module to search deezer.com using their API.

Uses api.deezer.com to get search results.
"""

import requests

from .provider_base import Song, Provider


class Deezer(Provider):
    URL = 'https://api.deezer.com/'
    SEARCH_ROUTE = '{}search?q={}'
    EXTRA_TRACK_ROUTE = '{}track/{}'
    EXTRA_ALBUM_ROUTE = '{}album/{}'

    def __init__(self):
        super().__init__(name='deezer')

    # this is abstract in the base class
    def search_song(self, query, lim=40):
        """Deezer"""
        url = self.SEARCH_ROUTE.format(self.URL, query)
        r = requests.get(url)
        data = r.json()
        data = data['data']
        return [DeezerSong(song, self) for song in data]


class DeezerSong(Song):
    """Class to store deezer song tags."""

    def __init__(self, SONG, provider):
        """SONG is supposed to be a dict."""
        track_name = SONG['title_short']
        artist_name = SONG['artist']['name']
        collection_id = SONG['album']['id']
        track_id = SONG['id']
        collection_name = SONG['album']['title']
        artwork_url_100 = SONG['album']['cover_medium']
        duration = SONG['duration']
        super().__init__(track_name, artist_name, artwork_url_100, duration, provider,
                         collection_name=collection_name, collection_id=collection_id, track_id=track_id)

    # this is abstract in the base class
    def get_more_data(self):
        url_track = Deezer.EXTRA_TRACK_ROUTE.format(Deezer.URL, self.track_id)
        url_album = Deezer.EXTRA_ALBUM_ROUTE.format(
            Deezer.URL, self.collection_id)

        r = requests.get(url_track)
        data_track = r.json()

        r = requests.get(url_album)
        data_album = r.json()

        self.primary_genre_name = data_album['genres']['data'][0]['name']
        self.track_number = data_track['track_position']
        self.release_date = data_track['release_date']


if __name__ == '__main__':
    q = input("Enter the query: ")
    dat = Deezer.search_song(q)
    for i in range(0, len(dat)):
        print(dat[i].collection_name)
