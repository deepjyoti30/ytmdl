"""
Handle all the util functions for working with YouTube Music.
"""


from ytmusicapi import YTMusic


def get_title() -> str:
    """
    Get the title of the song from the videoID.

    Youtube actually supports Youtube videoId's
    that can be found in YouTube Music with the
    proper song title.

    This is way more effective and correct than
    extracting the title from the YouTube video.
    """
    pass
