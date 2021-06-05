"""Module to handle meta fetch from musicbrainz"""

import musicbrainzngs
from ytmdl.__version__ import __version__

musicbrainzngs.set_useragent(
    "ytmdl",
    __version__,
    "https://github.com/deepjyoti30/ytmdl"
)


class MusicBrainzSong():
    """Class to store gaana song tags."""

    def __init__(self, SONG):
        """SONG is supposed to be a dict."""
        self.track_name = SONG['title']
        self.release_date = self.__get_date(SONG)
        self.artist_name = SONG['artist-credit'][0]['name']
        self.provider = "musicbrainz"
        self.collection_name = SONG['release-list'][0]['title']
        self.primary_genre_name = ""  # Seems musicbrainz doesn't provide genre
        self.track_number = SONG['release-list'][0]['medium-list'][0]['track-list'][0]['number']
        self.artwork_url_100 = ""
        self.track_time = self.__get_length(SONG)

        # Below will be used to fetch extra data
        self.__release_id = SONG['release-list'][0]['id']

    def __get_length(self, song):
        """Try to extract the length of the song"""
        try:
            return self._convert_time(song['length'])
        except KeyError:
            return ""

    def __get_date(self, song):
        """Try to extract the length of the song"""
        try:
            return song['release-list'][0]['date']
        except KeyError:
            return ""

    def _convert_time(self, duration):
        in_min = int(duration)
        in_time = int(in_min / 60) + (0.01 * (in_min % 60))
        return in_time

    @property
    def release_id(self) -> str:
        return self.__release_id


def search_song(query, lim=25):
    """Search the song using the API and return the
    results accordingly
    """
    recordings = musicbrainzngs.search_recordings(query)

    if not recordings:
        return []

    data = []

    recordings_results = recordings["recording-list"]
    for recording in recordings_results:
        data.append(MusicBrainzSong(recording))

    return data


def get_more_data(song):
    """Get extra data for the song like cover art"""
    id = song.release_id

    cover_art = musicbrainzngs.get_image_list(id)
    song.artwork_url_100 = cover_art["images"][0]["image"]

    return song


if __name__ == "__main__":
    data = search_song("Cradles")
    for i in data:
        print("{}:{}".format(i.track_name, i.artist_name))
