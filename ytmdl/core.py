"""Contain all the core functions for ytmdl"""

from typing import Union
from simber import Logger
from colorama import Fore, Style

from ytmdl import (
    yt,
    song,
    stringutils,
    defaults,
    utility,
    manual,
    metadata
)
from ytmdl.exceptions import (
    DownloadError, ConvertError, NoMetaError, MetadataError
)


logger = Logger("core")


def search(song_name, args) -> Union[str, str]:
    """Search the song on YouTube, ask the user for an input and accordingly
    return a selected song.

    The song can be extracted either from an URL or the name. If the name is
    present, we will search on YouTube for the name, ask the user for a choice
    and accordingly return the choice.

    If the URL is present, we will extract the data from the URL and return it
    accordingly.
    """
    # Declare some default values
    YOUTUBE_LINK_BASE = "https://youtube.com{}"
    PASSED_CHOICE = args.choice
    URL = args.url
    IS_QUIET = args.quiet

    if URL is None:
        if IS_QUIET:
            logger.info('Quiet is enabled')

        logger.info('Searching Youtube for {}{}{}'.format(
            Fore.LIGHTYELLOW_EX,
            song_name,
            Style.RESET_ALL
        ))

        data = yt.search(song_name, not args.disable_metaadd,
                         args.proxy,
                         kw=[args.artist, args.album])

        # Handle the exception if urls has len 0
        if len(data) == 0:
            logger.critical(
                "No song found. Please try again with a different keyword.")

        if not IS_QUIET:
            # Ask for a choice
            choice = song.getChoice(data, 'mp3')
        elif PASSED_CHOICE is not None and PASSED_CHOICE <= len(data):
            choice = PASSED_CHOICE - 1
            logger.info("Using {} as choice".format(PASSED_CHOICE))
        else:
            # Extract the verified music result if valid
            choice = song.get_default(data) - 1

        # Check if choice if -2. If it is that, then we need to stop executing
        # of the current song and gracefully exit.
        if choice == -2 or choice == -1:
            return False, False

        return (
            YOUTUBE_LINK_BASE.format(data[choice]["href"]),
            data[choice]["title"]
        )

    # If the url is passed then get the data
    data = []

    # Strip unwanted stuff from the URL
    URL = stringutils.srtip_unwanted_words_from_url(URL)

    # Get video data from youtube
    temp_data = yt.scan_video(yt.get_href(URL), args.proxy)

    # Sometimes the temp_data may be returned as unauthorized, skip that
    if type(temp_data) is str and temp_data.lower() == "Unauthorized".lower():
        if args.ignore_errors:
            logger.warning("{}: is unauthorized".format(URL))
            return None, None
        else:
            logger.critical("{}: is unauthorized".format(URL))

    data.append(temp_data)

    # In this case choice will be 0
    return URL, data[0]["title"]


def download(link, yt_title, args) -> str:
    """Download the song by using the passed link.

    The song will be saved with the passed title.
    Return the saved path of the song.
    """
    logger.info('Downloading {}{}{} in {}{}kbps{}'.format(
        Fore.LIGHTMAGENTA_EX,
        yt_title,
        Style.RESET_ALL,
        Fore.LIGHTYELLOW_EX,
        defaults.DEFAULT.SONG_QUALITY,
        Style.RESET_ALL
    ))
    path = yt.dw(link, args.proxy, yt_title,
                 args.format, no_progress=args.quiet,
                 ytdl_config=args.ytdl_config, dont_convert=args.dont_transcode)

    if type(path) is not str:
        # Probably an error occured
        raise DownloadError(link, path)

    logger.info('Downloaded!')
    return path


def convert(
    path: str,
    passed_format: str,
    start: float = None,
    end: float = None,
    dont_convert: bool = False
) -> str:
    """Convert the song into the proper format as asked by
    the user.
    """
    FORMAT_CONVERSION_MAP = {
        "mp3": utility.convert_to_mp3,
        "opus": utility.convert_to_opus
    }

    # We need to check if start and end are passed.
    # If those are passed it means only a part of the song is
    # to be extracted.
    logger.debug("{}:{}".format(start, end))
    if start is not None and end is not None:
        conv_name = utility.extract_part_convert(
            path, passed_format, start, end)

        # We need to raise exception if something went wrong
        if type(conv_name) is not str:
            raise ConvertError(conv_name)

        return conv_name

    # If it is m4a, don't convert
    #
    # If dont_convert is passed, we can skip the conversion since
    # the user wants to keep the original audio
    if passed_format == "m4a" or dont_convert:
        return path

    # Else the format needs to be in the list
    # It should probably in the list since the check
    # is done once before by the main function
    if passed_format not in FORMAT_CONVERSION_MAP.keys():
        return

    conv_name = FORMAT_CONVERSION_MAP.get(passed_format)(path)

    if type(conv_name) is not str:
        raise ConvertError(conv_name)

    return conv_name


def trim(name: str, args) -> None:
    """Trim the song of unwanted noise by making calls to the
    internal functions.
    """
    # Check if we need to import trim. Importing it is realy inefficient if
    # the user is not going to use it.
    if not args.trim:
        return

    logger.debug("Need to trim the song, importing the trim module.")
    try:
        from ytmdl import trim
    except ImportError:
        logger.error("Dependencies needed for trim are not installed. "
                     "Please use the [noise-clean] specifier when "
                     "installing ytmdl. The script will continue "
                     "without trimming.")
        return

    # Trim the song if the trim option is passed.
    logger.info("Passing the song to get trimmed.")
    trim.Trim(name)


def meta(conv_name: str, song_name: str, search_by: str, args):
    """Handle adding the metadata for the passed song.

    We will use the passed name to search for metadata, ask
    the user for a choice and accordingly add the meta to
    the song.
    """
    PASSED_FORMAT = args.format
    IS_QUIET = args.quiet

    # Check if the user wants a new name for metadata
    if args.ask_meta_name:
        search_by = utility.get_new_meta_search_by(search_by)

    if args.manual_meta:
        # Read the values from the user.
        TRACK_INFO = manual.get_data(song_name)

        # Since above code will return a list with just
        # one element, the option will be set to 0 by
        # default and won't ask the user
    elif args.itunes_id:
        logger.info('Direct iTunes lookup for {}...'.format(args.itunes_id))
        TRACK_INFO = metadata.lookup_from_itunes(args.itunes_id)
    elif args.spotify_id:
        logger.info('Direct Spotify lookup for {}...'.format(args.spotify_id))
        TRACK_INFO = metadata.lookup_from_spotify(args.spotify_id)
    else:
        # Else add metadata in ordinary way
        logger.info('Getting song data for {}...'.format(search_by))
        TRACK_INFO = metadata.SEARCH_SONG(search_by, song_name, filters=[
                                          args.artist, args.album],
                                          disable_sort=args.disable_sort)

    # If no meta was found raise error
    if not TRACK_INFO:
        # Check if we are supposed to add manual meta
        if args.on_meta_error != "manual":
            raise NoMetaError(search_by)

        TRACK_INFO = manual.get_data(song_name)
        return TRACK_INFO

    logger.info('Setting data...')
    option = song.setData(TRACK_INFO, IS_QUIET, conv_name, PASSED_FORMAT,
                          args.choice)

    if type(option) is not int:
        raise MetadataError(search_by)

    # If meta was skipped, indicate that
    if option == -1:
        logger.warning(
            "Metadata was skipped because -1 was entered as the option")
        return None
    # If amending the search, get the new search and retry
    elif option == -2:
        logger.info(
            "Amending the search because -2 was entered as the option")
        search_by = utility.get_new_meta_search_by(search_by)
        return meta(conv_name, song_name, search_by, args)

    return TRACK_INFO[option]
