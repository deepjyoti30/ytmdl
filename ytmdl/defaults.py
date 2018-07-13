"""Contains the definition of class DEFAULT."""
from ytmdl import setupConfig
import os


class DEFAULT:
    """DEFAULT class contains value of different paths."""

    # The home dir
    HOME_DIR = os.path.expanduser('~')

    # the directory where songs will be saved
    SONG_DIR = setupConfig.GIVE_DEFAULT(1, 'SONG_DIR')

    # the temp directory where songs will be modded
    SONG_TEMP_DIR = os.path.join(HOME_DIR, 'Music', 'ytmdl')

    # The path to keep cover image
    COVER_IMG = os.path.join(SONG_TEMP_DIR, 'cover.jpg')

    # The song quality
    SONG_QUALITY = setupConfig.GIVE_DEFAULT(1, 'QUALITY')
