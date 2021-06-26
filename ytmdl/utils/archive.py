"""
Handle the archive related feature.
"""

from pathlib import Path
from typing import List, Union
from simber import Logger
from io import TextIOWrapper

from ytmdl.yt import extract_video_id


# Create logger
logger = Logger("archive")


def open_archive_stream(file: str) -> Union[List, TextIOWrapper]:
    """
    Read the archive file and extract all the videoId's
    passed. This file will be read as text and should contain
    videoId's in each line.
    """
    file_path: Path = Path(file).expanduser()

    # Check if the file exists
    if not file_path.exists():
        logger.critical("Passed archive file does not exist. Exiting!")

    stream: TextIOWrapper = file_path.open("r+")
    file_content: List = stream.read().split("\n")
    return file_content, stream


def is_present_in_archive(file_content: List, youtube_link: str) -> bool:
    """
    Check if the passed song is present
    in the download-archive file passed
    and accordingly return.
    """
    video_id: str = extract_video_id(youtube_link)

    return video_id in file_content


def add_song_to_archive(stream: TextIOWrapper, youtube_link: str) -> None:
    """
    Add the passed song to the archive file.

    This method is supposed to be called when the song
    is considered `worked on` and not just when the song
    is just downloaded.
    """
    video_id: str = extract_video_id(youtube_link)

    # Go to the end of the file
    stream.seek(0, 2)
    stream.write(f"\n{video_id}")
