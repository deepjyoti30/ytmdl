"""All directory handling definitions."""

import os
import glob
import shutil
from ytmdl import defaults


def cleanup(TRACK_INFO, index):
    """Move the song from temp to $HOME/Music dir."""
    try:
        SONG = glob.glob(os.path.join(defaults.DEFAULT.SONG_TEMP_DIR, '*mp3'))
        SONG = SONG[0]

        SONG_NAME = os.path.basename(SONG)

        DIR = defaults.DEFAULT.SONG_DIR

        # Check if DIR has $ in its path
        # If it does then make those folders accordingly

        if '$' in DIR and '->' in DIR:
            DIR = make_custom_dir(DIR, TRACK_INFO[index])
        shutil.move(SONG, os.path.join(DIR, SONG_NAME))

        return DIR
    except Exception:
        return False


def ret_proper_names(ordered_names):
    """Return a list with the names changed to itunespy supported ones.

    For eg: Artist to artist_name
    """
    itunespy_dict = {'Artist': 'artist_name',
                     'Title': 'track_name',
                     'Album': 'collection_name',
                     'Genre': 'primary_genre_name',
                     'TrackNumber': 'track_number',
                     'ReleaseDate': 'release_date'
                     }

    new_names = []
    for names in ordered_names:
        new_names.append(itunespy_dict[names])

    return new_names


def seperate_kw(uns_kw):
    """Seperate the keywords and return a list."""
    sep_kw = []

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

    order_dir = ret_proper_names(order_dir)

    # Convert the TRACK_INFO namespace to a dictionary
    TRACK_INFO = vars(TRACK_INFO)

    for kw_name in order_dir:
        dir_name = TRACK_INFO[kw_name]
        new_dir = os.path.join(base_DIR, dir_name)

        # Make the dir only if it doesn't already exist
        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)

        # Now make the new_dir base_DIR
        base_DIR = new_dir

    return base_DIR
