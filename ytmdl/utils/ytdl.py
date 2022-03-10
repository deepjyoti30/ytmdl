"""
Handle ytdl related util methods.
"""

from os import path
from simber import Logger


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
