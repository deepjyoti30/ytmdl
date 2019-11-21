"""Functions used in setting up the config file are defined here."""

import os
import re
from ytmdl.logger import Logger
from xdg.BaseDirectory import xdg_config_home


config_text = '''#*****************************************#
#*-------------config for ytmdl ----------#
#
#-----------------------------------------#
#------PLEASE DON\'T LEAVE ANY BLANK LINE---#
#-----------------------------------------#
#
# To change defaults just remove the hash(#)
# from thw beginning of the line.
# The will be read as a single line comment.
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


def make_config():
    """Copy the config file to .config folder."""
    # Remove the current config from SONG_TEMP_DIR
    config_path = os.path.join(DEFAULTS().CONFIG_PATH, 'config')

    # Check if the ytmdl folder is present in config
    if not os.path.isdir(DEFAULTS().CONFIG_PATH):
        # Make the ytmdl folder
        os.makedirs(DEFAULTS().CONFIG_PATH)

    elif os.path.isfile(config_path):
        os.remove(config_path)

    # Check if the ytmdl folder is present in Music directory
    if not os.path.isdir(DEFAULTS().SONG_TEMP_DIR):
        # Make the ytmdl folder
        os.makedirs(DEFAULTS().SONG_TEMP_DIR)


    # Now write the config text to config file
    with open(config_path, 'w') as write_config:
        write_config.write(config_text)


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


def checkExistence(keyword, value):
    """Check if the user specified value in config is possible."""
    if keyword == 'SONG_DIR':
        # In this case check if $ and -> are present
        # If they are then only check if the base dir exists
        if '$' in value:
            pos = value.find('$')
            value = value[:pos]

        if os.path.isdir(value):
            return True
        else:
            return False
    elif keyword == 'QUALITY':
        # Possible values that QUALITY can take
        possQ = ['320', '192']

        if value in possQ:
            return True
        else:
            return False


def retDefault(keyword):
    """Return the DEFAULT value of keyword."""
    if keyword == 'QUALITY':
        return DEFAULTS().SONG_QUALITY
    elif keyword == 'SONG_DIR':
        return DEFAULTS().SONG_DIR


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
                # Check if the line has a \n in it
                if "\n" in line:
                    newDEFAULT = newDEFAULT.replace('\n', '')

                if checkExistence(keyword, newDEFAULT):
                    return newDEFAULT
                else:
                    logger.warning("{}: doesn't exist.")
                    return retDefault(keyword)


if __name__ == '__main__':
    make_config()
    exit(0)
