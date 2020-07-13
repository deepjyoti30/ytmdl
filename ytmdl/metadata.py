"""Define functions related to getting tags."""

import itunespy
from ytmdl.stringutils import (
    remove_multiple_spaces, remove_punct, compute_jaccard, remove_stopwords,
    check_keywords
)
from ytmdl import gaana, logger, defaults
from unidecode import unidecode

logger = logger.Logger('metadata')


def _logger_provider_error(exception, name):
    """Show error if providers throw an error"""
    logger.debug('{}'.format(exception))
    logger.error(
        "Something went wrong with {}. The program will continue with"
        "the other providers. Please check '{}' for more details.\
            ".format(name, logger.get_log_file()))


def get_from_itunes(SONG_NAME):
    """Try to download the metadata using itunespy."""
    # Try to get the song data from itunes
    try:
        SONG_INFO = itunespy.search_track(SONG_NAME)
        # Before returning convert all the track_time values to minutes.
        for song in SONG_INFO:
            song.track_time = round(song.track_time / 60000, 2)
        return SONG_INFO
    except Exception as e:
        _logger_provider_error(e, 'iTunes')
        return None


def get_from_gaana(SONG_NAME):
    """Get some tags from gaana."""
    try:
        nana = gaana.searchSong(SONG_NAME)
        return nana
    except Exception as e:
        _logger_provider_error(e, 'Gaana')
        return None


def _search_tokens(song_name, song_list):
    """Search song in the cache based on simple each word matching."""
    song_name = remove_punct(
                    remove_stopwords(
                        remove_multiple_spaces(unidecode(song_name)).lower()
                    ))
    tokens1 = song_name.split()
    cached_songs = song_list

    res = []
    for song in cached_songs:
        song_back = song
        name = song.track_name.lower()
        name = remove_punct(name)
        name = remove_multiple_spaces(name)
        name = unidecode(name)
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


def _extend_to_be_sorted_and_rest(provider_data, to_be_sorted, rest, filters):
    """Create the to be sorted and rest lists"""
    # Before passing for sorting filter the songs
    # with the passed args
    if filters:
        provider_data = filterSongs(provider_data, filters)
    if provider_data is not None:
        to_be_sorted.extend(provider_data[:10])
        rest.extend(provider_data[10:])


def SEARCH_SONG(q="Tera Buzz", filters=[]):
    """Do the task by calling other functions."""
    to_be_sorted = []
    rest = []

    metadata_providers = defaults.DEFAULT.METADATA_PROVIDERS

    GET_METADATA_ACTIONS = {
        'itunes': get_from_itunes,
        'gaana': get_from_gaana
    }

    broken_provider_counter = 0

    for provider in metadata_providers:
        data_provider = GET_METADATA_ACTIONS.get(
            provider, lambda _: None)(q)
        if data_provider:
            _extend_to_be_sorted_and_rest(
                data_provider, to_be_sorted, rest, filters)
        else:
            logger.warning(
                        '"{}" isn\'t implemented. Skipping!'.format(provider)
                    )
            broken_provider_counter += 1

    # to_be_sorted will be empty and it will return None anyway, no need
    # to do it here as well
    if broken_provider_counter == len(metadata_providers):
        logger.critical("{}".format(
                            'No metadata provider in the configuration is '
                            'implemented. Please change it to something \
                            available or use the --skip-meta flag'))

    if not to_be_sorted:
        return None

    # Send the data to get sorted
    sorted_data = _search_tokens(q, to_be_sorted)

    # Add the unsorted data
    sorted_data += rest

    return sorted_data


if __name__ == '__main__':
    n = SEARCH_SONG("That's what I like", ["Bruno Mars", None])

    for i in n:
        print(i.track_name + ' by ' + i.artist_name + ' of ' + i.collection_name)
