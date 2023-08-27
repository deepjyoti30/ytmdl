"""All directory handling definitions."""

import os
import glob
import shutil
from html import unescape
from re import sub

from ytmdl import defaults
from simber import Logger

logger = Logger("Dir")


def __replace_special_characters(passed_name: str) -> str:
    """
    In the passed name, replace the special characters like
    / with a `-` so that it does not raise any errors
    related to the OS while moving the file
    """
    # TODO: Also add support for removing backslash
    return sub(r'/', '-', passed_name)


def cleanup(TRACK_INFO, index, datatype, remove_cached=True, filename_passed=None):
    """Move the song from temp to the song dir."""
    try:
        SONG = glob.glob(os.path.join(
            defaults.DEFAULT.SONG_TEMP_DIR,
            '*{}'.format(datatype)
        ))
        SONG = SONG[0]

        SONG_NAME = os.path.basename(SONG)

        # If the filename is passed, use that instead of the song
        #
        # NOTE that is the path is set to be a dynamic value by using
        # special characters like `$` though the config then that will
        # overwrite the filename_passed.
        if filename_passed is not None:
            SONG_NAME = filename_passed + ".{}".format(datatype)

        DIR = defaults.DEFAULT.SONG_DIR
        logger.debug(DIR)

        # Check if DIR has $ in its path
        # If it does then make those folders accordingly

        if '$' in DIR:
            DIR, name = make_custom_dir(DIR, TRACK_INFO[index])

            if name is not None:
                os.rename(SONG, name + '.mp3')
                SONG_NAME = name + '.mp3'
                SONG = SONG_NAME

        dest_filename = os.path.join(
            DIR, __replace_special_characters(SONG_NAME))

        logger.debug("Final name: ", dest_filename)
        shutil.move(SONG, dest_filename)

        if remove_cached:
            _delete_cached_songs(datatype)

        logger.info('Moved to {}...'.format(DIR))
        return True
    except Exception as e:
        logger.critical("Failed while moving with error: {}".format(e))
        return False


def _delete_cached_songs(ext='mp3'):
    """Delete cached songs"""
    # We need to call this after song is moved
    # because otherwise if there is an error along the way
    # next time a wrong song may be copied.
    SONGS_PATH = os.path.join(
        defaults.DEFAULT.SONG_TEMP_DIR,
        '*{}'.format(ext)
    )
    deleted = False
    for song in glob.glob(SONGS_PATH):
        deleted = True
        os.remove(song)
        logger.debug('Removed "{}" from cache'.format(os.path.basename(song)))
    if deleted:
        logger.debug('{}'.format('Deleted cached songs'))


def ret_proper_names(ordered_names):
    """Return a list with the names changed to itunespy supported ones.

    For eg: Artist to artist_name
    """
    info_dict = {'Artist': 'artist_name',
                 'Title': 'track_name',
                 'Album': 'collection_name',
                 'Genre': 'primary_genre_name',
                 'TrackNumber': 'track_number',
                 'ReleaseDate': 'release_date'
                 }

    logger.debug(ordered_names)
    logger.debug(info_dict)

    new_names = []
    for name in ordered_names:
        new_names.append(info_dict.get(name))

    return new_names


def seperate_kw(uns_kw):
    """Separate the keywords and return a list."""
    sep_kw = []

    # Check if -> is present in the name
    if '->' not in uns_kw:
        sep_kw.append(uns_kw)
    else:
        while '->' in uns_kw:
            pos = uns_kw.find("->")
            sep_kw.append(uns_kw[:pos])
            uns_kw = uns_kw[pos + 2:]

        sep_kw.append(uns_kw)
    return sep_kw


def make_custom_dir(DIR, TRACK_INFO):
    """If the dirname has $ in it then we need to make them.

    The DIR is probably in the format of
    keyword->keyword->keyword
    """
    pos = DIR.index('$')

    # base_DIR is where the folders will be made
    base_DIR = DIR[:pos]

    remaining = DIR[pos + 1:]

    order_dir = seperate_kw(remaining)

    # The last element is to be returned and not considered as
    # a folder
    last_element = order_dir[-1]

    # Replace [] from it
    if last_element[0] == '[' and last_element[-1] == ']':

        last_element = last_element.replace('[', '')
        last_element = last_element.replace(']', '')

        order_dir[-1] = last_element

        order_dir = ret_proper_names(order_dir)

        last_element = order_dir[-1]

    else:
        last_element = None
        order_dir = ret_proper_names(order_dir)

    logger.debug(TRACK_INFO)

    if last_element is not None:
        last_element = getattr(TRACK_INFO, last_element)
        order_dir = order_dir[:len(order_dir) - 1]

    for kw_name in order_dir:
        dir_name = unescape(getattr(TRACK_INFO, kw_name))

        # Sometimes, certain strings have / in the name which creates
        # issues since those strings are used to create directories.
        # Whenever there is a /, replace it with -
        # Sometimes strings also contains [\,?,",<>, *] which may cause error
        dir_name = sub('[\\\\?<>/"*]', "-", dir_name)

        new_dir = os.path.join(base_DIR, dir_name)

        # Make the dir only if it doesn't already exist
        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)

        # Now make the new_dir base_DIR
        base_DIR = new_dir

    return (base_DIR, last_element)


def dry_cleanup(current_path, passed_name, filename_passed=None):
    """
    Move the song from the current path to the
    song dir and change the name to the passed_name.

    This is only for when the meta-skip option is passed,
    in which case the song needs to be moved from the cache
    to the user directory.
    """
    try:
        extension = os.path.basename(current_path).split(".")[-1]
        logger.debug("ext: {}".format(extension))

        # If the filename is passed from the CLI, we will use that
        # instead of the passed name.
        if filename_passed is not None:
            passed_name = filename_passed

        new_basename = "{}.{}".format(passed_name, extension)
        DEST = defaults.DEFAULT.SONG_DIR

        # NOTE: If the DEST is a dynamic directory, then we cannot
        # do a dry cleanup. So we'll have to use the base directory
        # instead.
        if "$" in DEST:
            logger.debug(DEST)

            # pylama:ignore=E501
            logger.warning(
                "Destination is a dynamic directory but this is a dry cleanup. Don't pass `--skip-meta` if you don't want this!")

            # Use the base directory
            DEST = DEST[:DEST.find("$")]

            logger.debug(f"Using {DEST} as destination instead")

        logger.debug("Moving to: {}".format(DEST))

        # Create the destination file name
        dest_filename = os.path.join(
            DEST, __replace_special_characters(new_basename))

        shutil.move(current_path, dest_filename)

        logger.info('Moved to {}...'.format(DEST))
        return True
    except Exception as e:
        logger.error("{}".format(e))
        return False
