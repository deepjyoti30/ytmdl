"""
Handle metadata extraction from youtube
"""

from typing import Dict, List
from datetime import datetime

from yt_dlp import YoutubeDL
from simber import Logger

from ytmdl.manual import Meta
from ytmdl.utils.ytdl import get_ytdl_opts
from ytmdl.exceptions import ExtractError

# Create logger
logger = Logger("meta:yt")


def __parse_release_date_from_utc(timestamp: int) -> str:
    if timestamp is None:
        return None
    
    dt_object = datetime.utcfromtimestamp(timestamp)
    return dt_object.strftime('%Y-%m-%dT%H:%M:%SZ')

def __parse_genre_name_from_categories(categories: List[str]) -> str:
    return categories[0] if len(categories) else "N/A"

def __parse_meta_from_details(details: Dict) -> Meta:
    """
    Parse the meta object from the passed details
    """
    return Meta(
        release_date=__parse_release_date_from_utc(details.get("release_timestamp", None)),
        track_name=details.get("title", "N/A"),
        artist_name=details.get("channel", "N/A"),
        primary_genre_name=__parse_genre_name_from_categories(details.get("categories", [])),
        artwork_url_100=details.get("thumbnail", "N/A")
    )

def extract_meta_from_yt(video_url: str) -> Meta:
    """
    Extract the metadata from the passed video ID and return
    it accordingly.
    """
    ytdl_obj = YoutubeDL(get_ytdl_opts())
    
    try:
        details = ytdl_obj.extract_info(video_url, download=False)
        return __parse_meta_from_details(details)
    except Exception as e:
        logger.debug("Got exception while extracting details for video: ", video_url)
        logger.warning("Failed to extract metadata from yt with exception: ", str(e))
        raise ExtractError(f"error extracting data from yt: {str(e)}")
