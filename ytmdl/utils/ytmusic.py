"""
Handle all the util functions for working with YouTube Music.
"""

from ytmusicapi import YTMusic
from simber import Logger

from ytmdl.exceptions import ExtractError


# Create logger
logger = Logger("ytmusic")


def get_title_from_ytmusic(videoId: str) -> str:
    """
    Get the title of the song from the videoID.

    Youtube actually supports Youtube videoId's
    that can be found in YouTube Music with the
    proper song title.

    This is way more effective and correct than
    extracting the title from the YouTube video.
    """
    ytmusic = YTMusic()

    details = ytmusic.get_song(videoId=videoId)

    # Check if error occured
    if details["playabilityStatus"]["status"] != "OK":
        raise ExtractError(videoId)

    try:
        return details["videoDetails"]["title"]
    except KeyError:
        raise ExtractError(videoId)
