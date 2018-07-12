"""Functions used in setting up the config file are defined here."""

import os
from pathlib import Path
import shutil


class DEFAULTS:
    """Some default stuff defined."""

    # The home dir
    HOME_DIR = str(Path.home())

    # The default song dir
    SONG_DIR = os.path.join(HOME_DIR, 'Music')

    # The temp dir
    SONG_TEMP_DIR = os.path.join(SONG_DIR, 'ytmdl')

    # The default song quality
    SONG_QUALITY = '320'

    # The config path
    CONFIG_PATH = os.path.join(Path.home(), '.config', 'ytmdl')


def make_config():
    """Copy the config file to .config folder."""
    # Remove the current config from SONG_TEMP_DIR
    config_path = os.path.join(DEFAULTS.CONFIG_PATH, 'config')

    # Check if the ytmdl folder is present in config
    if not os.path.isdir(DEFAULTS.CONFIG_PATH):
        # Make the ytmdl folder
        os.mkdir(DEFAULTS.CONFIG_PATH)
    elif os.path.isfile(config_path):
        os.remove(config_path)

    # Now copy the current one to that
    shutil.copy('config', config_path)


def checkConfig():
    """Need to check the config to see if defaults are changed.

    The config will be saved in the .config folder.
    """
    # Try to see if the config is present in the SONG_TEMP_DIR

    DIR_CONTENTS = os.listdir(DEFAULTS.CONFIG_PATH)

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
        return False
    else:
        # Then read from it
        READ_STREAM = open(os.path.join(DEFAULTS.SONG_TEMP_DIR, 'config'), 'r')

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

                input(newDEFAULT)
                if checkExistence(keyword, newDEFAULT):
                    input(newDEFAULT)
                    return newDEFAULT
                else:
                    return retDefault(keyword)


if __name__ == '__main__':
    make_config()
    exit(0)
