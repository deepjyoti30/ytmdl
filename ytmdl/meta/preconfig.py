"""
Handle all the preconfigurations related to metadata
"""

from ytmdl.meta import deezer
from ytmdl.meta import lastfm
from ytmdl.meta import musicbrainz


class CONFIG:
    """
    Class to handle all the preconfigurations
    related to the metadata sources
    """

    # Some sources require fetching extra data
    GET_EXTRA_DATA = {
        'deezer': deezer.get_more_data,
        'lastfm': lastfm.get_more_data,
        'musicbrainz': musicbrainz.get_more_data
    }

    # Search sensitivity is the restriction on matching the
    # search results to the value entered by the user.
    SEARCH_SENSITIVITY = 0.5
