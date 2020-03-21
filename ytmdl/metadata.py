"""Define functions related to getting tags."""

import itunespy
from ytmdl.stringutils import (
    remove_multiple_spaces, remove_punct, compute_jaccard, remove_stopwords,
    check_keywords
)
from ytmdl import gaana


def get_from_itunes(SONG_NAME):
    """Try to download the metadata using itunespy."""
    # Try to get the song data from itunes
    try:
        SONG_INFO = itunespy.search_track(SONG_NAME)
        # Before returning convert all the track_time values to minutes.
        for song in SONG_INFO:
            song.track_time = round(song.track_time / 60000, 2)
        return SONG_INFO
    except Exception:
        pass


def get_from_gaana(SONG_NAME):
    """Get some tags from gaana."""
    try:
        nana = gaana.searchSong(SONG_NAME)
        return nana
    except Exception:
        return None


def _search_tokens(song_name, song_list):
    """Search song in the cache based on simple each word matching."""
    song_name = remove_punct(
                    remove_stopwords(
                        remove_multiple_spaces(song_name).lower()
                    ))
    tokens1 = song_name.split()
    cached_songs = song_list

    res = []
    for song in cached_songs:
        song_back = song
        name = song.track_name.lower()
        name = remove_punct(name)
        name = remove_multiple_spaces(name)
        tokens2 = name.split()
        match = check_keywords(tokens1, tokens2)
        if match:
            dist = compute_jaccard(tokens1, tokens2)
            if dist >= 1:
                res.append((song_back, dist))
    res = sorted(res, key=lambda x: x[1], reverse=True)

    # Return w/o the dist values
    for i in range(0, len(res)):
        res[i] = res[i][0]
    return res


def filterSongs(data, filters=[]):
    """Filter the songs according to the passed filters.

    In the passed filters the first element is artist.
    The second element is album."""

    # In some cases the data can be None, then just return 
    if data is None:
        return data

    new_tuple = []
    rest = []

    for songData in data:
        artistMatch = True
        albumMatch = True

        if filters[0] is not None:
            artistMatch = (songData.artist_name == filters[0])
        if filters[1] is not None:
            albumMatch = (songData.collection_name == filters[1])

        if artistMatch and albumMatch:
            new_tuple.append(songData)
        else:
            rest.append(songData)
    return (new_tuple + rest)


def SEARCH_SONG(q="Tera Buzz", filters=[]):
    """Do the task by calling other functions."""
    to_be_sorted = []
    rest = []

    # Get from itunes
    data_itunes = get_from_itunes(q)
    data_gaana = get_from_gaana(q)

    # Before passing for sorting filter the songs
    # with the passed args
    if len(filters) != 0:
        data_itunes = filterSongs(data_itunes, filters)
        data_gaana = filterSongs(data_gaana, filters)

    if data_itunes is not None:
        to_be_sorted = data_itunes[:10]
        rest = data_itunes[10:]

    if data_gaana is not None:
        to_be_sorted += data_gaana[:10]
        rest += data_gaana[10:]

    if len(to_be_sorted) == 0:
        return False

    # Send the data to get sorted
    sorted_data = _search_tokens(q, to_be_sorted)
    # sorted_data = to_be_sorted

    # Add the unsorted data
    sorted_data += rest

    return sorted_data


if __name__ == '__main__':
    n = SEARCH_SONG("That's what I like", ["Bruno Mars", None])

    for i in n:
        print(i.track_name + ' by ' + i.artist_name + ' of ' + i.collection_name)
