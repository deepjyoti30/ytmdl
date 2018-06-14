import os
from pathlib import Path
import shutil

class DEFAULTS:
    # The home dir
    HOME_DIR = str(Path.home())
    
    # The default song dir
    SONG_DIR = os.path.join(HOME_DIR, 'Music')

    # The temp dir
    SONG_TEMP_DIR = os.path.join(SONG_DIR, 'ytmdl')

def checkConfig():
    # Need to check the config to see if defaults are changed
    # The config will be saved in the ytmdl directory in Music

    # Try to see if the config is present in the SONG_TEMP_DIR

    DIR_CONTENTS = os.listdir(DEFAULTS.SONG_TEMP_DIR)

    if 'config' not in DIR_CONTENTS:
        # Copy the config file from the current dir to SONG_TEMP_DIR
        try:
            src = os.path.join(os.getcwd(),'config')
            dst = os.path.join(DEFAULTS.SONG_TEMP_DIR, 'config')

            shutil.copy(src, dst)

            return True
        except:
            return False
    else:
        return True


class getPATHS:
    def GIVE_SONG_DIR(self):
        # Check If the config is already present in SONG_TEMP_DIR
        if not checkConfig():
            return False
        else:
            # Then read from it
            READ_STREAM = open(os.path.join(DEFAULTS.SONG_TEMP_DIR, 'config'), 'r')

            while True:
                line = READ_STREAM.readline()
                if not line:
                    return DEFAULTS.SONG_DIR
                if line[0] != '#' and 'SONG_DIR' in line:
                    # Remove all the spaces
                    line = line.replace(' ', '')
                    # Remove the "
                    line = line.replace('"', '')
                    newSONG_DIR = line[line.index('=') + 1:]
                    return newSONG_DIR

                