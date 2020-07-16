"""
Python wrapper for itunespy
"""

import requests
import itunespy

from .provider_base import Song, Provider


class iTunes(Provider):

    def __init__(self):
        super().__init__(name='itunes')

    # this is abstract in the base class
    def search_song(self, query, lim=40):
        """iTunes"""
        songs = itunespy.search_track(query)
        return [iTunesSong(song, self) for song in songs]


class iTunesSong(Song):
    """Class to store deezer song tags."""

    def __init__(self, SONG, provider):
        """SONG is supposed to be a dict."""
        track_name = SONG.track_name
        artist_name = SONG.artist_name
        collection_id = SONG.collection_id
        track_id = SONG.track_id
        collection_name = SONG.collection_name
        artwork_url_100 = SONG.artwork_url_100
        duration = SONG.track_time
        primary_genre_name = SONG.primary_genre_name
        track_number = SONG.track_number
        release_date = SONG.release_date
        super().__init__(track_name, artist_name, artwork_url_100, duration, provider,
                         collection_name=collection_name, collection_id=collection_id, track_id=track_id,
                         primary_genre_name=primary_genre_name, track_number=track_number, release_date=release_date)

    # this is abstract in the base class
    # we don't need more data
    def get_more_data(self):
        pass


if __name__ == '__main__':
    q = input("Enter the query: ")
    dat = iTunes.search_song(q)
    for i in range(0, len(dat)):
        print(dat[i].collection_name)
