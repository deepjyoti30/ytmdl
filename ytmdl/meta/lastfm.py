"""Handle data extraction from the Last.FM API

This module will handle everything related to extracting
the required data from the Last.FM source.
"""

from requests import get

API_BASE = "http://ws.audioscrobbler.com/2.0/"
API_KEY = "865e60e7cf58e028c063cb1230c95e5e"


class LastFMSongs():
    """Class to store Last FM song tags."""

    def __init__(self, SONG):
        """SONG is supposed to be a dict.

        All the empty attributes will be filled up in
        the extra feature fetching function.
        """
        self.track_name = SONG['name']
        self.artist_name = SONG['artist']
        self.provider = 'lastfm'
        self.track_number = "1"
        self.collection_name = ""
        self.release_date = ""
        self.artwork_url_100 = SONG["image"][-1]["#text"]
        self.track_time = ""
        self.primary_genre_name = "N/A"

    def _convert_time(self, duration):
        """duration is in ms"""
        in_sec = int(int(duration) / 1000)
        in_time = int(in_sec / 60) + (0.01 * (in_sec % 60))
        return in_time


def get_more_data(song):
    """song is a LastFMSong object.

    We can easily fetch the artist and track name and
    according get the extra required data from the API.
    """
    headers = {
        "User-Agent": "ytmdl"
    }
    payload = {
        "api_key": API_KEY,
        "method": "track.getInfo",
        "track": song.track_name,
        "artist": song.artist_name,
        "format": "json"
    }

    response = get(API_BASE, headers=headers, params=payload)

    # TODO: Add a check to exit if the response code is not 200

    track_details = response.json()

    # Update the songs attributes
    song.track_number = 1

    try:
        song.collection_name = track_details["track"]["album"]["title"]
        song.track_time = song._convert_time(
            track_details["track"]["duration"])
        song.release_date = track_details["track"]["wiki"]["published"]
    except KeyError:
        # This happens because last.fm do not have consistent data for some songs
        # Just ignore this errors if they occur.
        pass

    return song


def searchSong(query, lim=40):
    """Search the song using the last.fm API
    """
    headers = {
        "User-Agent": "ytmdl"
    }
    payload = {
        "api_key": API_KEY,
        "method": "track.search",
        "track": query,
        "format": "json"
    }

    data = []

    response = get(API_BASE, headers=headers, params=payload)

    if response.status_code != 200:
        print(response.status_code)
        return data

    for song in response.json()["results"]["trackmatches"]["track"]:
        data.append(LastFMSongs(song))

    return data


if __name__ == "__main__":
    songs = searchSong("Believer")
    song = get_more_data(songs[0])

    print(song.track_name, song.artist_name)
    print(song.collection_name, song.track_time, song.release_date)
