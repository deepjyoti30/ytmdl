"""
Handle ytdl related util methods.
"""

from os import path
from simber import Logger
from typing import Dict
from yt_dlp import parse_options

from ytmdl import utility


# Create logger
logger = Logger("yt")


def is_ytdl_config_present(path_passed: str) -> bool:
    """
    Check if the passed file is present or not.

    If the passed path is a directory, check if there is a
    `yt-dlp` file inside that directory.
    """
    # This can be changed to other name in case the package
    # name changes or the config name
    package_name = "yt-dlp"

    if path.isdir(path_passed):
        path_passed = path.join(path_passed, f"{package_name}.conf")

    logger.debug("Checking if path exists: ", path_passed)

    return path.exists(path_passed)


def ydl_opts_with_config(ytdl_config: str = None) -> Dict:
    """
    Generate the ydl_opts dictionary based on the passed config
    path.

    If the config is not present, return an empty dictionary
    """
    is_quiet: bool = utility.determine_logger_level(
    ) != logger.level_map["DEBUG"]
    no_warnings: bool = utility.determine_logger_level(
    ) > logger.level_map["WARNING"]

    ydl_opts = {
        "quiet": is_quiet,
        'no_warnings': no_warnings,
        'nocheckcertificate': True,
        'source_address': '0.0.0.0'
    }

    # If config is passed, generated opts with config
    if ytdl_config is not None:
        _, _, _, parsed_opts = parse_options(
            f"yt-dlp --config-locations {ytdl_config}".split())
        ydl_opts.update(parsed_opts)

    return ydl_opts
