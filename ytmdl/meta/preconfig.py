"""
Handle all the preconfigurations related to metadata
"""

from ytmdl.meta.deezer import get_more_data


class CONFIG:
    """
    Class to handle all the preconfigurations
    related to the metadata sources
    """

    # Some sources require fetching extra data
    GET_EXTRA_DATA = {
        'deezer': get_more_data
    }

    # Search sensitivity is the restriction on matching the
    # search results to the value entered by the user.
    SEARCH_SENSITIVITY = 0.5
