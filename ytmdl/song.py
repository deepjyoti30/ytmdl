"""song.py - Used for song related functions.

All the functions used to interact with the downloaded song are defined here.
"""

from colorama import Fore, Style
from mutagen.id3 import (
    ID3,
    APIC,
    TIT2,
    TPE1,
    TALB,
    TCON,
    TRCK,
    TYER,
    PictureType
)
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover
from mutagen import File
from mutagen.flac import Picture
from base64 import b64encode
import requests
import os
from rich.prompt import IntPrompt

from ytmdl import prepend, defaults
from simber import Logger
from ytmdl.meta import preconfig
from ytmdl.dir import __replace_special_characters
# import traceback

logger = Logger("song")

# ----------------------cover--------------------


def dwCover(song):
    """Download the song cover img from itunes."""
    # Try to download the cover art as cover.jpg in temp
    logger.info("Preparing the album cover")
    try:
        imgURL = song.artwork_url_100

        # Check if the passed imgURL is a local file
        # this is possible if the metadata was entered manually.
        imgURL = os.path.expanduser(imgURL)
        if os.path.exists(imgURL):
            # Probably a file, read it in binary and extract the data
            # then return.
            content = open(imgURL, "rb").read()
            with open(defaults.DEFAULT.COVER_IMG, 'wb') as f:
                f.write(content)
            return True

        # Else might be an URL
        try:
            # Try to get 512 cover art
            imgURL = imgURL.replace('100x100', '2048x2048')
        except Exception:
            pass

        r = requests.get(imgURL)

        with open(defaults.DEFAULT.COVER_IMG, 'wb') as f:
            f.write(r.content)

        return True
    except TimeoutError:
        prepend.PREPEND(2)
        print('Could not get album cover. Are you connected to internet?\a')
        return False
    except Exception as e:
        logger.warning(
            "Error while trying to download image, skipping!: {}".format(e))
        return False
    else:
        return False

# -----------------------tag----------------------


def print_choice(beg, end, SONG_INFO, type):
    """Print the available choices."""
    # Check if end is more than length of SONG_INFO
    if end > len(SONG_INFO):
        end = len(SONG_INFO)

    while beg != end:
        print(Fore.LIGHTMAGENTA_EX, end='')
        print(' [' + str(beg+1) + '] ', end='')
        print(Style.RESET_ALL, end='')
        print(Fore.LIGHTCYAN_EX, end='')
        if type == 'metadata':
            print(SONG_INFO[beg].track_name, end='')
        if type == 'mp3':
            print('[M] ' if SONG_INFO[beg]['verified_music'] else '', end='')
            print(SONG_INFO[beg]['title'], end='')
        print(Style.RESET_ALL, end='')
        print(' by ', end='')
        print(Fore.YELLOW, end='')
        if type == 'metadata':
            print(SONG_INFO[beg].artist_name, end='')
        if type == 'mp3':
            print(SONG_INFO[beg]['author_name'], end='')
            print(Style.RESET_ALL, end='')
            print(' with dur ', end='')
            print(Fore.GREEN, end='')
            print("{}".format(SONG_INFO[beg]['duration']), end='')
        print(Style.RESET_ALL)

        beg += 1

    # Before exiting print another choice to show more
    if end < len(SONG_INFO):
        print(Fore.LIGHTMAGENTA_EX, end='')
        print(' [0]', end='')
        print(Style.RESET_ALL, end='')
        print(Fore.YELLOW, end='')
        print(' More results')
        print(Style.RESET_ALL, end='')


def get_default(songs, type="mp3") -> int:
    """Get the default song that will be selected if the user
    doesn't select a value.
    """
    # If the user is asked to select metadata, then just return
    # 1
    if type != "mp3":
        return 1

    # Else, we need to find the first verified music video present.
    choice = 1

    for index in range(0, len(songs)):
        if songs[index]['verified_music']:
            choice = index + 1
            break

    return choice


def getChoice(SONG_INFO, type):
    """If more than 1 result from getData then ask for a choice."""
    # Print 5 of the search results
    # In case less, print all

    logger.info('Choose One {}'.format(
        '(One with [M] is verified music)'
        if type == 'mp3' else '(Enter -1 to skip metadata or -2 to amend search)'))

    results = len(SONG_INFO)

    if results > 5:
        results = 5

    PRINT_WHOLE = True

    default_choice = get_default(SONG_INFO, type)

    beg = 0
    while True:
        # Print the results first
        if PRINT_WHOLE:
            print_choice(beg, results, SONG_INFO, type)
        prepend.PREPEND(1)
        choice = IntPrompt.ask('Enter Choice', default=default_choice)

        logger.debug(choice)
        choice = int(choice)

        # If the choice is 0 then try to print more results
        # The choice is valid if it is in the range and it is greater than 0
        # We also need to break when the user enters -1 which means the exec
        # will skip the current song or -2 which means the exec will amend the
        # search and retry
        if choice == -1 or choice == -2 or (choice <= len(SONG_INFO) and choice > 0):
            break
        elif choice == 0 and results < len(SONG_INFO):
            PRINT_WHOLE = True
            beg = results
            results = beg + 5
        else:
            PRINT_WHOLE = False

    return choice - 1 if (choice != -1 and choice != -2) else choice


def set_MP3_data(song, song_path):
    """
    Set the meta data if the passed data is mp3.
    """
    # A variable to see if cover image was added.
    IS_IMG_ADDED = False

    try:
        SONG_PATH = os.path.join(defaults.DEFAULT.SONG_TEMP_DIR,
                                 song_path)

        audio = MP3(SONG_PATH, ID3=ID3)
        data = ID3(SONG_PATH)

        # Download the cover image, if failed, pass
        if dwCover(song):
            imagedata = open(defaults.DEFAULT.COVER_IMG, 'rb').read()
            data.add(APIC(3, 'image/jpeg', 3, 'Front cover', imagedata))
            # REmove the image
            os.remove(defaults.DEFAULT.COVER_IMG)
            IS_IMG_ADDED = True

        # If tags are not present then add them
        try:
            audio.add_tags()
        except Exception:
            pass

        audio.save()

        logger.debug("Passed song release date: ", song.release_date)

        data.add(TYER(encoding=3, text=song.release_date))
        data.add(TIT2(encoding=3, text=song.track_name))
        data.add(TPE1(encoding=3, text=song.artist_name))
        data.add(TALB(encoding=3, text=song.collection_name))
        data.add(TCON(encoding=3, text=song.primary_genre_name))
        data.add(TRCK(encoding=3, text=str(song.track_number)))

        data.save()

        defaults.DEFAULT.SONG_NAME_TO_SAVE = __replace_special_characters(
            song.track_name) + '.mp3'

        # Rename the downloaded file
        to_save_as = os.path.join(
            defaults.DEFAULT.SONG_TEMP_DIR,
            defaults.DEFAULT.SONG_NAME_TO_SAVE
        )
        logger.debug("Renaming file from: `{}` to `{}`".format(
            SONG_PATH, to_save_as))
        os.rename(SONG_PATH, to_save_as)

        return IS_IMG_ADDED

    except Exception as e:
        logger.debug("{}".format(e))
        return e, False


def set_M4A_data(song, song_path):
    """
    Set the tags in the m4a file passed.
    """
    cover_added = False

    try:
        SONG_PATH = os.path.join(defaults.DEFAULT.SONG_TEMP_DIR,
                                 song_path)
        audio = MP4(SONG_PATH)

        # Download the cover image, if failed, pass
        if dwCover(song):
            imagedata = open(defaults.DEFAULT.COVER_IMG, 'rb').read()
            audio["covr"] = [MP4Cover(
                imagedata,
                imageformat=MP4Cover.FORMAT_JPEG
            )]
            # REmove the image
            os.remove(defaults.DEFAULT.COVER_IMG)
            cover_added = True

        # If tags are not present then add them
        try:
            audio.add_tags()
        except Exception:
            pass

        audio.save()

        # Add the meta data, the key's can be found at
        # https://mutagen.readthedocs.io/en/latest/api/mp4.html#mutagen.mp4.MP4Tags
        audio["\xa9nam"] = song.track_name
        audio["\xa9alb"] = song.collection_name
        audio["\xa9ART"] = song.artist_name
        audio["\xa9day"] = song.release_date
        audio["\xa9gen"] = song.primary_genre_name

        # NOTE: In m4a files, the track number is of the following format
        # track number / track count
        # However, we don't have track count for all songs, so
        # we'll have to find a fallback for that.
        track_count = song.track_count if hasattr(song, 'track_count') else "1"
        logger.debug("Adding track count")
        logger.debug(f"Count: {track_count}")
        audio["trkn"] = [(int(song.track_number), int(track_count))]

        audio.save()

        defaults.DEFAULT.SONG_NAME_TO_SAVE = song.track_name + '.m4a'

        # Rename the downloaded file
        os.rename(SONG_PATH, os.path.join(
            defaults.DEFAULT.SONG_TEMP_DIR,
            defaults.DEFAULT.SONG_NAME_TO_SAVE
        ))

        return cover_added

    except Exception as e:
        return e


def set_OPUS_data(song, song_path):
    """
    Set the data into an OPUS container according to the
    passed data.
    """
    COVER_ADDED = False

    try:
        SONG_PATH = os.path.join(defaults.DEFAULT.SONG_TEMP_DIR,
                                 song_path)
        logger.debug("Opening file at {} to add metadata".format(SONG_PATH))
        mutagen_file = File(SONG_PATH)

        # Try adding the tags container
        try:
            mutagen_file.add_tags()
        except Exception as e:
            # If exception is thrown, the tags already exist
            logger.debug(
                "Got exception while adding tags to the passed file: ", str(e))
            pass

        # Clear out the tags from the file
        mutagen_file.clear()

        # Try adding the cover
        if dwCover(song):
            imagedata = open(defaults.DEFAULT.COVER_IMG, 'rb').read()
            picture = Picture()
            picture.data = imagedata
            picture.type = PictureType.COVER_FRONT
            picture.mime = "image/jpeg"
            encoded_data = b64encode(picture.write())
            mutagen_file["metadata_block_picture"] = encoded_data.decode(
                "ascii")

            # Remove the image
            os.remove(defaults.DEFAULT.COVER_IMG)
            COVER_ADDED = True

        # Add the tags now
        # Refer to https://www.programcreek.com/python/example/63675/mutagen.File
        # for more information on it
        mutagen_file["Title"] = song.track_name
        mutagen_file["Album"] = song.collection_name
        mutagen_file["Artist"] = song.artist_name
        mutagen_file["Date"] = song.release_date
        mutagen_file["Genre"] = song.primary_genre_name

        mutagen_file.save()

        defaults.DEFAULT.SONG_NAME_TO_SAVE = song.track_name + '.opus'

        # Rename the downloaded file
        os.rename(SONG_PATH, os.path.join(
            defaults.DEFAULT.SONG_TEMP_DIR,
            defaults.DEFAULT.SONG_NAME_TO_SAVE
        ))

        return COVER_ADDED
    except Exception as e:
        return e


def _get_option(SONG_INFO, is_quiet, choice):
    option = 0
    if len(SONG_INFO) > 1:
        if not is_quiet:
            option = getChoice(SONG_INFO, 'metadata')
        elif choice is not None and choice in range(1, len(SONG_INFO)):
            option = choice
    return int(option)


def setData(SONG_INFO, is_quiet, song_path, datatype='mp3', choice=None):
    """Add the metadata to the song."""

    # Some providers need extra daa from other endpoints,
    # this is where we define which need it and where to get
    # it from

    logger.debug(choice)
    option = _get_option(SONG_INFO, is_quiet, choice)
    logger.debug(option)

    # If -1 or -2 then skip setting the metadata
    if option == -1 or option == -2:
        return option

    song = SONG_INFO[option]

    get_more_data_dict = preconfig.CONFIG().GET_EXTRA_DATA

    # Try to check if the song object has an attribute provider
    # Deezer has it but other objects don't have it.
    # If the provider is present then fetch extra data accordingly

    if hasattr(song, 'provider') and song.provider in get_more_data_dict:
        song = get_more_data_dict.get(song.provider, lambda _: None)(song)

    if datatype == 'mp3':
        img_added = set_MP3_data(
            song,
            song_path,
        )
    elif datatype == 'm4a':
        img_added = set_M4A_data(
            song,
            song_path,
        )
    elif datatype == 'opus':
        img_added = set_OPUS_data(
            song,
            song_path
        )

    # Handle exception while adding the metadata
    if type(img_added) == Exception:
        logger.error(
            "Failed to add metadata due to exception: {}".format(img_added))

    # Show the written stuff in a better format
    prepend.PREPEND(1)
    print('================================')
    print('  || YEAR: ' + song.release_date)
    print('  || TITLE: ' + song.track_name)
    print('  || ARTIST: ' + song.artist_name)
    print('  || ALBUM: ' + song.collection_name)
    print('  || GENRE: ' + song.primary_genre_name)
    print('  || TRACK NO: ' + str(song.track_number))

    if img_added:
        print('  || ALBUM COVER ADDED')

    prepend.PREPEND(1)
    print('================================')

    return option
