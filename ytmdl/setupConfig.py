"""Functions used in setting up the config file are defined here."""

import os

config_text = '#*****************************************#\n\
#*-------------config for ytmdl ----------#\n\
#\n\
#-----------------------------------------#\n\
#------PLEASE DONT LEAVE ANY BLANK LINE---#\n\
#-----------------------------------------#\n\
#\n\
# To change defaults just remove the hash(#)\n\
# from thw beginning of the line.\n\
# The will be read as a single line comment.\n\
#\n\
#*****************************************\n\
# The SONG_DIR is the directory where all the songs will be saved.\n\
# In order to change it, simply remove the hash from beginning\n\
# And change the path to your desired one.\n\
# In case the path has spaces in in, include it in a " "\n\
# Following is a simple folder path example\n\
#\n\
#SONG_DIR = "path/to/your/desired/folder"\n\
#\n\
#************--------ADVANCED-------*********\n\
# If you want to save the song in custom folders than those can be\n\
# added to the name like the following example.\n\
# The possible values are following\n\
#\n\
# Artist --> Song Artist\n\
# Album  --> Song Album Name\n\
# Title  --> Song Name\n\
# Genre  --> Song Genre\n\
# TrackNumber --> Song Number in the album\n\
# ReleaseDate --> Song Release date\n\
#\n\
# Following is an example of the format\n\
#SONG_DIR = "/home/deepjyoti30/Music$Artist->Album->Title"\n\
#\n\
#*****************************************#\n\
# The QUALITY is the quality of the song in kbps\n\
# By default it is set to 320kbps\n\
# In case you want to change it to something else,\n\
# Uncomment the following line and change it\n\
#\n\
# Supported values are 320 and 192\n\
#\n\
#QUALITY = "320"\n\
#'


class DEFAULTS:
    """Some default stuff defined."""

    # The home dir
    HOME_DIR = os.path.expanduser('~')

    # The default song dir
    SONG_DIR = os.path.join(HOME_DIR, 'Music')

    # The temp dir
    SONG_TEMP_DIR = os.path.join(SONG_DIR, 'ytmdl')

    # The default song quality
    SONG_QUALITY = '320'

    # The config path
    CONFIG_PATH = os.path.join(HOME_DIR, '.config', 'ytmdl')


def make_config():
    """Copy the config file to .config folder."""
    # Remove the current config from SONG_TEMP_DIR
    config_path = os.path.join(DEFAULTS.CONFIG_PATH, 'config')

    # Check if the ytmdl folder is present in config
    if not os.path.isdir(DEFAULTS.CONFIG_PATH):
        # Make the ytmdl folder
        os.makedirs(DEFAULTS.CONFIG_PATH)
    elif os.path.isfile(config_path):
        os.remove(config_path)

    # Now write the config test to config file
    with open(config_path, 'w') as write_config:
        write_config.write(config_text)


def checkConfig():
    """Need to check the config to see if defaults are changed.

    The config will be saved in the .config folder.
    """
    # Try to see if the config is present in the SONG_TEMP_DIR

    if os.path.isdir(DEFAULTS.CONFIG_PATH):
        DIR_CONTENTS = os.listdir(DEFAULTS.CONFIG_PATH)
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
        # In this case check if $ and -> are presnt
        # If they are then only check if the base dir exists
        if '$' in value and '->' in value:
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
        return DEFAULTS.SONG_QUALITY
    elif keyword == 'SONG_DIR':
        return DEFAULTS.SONG_DIR


def GIVE_DEFAULT(self, keyword):
    """Check if the user has uncommented the config and added something.

    If possible get what is changed, else return the default value.
    """
    # Check If the config is already present in SONG_TEMP_DIR
    if not checkConfig():
        return retDefault(keyword)
    else:
        # Then read from it
        READ_STREAM = open(os.path.join(DEFAULTS.CONFIG_PATH, 'config'), 'r')

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
                    return retDefault(keyword)


if __name__ == '__main__':
    make_config()
    exit(0)
