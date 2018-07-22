"""song.py - Used for song related functions.

All the functions used to interact with the downloaded song are defined here.
"""

from colorama import Fore, Style
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TCON, TRCK, TYER
from mutagen.mp3 import MP3
import requests
import itunespy
from ytmdl import prepend, defaults
import glob
import os

# ----------------------cover--------------------


def dwCover(SONG_INFO, index):
    """Download the song cover img from itunes."""
    # Try to download the cover art as cover.jpg in temp
    try:
        imgURL = SONG_INFO[index].artwork_url_100
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
    else:
        return False

# -----------------------tag----------------------


def getData(SONG_NAME):
    """Try to download the metadata using itunespy."""
    # Try to get the song data from itunes
    try:
        SONG_INFO = itunespy.search_track(SONG_NAME)
        return SONG_INFO
    except LookupError:
        prepend.PREPEND(2)
        print('Song not found!')
        return False
    except TimeoutError:
        prepend.PREPEND(2)
        print('Search timed out. Are you connected to internet?\a')
        return False
    else:
        prepend.PREPEND(2)
        print('Unknown Error!\a')
        return False


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
            print(SONG_INFO[beg]['title'], end='')
        print(Style.RESET_ALL, end='')
        print(' by ', end='')
        print(Fore.YELLOW, end='')
        if type == 'metadata':
            print(SONG_INFO[beg].artist_name, end='')
        if type == 'mp3':
            print(SONG_INFO[beg]['author_name'], end='')
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


def getChoice(SONG_INFO, type):
    """If more than 1 result from getData then ask for a choice."""
    # Print 5 of the search results
    # In case less, print all

    prepend.PREPEND(1)
    print('Choose One')

    results = len(SONG_INFO)

    if results > 5:
        results = 5

    PRINT_WHOLE = True

    beg = 0
    while True:
        # Print the results first
        if PRINT_WHOLE:
            print_choice(beg, results, SONG_INFO, type)
        prepend.PREPEND(1)
        choice = input('Enter Choice [a valid choice] ')
        choice = int(choice)
        # If the choice is 6 then try to print more results
        if choice <= results and choice > 0:
            break
        elif choice == 0:
            PRINT_WHOLE = True
            beg = results
            results = beg + 5
        else:
            PRINT_WHOLE = False

    choice = int(choice)
    choice -= 1
    return choice


def setData(SONG_INFO, is_quiet):
    """Add the metadata to the song."""
    # A variable to see if cover image was added.
    IS_IMG_ADDED = False

    try:
        # If more than one choice then call getChoice
        if len(SONG_INFO) > 1 and not is_quiet:
            option = getChoice(SONG_INFO, 'metadata')
        else:
            option = 0

        SONG_PATH = os.path.join(defaults.DEFAULT.SONG_TEMP_DIR,
                                 'ytmdl_temp.mp3_new.mp3')

        audio = MP3(SONG_PATH, ID3=ID3)
        data = ID3(SONG_PATH)

        # Download the cover image, if failed, pass
        if dwCover(SONG_INFO, option):
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

        option = int(option)

        data.add(TYER(encoding=3, text=SONG_INFO[option].release_date))
        data.add(TIT2(encoding=3, text=SONG_INFO[option].track_name))
        data.add(TPE1(encoding=3, text=SONG_INFO[option].artist_name))
        data.add(TALB(encoding=3, text=SONG_INFO[option].collection_name))
        data.add(TCON(encoding=3, text=SONG_INFO[option].primary_genre_name))
        data.add(TRCK(encoding=3, text=str(SONG_INFO[option].track_number)))

        data.save()

        defaults.DEFAULT.SONG_NAME_TO_SAVE = SONG_INFO[option].track_name + '.mp3'

        # Rename the downloaded file
        os.rename(SONG_PATH, os.path.join(defaults.DEFAULT.SONG_TEMP_DIR,
                                             defaults.DEFAULT.SONG_NAME_TO_SAVE))

        # Show the written stuff in a better format
        prepend.PREPEND(1)
        print('================================')
        print('  || YEAR: ' + SONG_INFO[option].release_date)
        print('  || TITLE: ' + SONG_INFO[option].track_name)
        print('  || ARITST: ' + SONG_INFO[option].artist_name)
        print('  || ALBUM: ' + SONG_INFO[option].collection_name)
        print('  || GENRE: ' + SONG_INFO[option].primary_genre_name)
        print('  || TRACK NO: ' + str(SONG_INFO[option].track_number))

        if IS_IMG_ADDED:
            print('  || ALBUM COVER ADDED')

        prepend.PREPEND(1)
        print('================================')

        return option
    except Exception:
        return False
