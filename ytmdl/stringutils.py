#!/usr/bin/env python3
"""A magic module for various string operations.

    Nishan Pantha(c) 2017-18
    NISH1001@github.com
"""

import difflib


def get_closest_match(string_list, string):
    """Get the closest_match."""
    closest_matches = difflib.get_close_matches(string, string_list,
                                                len(string_list), 0.3)
    return closest_matches[0] if len(closest_matches) > 0 else None


def get_closest_match_ignorecase(string_list, string):
    """Find the closest match of a string from the list of the string.

    This will ignore the cases.
    """
    string_lower = string.lower().strip()
    if not string_list:
        return None

    # create a tuple of lowercased string and corresponding index
    # in the original list
    strings = [(s.lower(), i) for i, s in enumerate(string_list)]
    string_matched = get_closest_match(list(zip(*strings))[0], string_lower)
    for tup in strings:
        if string_matched == tup[0]:
            return string_list[tup[1]]
    return None
