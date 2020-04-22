"""Some definitions to interact with the command line."""

import subprocess
from os import remove, path, popen
from ytmdl import defaults
from shutil import which
import ffmpeg


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


def get_terminal_length():
    """Return the length of the terminal."""
    rows, cols = popen('stty size', 'r').read().split()

    return int(cols)


def convert_to_mp3r(path):
    """Convert the file to mp3 using ffmpeg."""
    try:
        new_name = path + '_new.mp3'

        command = "ffmpeg -loglevel panic -i {} -vn -ar 44100 -ac 2 -ab {}k -f mp3 {}".format(path,
                                                                                             defaults.DEFAULT.SONG_QUALITY,
                                                                                              new_name)
        output, error = exe(command)

        # Delete the temp file now
        remove(path)
        return new_name
    except Exception as e:
        return e


def convert_to_mp3(path):
    """Covert to mp3 using the python ffmpeg module."""
    new_name = path + '_new.mp3'
    ffmpeg.input(path).output(
                        new_name,
                        loglevel='panic',
                        ar=44100,
                        ac=2,
                        ab='{}k'.format(defaults.DEFAULT.SONG_QUALITY),
                        f='mp3'
                    ).run()
    # Delete the temp file now
    remove(path)
    return new_name


def is_valid(dir_path):
    """Check if passed path is valid or not."""
    if not path.isfile(dir_path):
        return False
    else:
        return True


def get_songs(file_path):
    """Extract the songs from the provided list."""

    if is_valid(file_path):
        RSTREAM = open(file_path, 'r')

        song_tup = RSTREAM.read().split("\n")

        return song_tup
    else:
        return []


def is_present(app):
    """Check if the passed app is installed in the machine."""
    return which(app) is not None