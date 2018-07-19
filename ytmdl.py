#!/usr/bin/env python3
"""
    * ytmdl.py - A script to download songs.

----------------------------------------------------
     A simple script to download songs in mp3 format
     from Youtube.
     Users pass the song name as arguement.
----------------------------------------------------
    --> Deepjyoti Barman
    --> deepjyoti30@github.com
"""

from __future__ import unicode_literals
import sys
from colorama import init
from colorama import Fore, Style
import argparse
from ytmdl import dir, song, yt, defaults, prepend, setupConfig, cache

# init colorama for windows
init()


def arguments():
    """Parse the arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument('SONG_NAME', help="Name of the song to download.",
                        default=None, nargs='?', type=str)
    parser.add_argument('-q', '--quiet',
                        help="Don't ask the user to select songs\
                        if more than one search result.\
                        The first result in each case will be considered.",
                        action='store_true')
    parser.add_argument('--version', action='version', version='v0.1-r9',
                        help='show the program version number and exit')
    parser.add_argument('--url',
                        help="Youtube song link.")
    parser.add_argument('-s', '--setup',
                        help='Setup the config file',
                        action='store_true')
    parser.add_argument('--nolocal',
                        help='Dont search locally for the song before\
                        downloading.',
                        action='store_true')

    args = parser.parse_args()

    return args


def main():
    """Run on program call."""
    args = arguments()
    song_name = args.SONG_NAME

    # Check if --setup is passed
    if args.setup:
        setupConfig.make_config()
        exit(0)

    # After this part song name is required
    if song_name is None:
        prepend.PREPEND(2)
        print('Please pass a song name.')
        exit(1)

    if not args.nolocal:
        # Search for the song locally
        if not cache.main(song_name):
            exit(0)

    is_quiet = args.quiet
    url = args.url

    # If the url is passed then get the data
    if url is not None:
        data = []
        # Get video data from youtube
        temp_data = yt.scan_video(yt.get_href(url))
        data.append(temp_data)

        # link to dw the song
        link = url

        # In this case choice will be 0
        choice = 0
    else:
        if is_quiet:
            prepend.PREPEND(1)
            print('Quiet is enabled')

        prepend.PREPEND(1)
        print('Searching Youtube for ', end='')
        print(Fore.LIGHTYELLOW_EX, end='')
        print(song_name, end='')
        print(Style.RESET_ALL)

        data, urls = yt.search(song_name)

        if len(data) > 1 and not is_quiet:
            # Ask for a choice
            choice = song.getChoice(data, 'mp3')
        else:
            choice = 0

        link = 'https://youtube.com{}'.format(urls[int(choice)])

    prepend.PREPEND(1)
    print('Downloading ', end='')
    print(Fore.LIGHTMAGENTA_EX, end='')
    print(data[choice]['title'], end=' ')
    print(Style.RESET_ALL, end='')
    print('in', end=' ')
    print(Fore.LIGHTYELLOW_EX, end='')
    print(defaults.DEFAULT.SONG_QUALITY + 'kbps', end='')
    print(Style.RESET_ALL)
    if not yt.GRAB_SONG(link):
        prepend.PREPEND(2)
        print('Something went wrong while downloading!\a')
        sys.exit(0)
    else:
        prepend.PREPEND(1)
        print('Downloaded!')

    prepend.PREPEND(1)
    print('Getting song data...')

    TRACK_INFO = song.getData(song_name)

    if TRACK_INFO is False:
        prepend.PREPEND(2)
        print('Exiting now!\a')
        exit(0)
    elif len(TRACK_INFO) == 0:
        prepend.PREPEND(2)
        print('No data was found!\a')
        sys.exit(0)
    else:
        prepend.PREPEND(1)
        print('Data downloaded!')

    prepend.PREPEND(1)
    print('Setting data...')

    if not song.setData(TRACK_INFO, is_quiet):
        prepend.PREPEND(2)
        print('Something went wrong while writing data!\a')
        sys.exit(0)

    # Get the directory where song is moved

    DIR = dir.cleanup(TRACK_INFO, choice)
    prepend.PREPEND(1)
    print('Moving to {}...'.format(DIR))

    if not DIR:
        prepend.PREPEND(2)
        print('Something went wrong while moving!\a')
        sys.exit(0)
    else:
        prepend.PREPEND(1)
        print('Done')


if __name__ == '__main__':
    main()
