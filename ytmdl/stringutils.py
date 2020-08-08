#!/usr/bin/env python3
"""
    A magic module for various string operations
"""

import difflib
import json
import re
import urllib.parse


def get_closest_match(string_list, string):
    closest_matches = difflib.get_close_matches(string, string_list, len(string_list), 0.6)
    return closest_matches if len(closest_matches)>0 else None


def get_closest_match_ignorecase(string_list, string):
    """
        Find the closest match of a string
        from the list of the string.
        This will ignore the cases
    """
    string_lower = string.lower().strip()
    if not string_list:
        return None

    # create a tuple of lowercased string and corresponding index
    # in the original list
    strings = [ (s.lower(), i) for i, s in enumerate(string_list) ]
    string_matched = get_closest_match( list(zip(*strings))[0], string_lower)
    for tup in strings:
        if string_matched == tup[0]:
            return string_list[tup[1]]
    return None

def escape_characters(string):
    return json.dumps(string)[1:-1]

def escape_quotes(string):
    return re.sub(r'"', '\\"', string)

def remove_multiple_spaces(string):
    return re.sub(r'\s+', ' ', string)

def replace_space(string, replacer):
    return re.sub(r"\s", replacer, string)

def remove_punct(string):
    return re.sub(r"[-:_!,'()’]+", '', string)

def replace_character(string, character, replacer):
    return re.sub(r"{}".format(character), replacer, string)

def compute_jaccard(tokens1, tokens2):
    union = set(tokens1).union(tokens2)
    intersect = set(tokens1).intersection(tokens2)
    return len(intersect)/len(union)

def remove_unwanted_chars(string):
    return re.sub(r" |/", "#", string)


def urlencode(text):
    """
        Url encode the text
    """
    q = {}
    encoded = ""
    if(text):
        q['q'] = text
        encoded = urllib.parse.urlencode(q)
        encoded = encoded[2::]
    return encoded

def remove_stopwords(string):
    stopwords = ['the', 'in', 'of', 'at']
    res = []
    tokens = string.split()
    for token in tokens:
        if token not in stopwords:
            res.append(token)
    return ' '.join(res)


def check_keywords(tokens1, tokens2):
    """Check if all the tokens from tokens1 is in tokens2 list."""
    res = [token in tokens2 for token in tokens1]
    return sum(res) == len(tokens1)


def remove_yt_words(title):
    """
    Remove words like Official video etc from the name of the song
    """
    # Remove stopwords like official, video etc
    # Remove square as well as circle brackets
    # Remove dashes (-) and trademark icons like ®
    # Remove spaces in the beginning or at the end
    title = re.sub(
                r'\]|\[|official|video|music|audio|full|lyrics?|-|\)|\(|®|^[ ]*|[ ]*$',
                '',
                str(title).lower()
            )
    # Replace more than one space with one space
    title = re.sub(r'\ {2,}', ' ', title)
    return title


def srtip_unwanted_words_from_url(url):
    """
    If more than just the video ID is passed, extract the
    URL and operate on that only.

    The URL will be of the type https://yotuube.com/watch?v=<id>&other_args

    We just need to keep the v arg and remove all the other args
    """
    return url.split("&")[0]


def main():
    print(remove_yt_words("    Nana   haha  "))

if __name__ == "__main__":
    main()
