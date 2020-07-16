"""Contains the definition of class DEFAULT."""
from ytmdl.config import setup_config 
import os
from xdg.BaseDirectory import xdg_cache_home


def _providers_string_to_list(val):
    """Convert string to list if not already"""
    # Use a set to remove duplicates
    if type(val) == str:
        return list(set(val.replace(' ', '').split(',')))
    return list(set(val))


class DEFAULT:
    """DEFAULT class contains value of different constants."""

    HOME_DIR = os.path.expanduser('~')

    # The directory where songs will be saved
    SONG_DIR = setup_config.GIVE_DEFAULT(1, 'SONG_DIR')

    # The temp directory where songs will be modded
    SONG_TEMP_DIR = os.path.join(xdg_cache_home, 'ytmdl')

    COVER_IMG = os.path.join(SONG_TEMP_DIR, 'cover.jpg')

    SONG_QUALITY = setup_config.GIVE_DEFAULT(1, 'QUALITY')

    METADATA_PROVIDERS = _providers_string_to_list(
        setup_config.GIVE_DEFAULT(1, 'METADATA_PROVIDERS'))

    SEARCH_SENSITIVITY = float(setup_config.GIVE_DEFAULT(1, 'SEARCH_SENSITIVITY'))


class FORMAT:
    """
    Class to handle stuff related to the passed
    format.
    """
    valid_formats = [
        'mp3',
        'm4a'
    ]
