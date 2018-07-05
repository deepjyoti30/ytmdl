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


# Possible values that QUALITY can take
possibleQualities = ['320', '192']


def checkConfig():
    """Need to check the config to see if defaults are changed.

    The config will be saved in the ytmdl directory in Music.
    """
    # Try to see if the config is present in the SONG_TEMP_DIR

    DIR_CONTENTS = os.listdir(DEFAULTS.SONG_TEMP_DIR)

    if 'config' not in DIR_CONTENTS:
        # Copy the config file from the current dir to SONG_TEMP_DIR
        try:
            src = os.path.join(os.getcwd(), 'config')
            dst = os.path.join(DEFAULTS.SONG_TEMP_DIR, 'config')

            shutil.copy(src, dst)

            return True
        except:
            return False
    else:
        return True


def checkExistence(keyword, value):
    """Check if the user specified value in config is possible."""
    if keyword == 'SONG_DIR':
        if os.path.isdir(value):
            return True
        else:
            return False
    elif keyword == 'QUALITY':
        if value in possibleQualities:
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
                # Remove all the spaces
                line = line.replace(' ', '')
                # Remove the "
                line = line.replace('"', '')
                newDEFAULT = line[line.index('=') + 1:]
                # Before returning check the value
                if checkExistence(keyword, newDEFAULT):
                    return newDEFAULT
                else:
                    return retDefault(keyword)
