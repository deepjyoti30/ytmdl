#!/usr/bin/env python3
"""Module for caching songs.

    Nishan Pantha(c) 2017-18
    NISH1001@github.com
"""

import glob
import os
from ytmdl.stringutils import (
    remove_multiple_spaces, remove_punct, compute_jaccard, remove_stopwords,
    check_keywords
)
from ytmdl.defaults import DEFAULT
from ytmdl.prepend import PREPEND
from colorama import Fore, Style


class Cache:
    """The main caching component."""

    def __init__(self, directory=None):
        """Init the stuff."""
        if directory is None:
            directory = DEFAULT.SONG_DIR
            # Check the dir only if special characters are present
            if '$' in directory:
                directory = os.path.dirname(directory)
        directory = os.path.expanduser(directory)
        self.directory = directory

    def list_mp3(self):
        """Get the list of all the mp3 files in the cache."""
        os.chdir(self.directory)
        return glob.glob("*.mp3")

    def search_exactly(self, song_name):
        """Search the song in the cache.

        Tries to match the song name exactly.
        """
        print("Searching the song : {} in the cache...".format(song_name))
        song_name = song_name.lower()
        cached_songs = self.list_mp3()
        for song in cached_songs:
            if song.lower() == song_name:
                return song
        return None

    def get_full_location(self, song_name):
        """Return full location of the song."""
        return self.directory + "/" + song_name

    def search(self, song_name):
        return self._search_tokens(song_name)

    def _search_tokens(self, song_name):
        """Search song in the cache based on simple each word matching."""
        song_name = remove_stopwords(remove_multiple_spaces(song_name).lower())
        tokens1 = song_name.split()
        cached_songs = self.list_mp3()

        res = []
        for song in cached_songs:
            name = os.path.splitext(song)[0].lower()
            title = name
            name = remove_punct(name)
            name = remove_multiple_spaces(name)
            tokens2 = name.split()
            match = check_keywords(tokens1, tokens2)
            if match:
                dist = compute_jaccard(tokens1, tokens2)
                res.append((song_name, song, title, dist))
        res = sorted(res, key=lambda x: x[-1], reverse=True)
        if res and res[0][-1] > 0:
            return res[0][2], self.get_full_location(res[0][1])
        else:
            return None


def main(SONG_NAME=''):
    """Run on program call."""
    cache = Cache("~/Music")
    match = cache.search(SONG_NAME)
    if match is not None:
        PREPEND(1)
        print(Fore.MAGENTA, end='')
        print('{} '.format(match[0]), end='')
        print(Style.RESET_ALL, end='')
        print('found.')
        while True:
            choice = input('Do you still want to continue[y/n]')
            choice = choice.lower()
            if choice == 'y' or choice == 'Y':
                return True
            elif choice == 'n' or choice == 'N':
                return False
    else:
        return True


if __name__ == "__main__":
    main()
