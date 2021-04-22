"""
Python module to search deezer.com using their API.

Uses api.deezer.com to get search results.
"""

import requests

DEEZER_URL = "https://api.deezer.com/"

search_url = "{}search?q={}"

url_extra_track = "{}track/{}"
url_extra_album = "{}album/{}"

SONG = []


class DeezerSongs():
    """Class to store deezer song tags."""

    def __init__(self, SONG):
        """SONG is supposed to be a dict."""
        self.track_name = SONG['title_short']
        self.artist_name = SONG['artist']['name']
        self.provider = 'deezer'
        self.collection_id = SONG['album']['id']
        self.track_id = SONG['id']
        self.track_number = "1"
        self.collection_name = SONG['album']['title']
        self.artwork_url_100 = SONG['album']['cover_medium']
        self.track_time = self._convert_time(SONG['duration'])

    def _convert_time(self, duration):
        in_min = int(duration)
        in_time = int(in_min / 60) + (0.01 * (in_min % 60))
        return in_time


def get_more_data(song):
    url_track = url_extra_track.format(DEEZER_URL, song.track_id)
    url_album = url_extra_album.format(DEEZER_URL, song.collection_id)

    r = requests.get(url_track)
    data_track = r.json()

    r = requests.get(url_album)
    data_album = r.json()

    song.primary_genre_name = data_album['genres']['data'][0]['name']
    song.track_number = data_track['track_position']
    song.release_date = data_track['release_date']

    return song


def searchSong(query, lim=40):
    """Deezer"""
    url = search_url.format(DEEZER_URL, query)
    r = requests.get(url)
    data = r.json()
    data = data['data']
    SONG_TUPLE = []

    if data:
        for i in range(0, len(data)):
            song_obj = DeezerSongs(data[i])
            SONG_TUPLE.append(song_obj)
    return SONG_TUPLE


if __name__ == '__main__':
    q = input("Enter the query: ")
    dat = searchSong(q)
    for i in range(0, len(dat)):
        print(dat[i].collection_name)
