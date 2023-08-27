#!/usr/bin/env python3
"""
    * ytmdl.py - A script to download songs.

----------------------------------------------------
     A simple script to download songs in mp3 format
     from Youtube.
     Users pass the song name as arguments.
----------------------------------------------------
    --> Deepjyoti Barman
    --> deepjyoti30@github.com
"""

from __future__ import unicode_literals

from colorama import init
from colorama import Style
import argparse
from xdg.BaseDirectory import xdg_cache_home
from os import path
from simber import Logger
from ytmdl import (
    dir,
    yt,
    defaults,
    setupConfig,
    cache,
    utility,
)
from ytmdl.exceptions import (
    DownloadError, ConvertError, NoMetaError, MetadataError,
    ExtractError
)
from ytmdl.core import (
    search, download, convert, trim, meta
)
from ytmdl.utils.archive import (
    open_archive_stream,
    is_present_in_archive,
    add_song_to_archive
)
from ytmdl.utils.ytdl import is_ytdl_config_present
from ytmdl.yt import is_yt_url
from ytmdl.__version__ import __version__
from typing import Tuple

# init colorama for windows
init()

LOGGER_OUTTEMPLATE = " %a{}==>{}%".format(Style.BRIGHT, Style.RESET_ALL)
LOGGER_FILEFORMAT = "[{logger}]:[{time}]: "
logger = Logger('ytmdl',
                log_path=path.join(xdg_cache_home, 'ytmdl/logs/log.cat'),
                format=LOGGER_OUTTEMPLATE,
                file_format=LOGGER_FILEFORMAT,
                update_all=True
                )


def arguments():
    """Parse the arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument('SONG_NAME', help="Name of the song to download.\
                         Can be an URL to a playlist as well. It will be\
                         automatically recognized.",
                        type=str, nargs="*")
    parser.add_argument('-q', '--quiet',
                        help="Don't ask the user to select songs\
                        if more than one search result.\
                        The first result in each case will be considered.",
                        action='store_true')
    parser.add_argument('-o', '--output-dir',
                        help="The location for the song to be downloaded\
                        to. When no argument is passed, the default locations\
                        of SONG_DIR or XDG_MUSIC_DIR are used.")
    metadata_group = parser.add_argument_group("Metadata")
    metadata_group.add_argument(
        '--song', help="The song to search in Metadata. \
                        Particularly useful for songs that have the names in a\
                        different language in YouTube. For Example, greek songs.",
        metavar='SONG-METADATA', default=None)
    metadata_group.add_argument(
        '--choice', help="The choice that the user wants\
                        to go for. Usefull to pass along with --quiet.\
                        Choices start at 1", choices=range(1, 50),
        type=int, default=None, metavar="CHOICE")
    metadata_group.add_argument(
        '--artist', help="The name of the song's artist.\
                        Pass it with a song name.")
    metadata_group.add_argument(
        '--album', help="The name of the song's album.\
                        Pass it with a song name.")
    metadata_group.add_argument('--disable-metaadd', help="Disable addition of\
                        passed artist and album keyword to the youtube search\
                        in order to get a more accurate result. (Default: false)",
                                action="store_true")
    metadata_group.add_argument('--skip-meta', help="Skip setting the metadata and\
                        just copy the converted song to the destination directory.\
                        '--manual-meta' will override this option, pass only one\
                        of them.",
                                action="store_true")
    metadata_group.add_argument('-m', '--manual-meta', help="Manually enter song\
                        details.", action="store_true")
    metadata_group.add_argument(
        '--itunes-id', help="Direct lookup from itunes. If passed, metadata will be automatically added.")
    metadata_group.add_argument(
        "--spotify-id", help="Direct lookup for Spotify tracks using the ID. If passed, metadata will be automatically added.")
    metadata_group.add_argument("--disable-sort", help="Disable sorting of the metadata \
                        before asking for input. Useful if the song is in some other language \
                        and/or just a few providers are used.", action="store_true")
    metadata_group.add_argument("--ask-meta-name", help="Ask the user to enter a separate \
                        name for searching the metadata (Default: false)", action="store_true")
    metadata_group.add_argument("--on-meta-error", help="What to do if adding the metadata fails \
                        for some reason like lack of metadata or perhaps a network issue. \
                        Options are {}".format(defaults.DEFAULT.ON_ERROR_OPTIONS),
                                type=str, default=None)

    parser.add_argument('--proxy', help='Use the specified HTTP/HTTPS/SOCKS proxy. To enable '
                        'SOCKS proxy, specify a proper scheme. For example '
                        'socks5://127.0.0.1:1080/. Pass in an empty string (--proxy "") '
                        'for direct connection', default=None, metavar='URL')
    parser.add_argument('--url',
                        help="Youtube song link.")
    parser.add_argument('--list', help="Download list of songs.\
                        The list should have one song name in every line.",
                        default=None, metavar="path to list".upper())
    parser.add_argument('--nolocal',
                        help='Don\'t search locally for the song before\
                        downloading.',
                        action='store_true')
    parser.add_argument('--format',
                        help="The format in which the song should be downloaded.\
                        Default is mp3, but can be set in config. Available options are\
                         {}".format(defaults.DEFAULT.VALID_FORMATS),
                        default=defaults.DEFAULT.DEFAULT_FORMAT,
                        type=str)
    parser.add_argument('--trim', '-t', help="Trim out the audio from the song. Use \
                        underlying speech and music segmentation engine to determine \
                        and keep only the music in the file. Useful in songs where there \
                        are speeches, noise etc before/after the start of the song. Default \
                        is false.", action='store_true')
    parser.add_argument('--version', action='version', version=__version__,
                        help='show the program version number and exit')
    parser.add_argument('--get-opts', action="store_true",
                        help=argparse.SUPPRESS)
    parser.add_argument("--keep-chapter-name", action="store_true", help="Keep the title \
                        extracted from the chapter in order to search for the metadata. If \
                        not passed, the user will be asked if they'd like to change the title \
                        with which the metadata will be searched.")
    parser.add_argument("--download-archive", help="Skip downloading songs that are present in \
                        the passed file. The songs are matched by using the videoId. All downloaded \
                        song Id's are automatically added to the file.", default=None,
                        metavar="FILE")
    parser.add_argument('--ignore-chapters', help="Ignore chapters if available in the video and treat \
                        it like one video",
                        action="store_true")
    parser.add_argument('--ytdl-config', help="Path to the youtube-dl config location or the "
                        "directory", default=None, metavar="PATH", type=str)
    parser.add_argument("--dont-transcode", help="Don't transcode the audio after \
                        downloading. Applicable for OPUS format only. (Default: false)",
                        action="store_true")
    parser.add_argument("--filename", help="Final filename after the song is ready to be used. \
                        This will be given priority over automatic detection unless dynamic filename \
                        path is set through config", default=None, metavar="NAME", type=str)

    playlist_group = parser.add_argument_group("Playlist")
    playlist_group.add_argument(
        "--pl-start",
        help="Playlist video to start at (default is 1)",
        default=None,
        metavar="NUMBER",
        type=int
    )
    playlist_group.add_argument(
        "--pl-end",
        help="Playlist video to end at (default is last)",
        default=None,
        metavar="NUMBER",
        type=int
    )
    playlist_group.add_argument(
        "--pl-items",
        help="Playlist video items to download. \
             Specify indices of the videos present in the\
             playlist separated by commas like: '--playlist-items\
              1, 2, 4, 6' if you want to download videos indexed\
             1, 2, 4 and 6. Range can also be passed like:\
             '--playlist-items 1-3, 5-7' to download the videos\
             indexed at 1, 2, 3, 5, 6, 7.",
        type=str,
        metavar="item_spec".upper(),
        default=None
    )
    playlist_group.add_argument(
        "--ignore-errors",
        help="Ignore if downloading any video fails in a playlist.\
             If passed, the execution will move to the next video in the\
             passed playlist.",
        action="store_true"
    )
    playlist_group.add_argument(
        "--title-as-name",
        help="Use the title of the video as the name of the song to search\
            for metadata. If not passed, user will be asked if they\
            want to use a different name and continue accordingly.",
        action="store_true"
    )

    logger_group = parser.add_argument_group("Logger")
    logger_group.add_argument(
        "--level",
        help="The level of the logger that will be used while verbosing.\
            Use `--list-level` to check available options." + "\n",
        default="INFO",
        type=str
    )
    logger_group.add_argument(
        "--disable-file",
        help="Disable logging to files",
        default=False,
        action="store_true",
    )
    logger_group.add_argument(
        "--list-level",
        help="List all the available logger levels.",
        action="store_true"
    )

    args = parser.parse_args()

    return args


def main(args):
    """Run on program call."""

    song_name, verify_name = extract_song_name(args)
    logger.debug("verify title: ", str(verify_name))

    # Extract the archive file contents
    is_download_archive = args.download_archive is not None
    stream = None

    if is_download_archive:
        archive_content, stream = open_archive_stream(args.download_archive)

    logger.debug(song_name)
    logger.hold()
    logger.debug(stream)

    if not args.nolocal:
        # Search for the song locally
        if not cache.main(song_name):
            return 0

    # Check if ffmpeg is installed.
    if not utility.is_present('ffmpeg'):
        logger.critical("ffmpeg is not installed. Please install it!")

    passed_format = args.format.lower()

    logger.debug("proxy passed: {}".format(args.proxy))
    logger.debug("Passed format: {}".format(passed_format))

    # Check if passed format is support, if not exit.
    if passed_format not in defaults.DEFAULT.VALID_FORMATS:
        logger.critical("Passed format is not supported yet!")

    if args.song is not None:
        song_metadata = args.song
    else:
        song_metadata = song_name

    link, yt_title = search(song_name=song_name, args=args)

    # Check if this song is supposed to be skipped.
    if not link:
        logger.warning("Skipping this song!")
        return

    # If download archive is passed then skip the song.
    if is_download_archive and is_present_in_archive(archive_content, link):
        logger.warning("videoId found in the archive file. Skipping the song!")
        return

    # Try to download the song
    # TODO: Change the way ignore-errors is used in order to handle playlists
    try:
        path = download(link, yt_title, args)
    except DownloadError as dw_error:
        if args.ignore_errors:
            logger.info("--ignore-errors passed. Skipping this song!")
            return

        logger.critical("ERROR: {}".format(dw_error),
                        ". Pass `--ignore-errors` to ignore this.")
        return

    # Try to extract the chapters
    chapters = yt.get_chapters(link, args.ytdl_config)

    # Add the current passed song as the only entry here
    # This dictionary will be cleared if the song is found to be containing
    # chapters.
    #
    # Moreover, the `is_original` field is **not** present from the youtube
    # response which would force the following code to verify the title
    # for chapters which is the behavior we want.
    songs_to_download = [{'title': song_name, 'is_original': not verify_name}]

    # If the chapters are present, we will have to iterate and extract each chapter
    if chapters and not args.ignore_chapters:
        logger.info("The song has chapters in it.",
                    "Each part will be extracted and worked accordingly.")

        songs_to_download.clear()
        for chapter in chapters:
            songs_to_download.append(chapter)

    logger.debug("songs to download: ", str(songs_to_download))
    for song in songs_to_download:
        song_title = song.get("title", yt_title)
        start_time = song.get("start_time", None)
        end_time = song.get("end_time", None)

        is_original = song.get("is_original", False)
        logger.debug("is original: ", str(is_original))

        if "title" in song.keys():
            logger.debug("Has the attribute")
            # Update the song_metadata with the name of the chapter
            song_metadata = song.get("title")

            # Ask the user if they would like to change the name
            #
            # NOTE: Check if skip meta is passed, we don't need to
            # extract the new title.
            song_metadata = utility.get_new_title(song_metadata) if \
                (not args.keep_chapter_name and not args.skip_meta and not is_original) else song_metadata

        # Pass the song for post processing
        try:
            post_processing(
                song_title,
                song_metadata,
                passed_format,
                path,
                start_time,
                end_time,
                args,
                link,
                stream,
                is_download_archive
            )
        except Exception as e:
            if args.ignore_errors:
                logger.warning("Ignoring error: ", str(e))
                continue

            # Else exit
            logger.critical("Error occurred: ", str(e),
                            ". Exiting. Pass `--ignore-errors` if you want errors"
                            "like this to be ignored")

    # Delete the cached songs
    dir._delete_cached_songs(passed_format)


def post_processing(
    song_name: str,
    song_metadata: str,
    passed_format: str,
    path: str,
    start_time: float,
    end_time: float,
    args: object,
    link: str,
    stream,
    is_download_archive: bool
) -> None:
    """Handle all the activities post search of the song.

    This function will handle the following:
    Convert, Trim, Metadata, Cleaning up.
    """
    logger.debug("song_name: ", song_name, " song_meta: ", song_metadata)
    logger.debug(stream)
    # Try to convert the song
    try:
        conv_name = convert(path, passed_format, start_time,
                            end_time, args.dont_transcode)
    except ConvertError as convert_error:
        logger.critical('ERROR: {}'.format(convert_error))
        return

    # Trim the song
    trim(conv_name, args)

    logger.debug("Skip Meta: {}".format(args.skip_meta))

    if args.skip_meta:
        # Write to the archive file
        add_song_to_archive(
            stream=stream, youtube_link=link) if is_download_archive else None

        # Do a dry cleanup
        if dir.dry_cleanup(conv_name, song_name, args.filename):
            logger.info("Done")
            return

    # Else fill the meta by searching
    try:
        track_selected = meta(conv_name, song_name, song_metadata, args)
    except NoMetaError as no_meta_error:
        if args.on_meta_error == 'skip':
            # Write to the archive file
            add_song_to_archive(
                stream=stream, youtube_link=link) if is_download_archive else None

        if dir.dry_cleanup(conv_name, song_name, args.filename):
            logger.info("Done")
        elif not args.ignore_errors or args.on_meta_error == 'exit':
            logger.critical(
                str(no_meta_error), ". Pass `--ignore-errors` or `on-meta-error` to ignore this.")
        return
    except MetadataError as metadata_error:
        if not args.ignore_errors:
            logger.critical(str(
                metadata_error), ". Pass `--ignore-errors` or `on-meta-error` to ignore this.")
        return

    # Write to the archive file
    add_song_to_archive(
        stream=stream, youtube_link=link) if is_download_archive else None

    # If no metadata was selected, just do a dry cleanup and skip the
    # song
    if track_selected is None:
        if dir.dry_cleanup(conv_name, song_name, args.filename):
            logger.info("Done")
        elif not args.ignore_errors or args.on_meta_error == 'exit':
            logger.critical(
                ". Pass `--ignore-errors` or `on-meta-error` to ignore this.")
        return

    if dir.cleanup([track_selected], 0, passed_format, remove_cached=False,
                   filename_passed=args.filename):
        logger.info("Done")


def pre_checks(args):
    """Run some checks in order to make sure the basic things are
    working all right.
    """
    if args.list_level:
        logger.list_available_levels()
        exit(0)

    # If options is asked for
    #
    # It is important not to run any possible verbose commands
    # before this output because this one is used for automatic
    # generation of the completion files.
    if args.get_opts:
        print(" ".join(("--{}".format(opt.replace("_", "-"))
              for opt in vars(args))))
        exit(0)

    # Update the logger flags, in case those are not the default ones.
    if args.level.lower != "info":
        logger.update_level(args.level.upper())

    if args.disable_file:
        logger.update_disable_file(True)
        logger.debug("Writing logs to file disabled")

    # Just a message to make the user aware of the current running state
    logger.debug("Logger running in DEBUG mode")
    logger.debug("Passed args: {}".format(args))

    # Check if --setup is passed
    if not setupConfig.check_config_setup():
        logger.debug("Config not present, creating default.")
        setupConfig.make_config()
        logger.debug("Config created")
        logger.info("Created new config since none was present")

    # Check if ytdl config is present if it is passed
    if args.ytdl_config and not is_ytdl_config_present(args.ytdl_config):
        logger.critical(
            "YoutubeDL config passed is invalid or not present:", args.ytdl_config)

    # Ensure the output directory is legitimate
    if (args.output_dir is not None):
        if path.isdir(path.expanduser(args.output_dir)):
            defaults.DEFAULT.SONG_DIR = path.expanduser(args.output_dir)
        else:
            logger.warning(
                "{}: is an invalid path. Continuing with default.".format(args.output_dir))

    # Extract on-meta-error
    logger.debug("on_meta_error before: ", str(args.on_meta_error))
    on_meta_error = args.on_meta_error
    if on_meta_error not in defaults.DEFAULT.ON_ERROR_OPTIONS:
        args.on_meta_error = defaults.DEFAULT.ON_ERROR_DEFAULT

    logger.debug("on_meta_error after: ", args.on_meta_error)

    # Check the Itunes Country value
    logger.debug("itunes_country:", defaults.DEFAULT.ITUNES_COUNTRY)

    if not args.SONG_NAME and not args.url and not args.list:
        logger.critical(
            "Song Name is required. Check 'ytmdl --help' for help.")


def extract_song_name(args) -> Tuple[str, bool]:
    """Extract the name of the song from the given args"""
    logger.debug(args.SONG_NAME)

    if args.SONG_NAME:
        return " ".join(args.SONG_NAME), False

    # If song name is not passed then try to extract
    # the title of the song using the URL.
    verify_title = True
    try:
        # Fetch the title of the song
        song_name, verify_title = yt.get_title(args.url, args.ytdl_config)
    except ExtractError:
        if not args.ignore_errors:
            logger.critical("Wasn't able to extract song data.",
                            "Use `--ignore-errors` to ignore this error")
        return None, False

    # Ask the user if they want to go with the extracted
    # title or if they would like to change it.
    #
    # NOTE: We don't need the song name if the meta is to be
    # skipped. So we can skip the next step if --skip-meta is
    # passed.
    if not args.title_as_name and not args.skip_meta and verify_title:
        song_name = utility.get_new_title(song_name)
        verify_title = False

    return song_name, verify_title


def extract_data():
    """Extract the arguments and act accordingly."""
    args = arguments()
    pre_checks(args)

    if args.list is not None:
        songs = utility.get_songs(args.list)
        logger.debug(str(songs))
        if len(songs) != 0:
            logger.info("Downloading songs in {}".format(args.list))
            for song_name in songs:
                logger.debug(song_name)

                # Set the song name if an URL is not passed, else
                # pass it as an URL
                if is_yt_url(song_name):
                    logger.debug("Detected passed song as URL")
                    args.url = song_name
                else:
                    args.SONG_NAME = [song_name]

                main(args)
        else:
            logger.info("{}: is empty".format(args.list))
    elif args.SONG_NAME and yt.is_playlist(args.SONG_NAME[0]):
        logger.info("Youtube playlist passed...extracting!")
        songs, playlist_name = yt.get_playlist(
            args.SONG_NAME[0],
            args.proxy,
            args.pl_start,
            args.pl_end,
            args.pl_items,
            args.ytdl_config
        )

        # Check if data is actually returned
        if songs is None:
            logger.critical("Couldn't extract playlist data!")

        logger.info("Playlist: {}".format(playlist_name))
        logger.info("{} songs found".format(len(songs)))

        # Before passing the args, make the song name None
        # so that the song name will be extracted in main
        args.SONG_NAME = []

        # Iterate and work on the data.
        # NOTE: song["url"] will contain the URL all right, it won't be just
        # the href.
        for song in songs:
            args.url = song["url"]

            # Keep compatibility in case the url value changes back to href
            # in the future.
            if '/' not in args.url:
                args.url = f"https://www.youtube.com/watch?v={args.url}"

            main(args)
    else:
        main(args)


def entry():
    try:
        extract_data()
    except KeyboardInterrupt:
        logger.info("\nExiting..!")


if __name__ == '__main__':
    entry()
