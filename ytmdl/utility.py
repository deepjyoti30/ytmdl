"""Some definitions to interact with the command line."""

import subprocess
from os import remove, path, popen
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


def get_terminal_length():
    """Return the length of the terminal."""
    rows, cols = popen('stty size', 'r').read().split()

    return int(cols)


def convert_to_mp3(path):
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
    except Exception:
        return False


def is_valid(dir_path):
    """Check if passed path is valid or not."""
    if not path.isfile(dir_path):
        return False
    else:
        return True


def get_songs(file_path):
    """Extract the songs from the provided list."""
    song_tup = []

    if is_valid(file_path):
        STREAM = open(file_path, 'r')

        while True:
            line = STREAM.readline()
            if not line:
                break
            # Remove the \n
            line = line.replace('\n', '')
            song_tup.append(line)

    return song_tup
