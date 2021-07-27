"""Contains the definition of class DEFAULT."""
from ytmdl import setupConfig
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

    def __parse_dir_path(dir_path: str):
        """
        Parse the passed directory path and return a proper
        string. This is for situations when the path might
        have something like a `~` in it.
        """
        if dir_path.startswith("~"):
            dir_path = os.path.expanduser(dir_path)

        return dir_path

    # The home dir
    HOME_DIR = os.path.expanduser('~')

    # The directory where songs will be saved
    SONG_DIR = __parse_dir_path(setupConfig.GIVE_DEFAULT(1, 'SONG_DIR'))

    # The temp directory where songs will be modded
    SONG_TEMP_DIR = os.path.join(xdg_cache_home, 'ytmdl')

    # The path to keep cover image
    COVER_IMG = os.path.join(SONG_TEMP_DIR, 'cover.jpg')

    # The song quality
    SONG_QUALITY = setupConfig.GIVE_DEFAULT(1, 'QUALITY')

    DEFAULT_FORMAT = setupConfig.GIVE_DEFAULT(1, 'DEFAULT_FORMAT')

    # The metadata providers
    METADATA_PROVIDERS = _providers_string_to_list(
        setupConfig.GIVE_DEFAULT(1, 'METADATA_PROVIDERS'))

    VALID_FORMATS = setupConfig.DEFAULTS().VALID_FORMATS

    ON_ERROR_OPTIONS = setupConfig.DEFAULTS().ON_ERROR_OPTIONS
    ON_ERROR_DEFAULT = setupConfig.GIVE_DEFAULT(1, 'ON_META_ERROR')

    ITUNES_COUNTRY = setupConfig.GIVE_DEFAULT(1, 'ITUNES_COUNTRY')

    SPOTIFY_COUNTRY = setupConfig.GIVE_DEFAULT(1, 'SPOTIFY_COUNTRY')
