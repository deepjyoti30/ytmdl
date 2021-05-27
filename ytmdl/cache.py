#!/usr/bin/env python3
"""Module for caching songs.

    Nishan Pantha(c) 2017-18
    NISH1001@github.com
"""

from glob import glob
import os
from ytmdl.stringutils import (
    remove_multiple_spaces, remove_punct, compute_jaccard, remove_stopwords,
    check_keywords
)
from ytmdl.defaults import DEFAULT
from ytmdl.prepend import PREPEND
from simber import Logger
from colorama import Fore, Style

logger = Logger("cache")


class Cache:
    """The main caching component."""

    def __init__(self, directory=None):
        """Init the stuff."""
        if directory is None:
            directory = DEFAULT.SONG_DIR
            # Check the dir only if special characters are present
            if '$' in directory:
                directory = directory.split("$")[0]
        directory = os.path.expanduser(directory)
        self.directory = directory
        self.max_depth = 4

    def _get_files(self, song_name):
        """
        List all the files in the passed dir.
        """
        files = []
        for depth in range(0, self.max_depth):
            pattern = '{}{}{}*'.format(
                self.directory,
                '{}'.format(os.sep).join(depth * ['*']),
                song_name
            )
            files.extend(glob(pattern))

        return files

    def search(self, song_name):
        logger.info(
            "Searching to see if already present in {}".format(
                self.directory)
        )
        return len(self._get_files(song_name))


def main(SONG_NAME=''):
    """Run on program call."""
    cache = Cache()
    match = cache.search(SONG_NAME)
    if match:
        PREPEND(1)
        print(Fore.MAGENTA, end='')
        print('{} '.format(SONG_NAME), end='')
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
    main("Cradles")
