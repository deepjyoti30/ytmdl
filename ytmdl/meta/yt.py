"""
Handle metadata extraction from youtube
"""

from typing import Dict

from yt_dlp import YoutubeDL
from simber import Logger

from ytmdl.manual import Meta
from ytmdl.utils.ytdl import get_ytdl_opts
from ytmdl.exceptions import ExtractError

# Create logger
logger = Logger("meta:yt")


def __parse_meta_from_details(details: Dict) -> Meta:
    """
    Parse the meta object from the passed details
    """
    return Meta(
        
    )

def extract_meta_from_yt(video_id: str) -> Meta:
    """
    Extract the metadata from the passed video ID and return
    it accordingly.
    """
    ytdl_obj = YoutubeDL(get_ytdl_opts())
    
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        details = ytdl_obj.extract_info(video_url, download=False)
    except Exception as e:
        logger.debug("Got exception while extracting details for video with ID: ", video_id)
        logger.warning("Failed to extract metadata from yt with exception: ", str(e))
        raise ExtractError(f"error extracting data from yt: {str(e)}")
