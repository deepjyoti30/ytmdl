"""Functions used in setting up the config file are defined here."""

import os
import re
from simber import Logger
from xdg.BaseDirectory import xdg_config_home


config_text = '''#*****************************************#
#*-------------config for ytmdl-----------#
#
#-----------------------------------------#
#------PLEASE DON\'T LEAVE ANY BLANK LINES---#
#-----------------------------------------#
#
# To change defaults just remove the hash(#)
# from the beginning of the line.
#
#*****************************************
# The SONG_DIR is the directory where all the songs will be saved.
# In order to change it, simply remove the hash from beginning
# And change the path to your desired one.
# In case the path has spaces in in, include it in a " "
# Following is a simple folder path example
#
#SONG_DIR = "path/to/your/desired/folder"
#
#************--------ADVANCED-------*********
# If you want to save the song in custom folders than those can be
# added to the name like the following example.
# The possible values are following
#
# Artist --> Song Artist
# Album  --> Song Album Name
# Title  --> Song Name
# Genre  --> Song Genre
# TrackNumber --> Song Number in the album
# ReleaseDate --> Song Release date
#
# Following is an example of the format
#SONG_DIR = "/home/user/Music$Artist->Album->Title"
#
#*****************************************#
# The QUALITY is the quality of the song in kbps
# By default it is set to 320kbps
# In case you want to change it to something else,
# Uncomment the following line and change it
#
# Supported values are 320 and 192
#
#QUALITY = "320"
#
#*****************************************#
# The METADATA_PROVIDERS value is a comma separated
# values that specifies wich API providers to use for getting
# the song metadata. Available values right now are:
#
# ---------
# "{{supported_providers}}".
# ---------
#
# Please check the github page of ytmdl for more information.
#
#METADATA_PROVIDERS = "itunes, spotify, gaana"
#
#*****************************************#
# The DEFAULT_FORMAT denotes what to use as default for downloading.
# Available values are:
#
# ---------
# "{{supported_formats}}"
# ---------
#
#DEFAULT_FORMAT = "mp3"
#
#*****************************************#
# What to do when something goes wrong while adding the metadata. This can
# happen for various reasons like lack of metadata or network issues.
# Available options are:
#
# ---------
# "{{supported_on_error_options}}"
# ---------
#
#ON_META_ERROR = "exit"
#****************************************#
# ITUNES SETTINGS
# Which region to use while searching from Itunes.
#
#
# Country where the song is to be searched for in Itunes.
# The country helps if you're looking for regional songs in
# which case Itunes orders the results accordingly.
#
# By default, 'US' will be used.
#
#ITUNES_COUNTRY = "US"
#
# Country where the song is to be searched for in Spotify.
# The country helps if you're looking for regional songs in
# which case Spotify orders the results accordingly.
#
# By default, 'US' is used
#
#SPOTIFY_COUNTRY = "US"
#'''


logger = Logger("config")


class DEFAULTS:
    """Some default stuff defined."""

    def __init__(self):
        # The home dir
        self.HOME_DIR = os.path.expanduser('~')

        # The default song dir
        self.SONG_DIR = self._get_music_dir()

        # The temp dir
        self.SONG_TEMP_DIR = os.path.join(self.SONG_DIR, 'ytmdl')

        # The default song quality
        self.SONG_QUALITY = '320'

        # The config path
        self.CONFIG_PATH = os.path.join(xdg_config_home, 'ytmdl')

        # The default metadata providers
        self.METADATA_PROVIDERS = ['itunes', 'spotify', 'gaana']

        # The available metadata providers
        self.AVAILABLE_METADATA_PROVIDERS = self.METADATA_PROVIDERS + \
            ['deezer', 'lastfm', 'musicbrainz', 'saavn']  # add new ones here

        self.VALID_FORMATS = ['mp3', 'm4a', 'opus']

        self.DEFAULT_FORMAT = 'mp3'

        self.ON_ERROR_OPTIONS = ['exit', 'skip', 'manual']

        self.ON_ERROR_DEFAULT = 'exit'

        # Itunes related settings
        self.ITUNES_COUNTRY_DEFAULT = "US"

        # Spotify country
        self.SPOTIFY_COUNTRY_DEFAULT = "US"

    def _get_music_dir(self):
        """Get the dir the file will be saved to."""
        # The first preference will be ~/Music.
        # If that is not present, try checking the XDG_MUSIC_DIR
        # If still not, then use the current directory.
        music_dir = self._get_xdg_dir()

        if music_dir is None:
            music_dir = os.path.join(self.HOME_DIR, 'Music')

        if not os.path.exists(music_dir):
            music_dir = os.getcwd()

        return music_dir

    def _get_xdg_dir(self):
        """Get the xdg dir."""
        file_path = os.path.expanduser('~/.config/user-dirs.dirs')

        if not os.path.exists(file_path):
            return None

        with open(file_path, 'r') as RSTREAM:
            data = RSTREAM.read()
            path = re.findall(r'\nXDG_MUSIC_DIR.*?\n', str(data))
            if not path:
                return None
            path = re.sub(r'\n|XDG_MUSIC_DIR|=|"', '', path[0])
            path = os.path.expandvars(path)
            return path


def render_config_template() -> str:
    """Render the config template in order ot get the updated
    config
    """
    defaults_obj = DEFAULTS()
    providers = ", ".join(defaults_obj.AVAILABLE_METADATA_PROVIDERS)
    formats = ", ".join(defaults_obj.VALID_FORMATS)
    on_error_options = ", ".join(defaults_obj.ON_ERROR_OPTIONS)

    KEYWORD_MAP = {
        '"{{supported_providers}}"': providers,
        '"{{supported_formats}}"': formats,
        '"{{supported_on_error_options}}"': on_error_options
    }

    rendered_content = config_text

    for keyword, value in KEYWORD_MAP.items():
        rendered_content = rendered_content.replace(keyword, value)

    return rendered_content


def make_config():
    """Copy the config file to .config folder."""
    # Remove the current config from SONG_TEMP_DIR
    config_path = os.path.join(DEFAULTS().CONFIG_PATH, 'config')

    # Check if the ytmdl folder is present in config
    if not os.path.isdir(DEFAULTS().CONFIG_PATH):
        # Make the ytmdl folder
        os.makedirs(DEFAULTS().CONFIG_PATH, exist_ok=True)

    elif os.path.isfile(config_path):
        os.remove(config_path)

    # Check if the ytmdl folder is present in Music directory
    if not os.path.isdir(DEFAULTS().SONG_TEMP_DIR):
        # Make the ytmdl folder
        os.makedirs(DEFAULTS().SONG_TEMP_DIR)

    # Now write the config text to config file
    with open(config_path, 'w') as write_config:
        write_config.write(render_config_template())


def checkConfig():
    """Need to check the config to see if defaults are changed.

    The config will be saved in the .config folder.
    """
    # Try to see if the config is present in the SONG_TEMP_DIR

    if os.path.isdir(DEFAULTS().CONFIG_PATH):
        DIR_CONTENTS = os.listdir(DEFAULTS().CONFIG_PATH)
    else:
        return False

    if 'config' not in DIR_CONTENTS:
        make_config()
        return True
    else:
        return True


def check_config_setup():
    """
    Method to check if the config file is setup.

    This is different from the above method because
    it will check if the config is setup and not do
    anything about it.

    The return value can be used to perform on config
    setup etc.
    """
    # There are two possibilities that might indicate
    # that the config is not setup.
    DEFAULT_CONF_PATH = DEFAULTS().CONFIG_PATH

    # Check if ytmdl config directory is present
    if not os.path.isdir(DEFAULT_CONF_PATH):
        return False

    # Check if config file is present
    if not os.path.isfile(os.path.join(DEFAULT_CONF_PATH, 'config')):
        return False

    # Else it's probably setup
    return True


def checkValidity(keyword, value):
    """Check if the user specified value in config is possible."""
    if keyword == 'SONG_DIR':
        # In this case check if $ and -> are present
        # If they are then only check if the base dir exists
        if '$' in value:
            pos = value.find('$')
            value = value[:pos]
        return os.path.isdir(os.path.expanduser(value))
    elif keyword == 'QUALITY':
        # Possible values that QUALITY can take
        possQ = ['320', '192']
        return value in possQ
    elif keyword == 'DEFAULT_FORMAT':
        possF = DEFAULTS().VALID_FORMATS
        return value in possF
    elif keyword == 'METADATA_PROVIDERS':
        # Possible values that METADATA_PROVIDERS can take
        possM = DEFAULTS().AVAILABLE_METADATA_PROVIDERS
        if not value:
            logger.warning(
                "Metadata provider value is empty. \
                    Default values will be used.")
            return False
        new_val = value.replace(' ', '').split(',')

        # Even if one is valid, return true
        for provider in new_val:
            if provider in possM:
                return True
        return False
    elif keyword == "ON_META_ERROR":
        if not value:
            logger.warning("On meta error value is empty. \
                    Default will be used")
            return False

        if value not in DEFAULTS().ON_ERROR_OPTIONS:
            return False
        return True

    elif keyword == "ITUNES_COUNTRY":
        if not value:
            logger.warning("Itunes Country value is empty. \
                Default will be used")
            return False

        # TODO: Perhaps check if valid country
        return True

    elif keyword == "SPOTIFY_COUNTRY":
        if not value:
            logger.warning("Spotify Country value is empty. \
                Default will be used")
            return False

        # TODO: Perhaps check if valid country
        return True


def retDefault(keyword):
    """Return the DEFAULT value of keyword."""
    if keyword == 'QUALITY':
        return DEFAULTS().SONG_QUALITY
    elif keyword == 'DEFAULT_FORMAT':
        return DEFAULTS().DEFAULT_FORMAT
    elif keyword == 'SONG_DIR':
        return DEFAULTS().SONG_DIR
    elif keyword == 'METADATA_PROVIDERS':
        return DEFAULTS().METADATA_PROVIDERS
    elif keyword == "ON_META_ERROR":
        return DEFAULTS().ON_ERROR_DEFAULT
    elif keyword == "ITUNES_COUNTRY":
        return DEFAULTS().ITUNES_COUNTRY_DEFAULT
    elif keyword == "SPOTIFY_COUNTRY":
        return DEFAULTS().SPOTIFY_COUNTRY_DEFAULT


def GIVE_DEFAULT(self, keyword):
    """Check if the user has uncommented the config and added something.

    If possible get what is changed, else return the default value.
    """
    # Check If the config is already present in SONG_TEMP_DIR
    if not checkConfig():
        return retDefault(keyword)
    else:
        # Then read from it
        READ_STREAM = open(os.path.join(DEFAULTS().CONFIG_PATH, 'config'), 'r')

        while True:
            line = READ_STREAM.readline()
            if not line:
                return retDefault(keyword)
            if line[0] != '#' and keyword in line:
                # Get the position of =
                index_equal = line.index('=')
                if line[index_equal + 1] == ' ':
                    newDEFAULT = line[index_equal + 2:]
                else:
                    newDEFAULT = line[index_equal + 1:]

                # Remove the "
                newDEFAULT = newDEFAULT.replace('"', '')
                newDEFAULT = newDEFAULT.replace("'", '')
                # Check if the line has a \n in it
                if "\n" in line:
                    newDEFAULT = newDEFAULT.replace('\n', '')

                if checkValidity(keyword, newDEFAULT):
                    return newDEFAULT
                else:
                    if newDEFAULT:
                        logger.warning(
                            "{}: is invalid for option {}.".format(newDEFAULT, keyword))
                    return retDefault(keyword)


if __name__ == '__main__':
    # Create the config in the examples directory
    try:
        with open("examples/config", 'w') as write_config:
            write_config.write(render_config_template())
    except Exception:
        print("You need to run this script in root directory of ytmdl")
