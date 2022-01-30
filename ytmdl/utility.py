"""Some definitions to interact with the command line."""

import subprocess
from os import remove, path, popen
from ytmdl import defaults, prepend
from shutil import which
import ffmpeg
from simber import Logger
from rich.prompt import Confirm, Prompt
from sys import stdout

logger = Logger("Utility")


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


def convert_to_mp3(path, start=None, end=None, cleanup_after_done=True):
    """Covert to mp3 using the python ffmpeg module."""
    new_name = path + '_new.mp3'
    params = {
        "loglevel": "panic",
        "ar": 44100,
        "ac": 2,
        "ab": '{}k'.format(defaults.DEFAULT.SONG_QUALITY),
        "f": "mp3"
    }

    try:
        if start is not None and end is not None:
            params["ss"] = start
            params["to"] = end

        job = ffmpeg.input(path).output(
            new_name,
            **params
        )
        job.run()

        # Delete the temp file now
        if cleanup_after_done:
            remove(path)

        return new_name
    except ffmpeg._run.Error:
        # This error is usually thrown where ffmpeg doesn't have to
        # overwrite a file.
        # The bug is from ffmpeg, I'm just adding this catch to
        # handle that.
        return new_name


def convert_to_opus(path, start=None, end=None, cleanup_after_done=True):
    """Covert to opus using the python ffmpeg module."""
    new_name = path + '_new.opus'
    params = {
        "loglevel": "panic",
        "f": "opus"
    }

    try:
        if start is not None and end is not None:
            params["ss"] = start
            params["to"] = end

        job = ffmpeg.input(path).output(
            new_name,
            **params
        )
        job.run()

        # Delete the temp file now
        if cleanup_after_done:
            remove(path)

        return new_name
    except ffmpeg._run.Error:
        # This error is usually thrown where ffmpeg doesn't have to
        # overwrite a file.
        # The bug is from ffmpeg, I'm just adding this catch to
        # handle that.
        return new_name


def extract_m4a(path, start=None, end=None, cleanup_after_done=True):
    """Extract a m4a file from the given path based on the start
    and end passed.

    This function is to be called internally only for supporting
    songs with chapters as supported by YouTube.
    """
    if not start and not end:
        logger.error("Cannot trim without start and end")

    new_name = path + '_new.m4a'
    try:
        job = ffmpeg.input(path).output(
            new_name, ss=start, to=end, loglevel="panic")
        job.run()

        if cleanup_after_done:
            remove(path)

        return new_name
    except ffmpeg._run.Error as e:
        logger.warning(str(e))
        return new_name


def extract_part_convert(path, format, start, end):
    """Extract part of the file using the path provided and accordingly
    convert to the given format.
    """
    FORMAT_MAP = {
        "mp3": convert_to_mp3,
        "opus": convert_to_opus,
        "m4a": extract_m4a
    }

    # Format will be checked by the main function so no need
    # to check here.
    converted_name = FORMAT_MAP.get(format)(path, start, end, False)
    return converted_name


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


def get_new_title(old_title):
    """
    Ask the user if they would like to go with the old
    title passed as an argument.

    If they say so, it will be returned as it is.

    However, if they want to change the title, get the new
    title and return that one.
    """
    logger.info(
        "Current extracted title for the song is: `{}`".format(old_title)
    )
    logger.info(
        "Most extracted titles are not accurate and they affect the meta search"
    )

    is_change = Confirm.ask("Would you like to change", default=True)

    if not is_change:
        return old_title

    # Else ask for new title
    title = Prompt.ask("Enter new title")
    return title


def get_new_meta_search_by(old_search_by):
    """
    Ask the user to enter a new title to search the metadata with.

    This function will be called when the user explicitly asks for a
    different title to search the metadata with.
    """
    prepend.PREPEND(1)
    new_search_by = Prompt.ask("Enter new title to search metadata with",
                               default=old_search_by)

    if new_search_by == old_search_by:
        logger.info("You can disable this behaviour by removing the"
                    "`--ask-meta-name` flag.")

    return new_search_by


def determine_logger_level() -> int:
    """
    Determine the logger level for stdout stream.
    """
    return [stream for stream in logger.streams if stream.stream_name == stdout.name][0].level


if __name__ == "__main__":
    print(get_new_title("Haha"))
