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
from ytmdl import (dir, song, yt, defaults, prepend, setupConfig, cache, utility,
                   metadata)

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
    parser.add_argument('--artist', help="Name of the artist")
    parser.add_argument('--album', help="Name of the album.")
    parser.add_argument('--version', action='version', version='2019.10.8',
                        help='show the program version number and exit')
    parser.add_argument('--url',
                        help="Youtube song link.")
    parser.add_argument('--better-search', help="Better search is addition of\
                        passed artist and album keyword to the youtube search\
                        in order to get a more accurate result. (Default: true)",
                        type=bool, default=True)
    parser.add_argument('-s', '--setup',
                        help='Setup the config file',
                        action='store_true')
    parser.add_argument('-l', '--list', help="Download list of songs.\
                        The list should have one song name in every line.",
                        default=None)
    parser.add_argument('--nolocal',
                        help='Dont search locally for the song before\
                        downloading.',
                        action='store_true')

    args = parser.parse_args()

    return args


def main(args):
    """Run on program call."""
    # args = arguments()
    song_name = args.SONG_NAME

    # Check if --setup is passed
    if args.setup:
        setupConfig.make_config()
        exit(0)

    # After this part song name is required
    if song_name is None:
        prepend.PREPEND(2)
        print("Please pass a song name. This is necessary",
              "to search metadata.")
        exit(1)

    if not args.nolocal:
        # Search for the song locally
        if not cache.main(song_name):
            return 0

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

        data, urls = yt.search(song_name, args.better_search,
                                kw=[args.artist, args.album])
        
        # Handle the exception if urls has len 0
        if len(urls) == 0:
            prepend.PREPEND(2)
            print("No song found. Please try again with a different keyword.")
            print(Style.RESET_ALL, end='')
            exit()

        if len(data) > 1 and not is_quiet:
            # Ask for a choice
            choice = song.getChoice(data, 'mp3')
        else:
            choice = 0

        link = 'https://youtube.com{}'.format(urls[int(choice)])

    # Declare a var to store the name of the yt video
    yt_title = data[choice]['title']

    prepend.PREPEND(1)
    print('Downloading ', end='')
    print(Fore.LIGHTMAGENTA_EX, end='')
    print(yt_title, end=' ')
    print(Style.RESET_ALL, end='')
    print('in', end=' ')
    print(Fore.LIGHTYELLOW_EX, end='')
    print(defaults.DEFAULT.SONG_QUALITY + 'kbps', end='')
    print(Style.RESET_ALL)
    path = yt.dw(link, yt_title)

    if not path:
        prepend.PREPEND(2)
        print('Something went wrong while downloading!\a')
        sys.exit(0)
    else:
        prepend.PREPEND(1)
        print('Downloaded!')

    prepend.PREPEND(1)
    print('Converting to mp3...')

    conv_name = utility.convert_to_mp3(path)

    if not conv_name:
        prepend.PREPEND(2)
        print('Something went wrong while converting!\a')
        exit(-1)

    prepend.PREPEND(1)
    print('Getting song data...')

    # TRACK_INFO = song.getData(song_name)
    TRACK_INFO = metadata.SEARCH_SONG(song_name, filters=[args.artist, args.album])

    # declare a variable to store the option
    option = 0

    if TRACK_INFO is False:
        # prepend.PREPEND(2)
        # print('Data \a')
        # exit(0)
        pass
    elif len(TRACK_INFO) == 0:
        prepend.PREPEND(2)
        print('No data was found!\a')
        sys.exit(0)
    else:
        prepend.PREPEND(1)
        print('Setting data...')

        option = song.setData(TRACK_INFO, is_quiet, conv_name)

        if type(option) is not int:
            prepend.PREPEND(2)
            print('Something went wrong while writing data!\a')
            sys.exit(0)

    # Get the directory where song is moved

    DIR = dir.cleanup(TRACK_INFO, option)
    prepend.PREPEND(1)
    print('Moving to {}...'.format(DIR))

    if not DIR:
        prepend.PREPEND(2)
        print('Something went wrong while moving!\a')
        sys.exit(0)
    else:
        prepend.PREPEND(1)
        print('Done')


def extract_data():
    """Extract the arguments and act accordingly."""
    args = arguments()

    if args.list is not None:
        songs = utility.get_songs(args.list)
        if len(songs) != 0:
            prepend.PREPEND(1)
            print("Downloading songs in {}".format(args.list))
            for song_name in songs:
                args.SONG_NAME = song_name
                main(args)
        else:
            prepend.PREPEND(2)
            print("{}: is empty".format(args.list))
    else:
        main(args)


if __name__ == '__main__':
    extract_data()
