"""Some definitions to interact with the command line."""

import subprocess
from os import remove
from ytmdl import defaults


def exe(command):
    """Execute the command externally.

    Written by Nishan Pantha.
    """
    command = command.strip()
    c = command.split()
    output, error = subprocess.Popen(c,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE).communicate()
    output = output.decode('utf-8').strip()
    error = error.decode('utf-8').strip()
    return (output, error)


def convert_to_mp3(path):
    """Convert the file to mp3 using ffmpeg."""
    new_name = path + '_new.mp3'
    command = "ffmpeg -loglevel panic -i {} -vn -ar 44100 -ac 2 -ab {}k -f mp3 {}".format(path,
                                                                                         defaults.DEFAULT.SONG_QUALITY,
                                                                                          new_name)
    output, error = exe(command)

    # Delete the temp file now
    remove(path)
    return True
