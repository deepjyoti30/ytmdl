
"""Definition of functions that are used to interact with youtube."""

import requests
import os
from urllib.parse import urlparse, parse_qs
import yt_dlp
from yt_dlp.utils import DownloadError
from re import match, sub
from ytmdl import defaults, utility, stringutils
from downloader_cli.download import Download
import traceback
from sys import stdout
from simber import Logger
from ytmdl.exceptions import ExtractError
from ytmdl.utils.ytmusic import get_title_from_ytmusic
from youtubesearchpython import VideosSearch
from typing import List
from ytmdl.utils.ytdl import ydl_opts_with_config


logger = Logger("yt")


def get_youtube_streams(url):
    """Get both audio & video stream urls for youtube using youtube-dl.

    PS: I don't know how youtube-dl does the magic
    """
    cli = "yt-dlp -g {}".format(url)
    output, error = utility.exe(cli)
    stream_urls = output.split("\n")

    url = stream_urls[1]
    return url


# Function to be called by ytdl progress hook.
def progress_handler(d):
    d_obj = Download('', '')

    if d['status'] == 'downloading':
        length = d_obj._get_terminal_length()
        time_left = d['eta']
        f_size_disp, dw_unit = d_obj._format_size(d['downloaded_bytes'])

        # Total bytes might not be always passed, sometimes
        # total_bytes_estimate is passed
        try:
            total_bytes = d['total_bytes']
        except KeyError:
            total_bytes = d['total_bytes_estimate']

        percent = d['downloaded_bytes'] / total_bytes * 100
        speed, s_unit, time_left, time_unit = d_obj._get_speed_n_time(
            d['downloaded_bytes'],
            0,
            cur_time=d['elapsed'] - 6
        )

        status = r"%-7s" % ("%s %s" % (round(f_size_disp), dw_unit))
        if d['speed'] is not None:
            speed, s_unit = d_obj._format_speed(d['speed'] / 1000)
            status += r"| %-3s " % ("%s %s" % (round(speed), s_unit))

        status += r"|| ETA: %-4s " % (
            "%s %s" %
            (round(time_left), time_unit))

        status = d_obj._get_bar(status, length, percent)
        status += r" %-4s" % ("{}%".format(round(percent)))

        stdout.write('\r')
        stdout.write(status)
        stdout.flush()


def dw_using_yt(link, proxy, song_name, datatype, no_progress=False, ytdl_config: str = None, dont_convert: bool = False):
    """
    Download the song using YTDL downloader and use downloader CLI's
    functions to be used to display a progressbar.

    The function will be called by using hooks.
    """
    if datatype == 'mp3' or datatype == 'opus':
        format_ = 'bestaudio/best'
    elif datatype == 'm4a':
        format_ = 'bestaudio[ext=m4a]'

    extra_opts = {
        'outtmpl': song_name,
        'format': format_,
    }

    # Add a postprocessor to convert the audio into
    # opus if dont_convert is passed.
    #
    # Idea is to convert the audio through yt-dlp instead
    # of using ffmpeg which is the format ytmdl uses.
    #
    # Replace `.opus` with `.webm` from the file since otherwise
    # yt-dlp thinks that the file is converted.
    if datatype == "opus" and dont_convert:
        extra_opts["postprocessors"] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': "best",
            'preferredquality': '5',
            'nopostoverwrites': True,
        }]
        extra_opts["outtmpl"] = song_name.replace(".opus", ".webm")

    ydl_opts = ydl_opts_with_config(ytdl_config)
    ydl_opts.update(extra_opts)

    if not no_progress:
        logger.debug("Enabling progress hook.")
        logger.debug(f"Passed value for no_progress: {no_progress}")
        ydl_opts['progress_hooks'] = [progress_handler]

    if proxy is not None:
        ydl_opts['proxy'] = proxy

    logger.debug("args passed: ", str(ydl_opts))
    ydl = yt_dlp.YoutubeDL(ydl_opts)

    try:
        ydl.download([link])
        return 0
    except Exception as e:
        logger.warning("{}".format(e))
        return e


def dw(
        value,
        proxy=None,
        song_name='ytmdl_temp.mp3',
        datatype='mp3',
        no_progress=False,
        ytdl_config: str = None,
        dont_convert: bool = False
):
    """
    Download the song.

    The song can be downloaded in various types.

    Default type is mp3 as ytmdl was solely designed to download
    MP3 songs, however due to user requests other formats are
    added.
    """
    # If song_name doesn't have mp3 extension, add it
    if (datatype == "mp3" or datatype == "opus") and not song_name.endswith(datatype):
        song_name += '.' + datatype
    elif datatype == "m4a" and not song_name.endswith(datatype):
        song_name += '.' + datatype

    try:
        # Replace the spaces with hashes
        song_name = stringutils.remove_unwanted_chars(song_name)

        # The directory where we will download to.
        dw_dir = defaults.DEFAULT.SONG_TEMP_DIR
        logger.info("Saving the files to: {}".format(dw_dir))

        if not os.path.exists(dw_dir):
            os.makedirs(dw_dir)

        # Name of the temp file
        name = os.path.join(dw_dir, song_name)
        logger.debug(name)

        # Start downloading the song
        status = dw_using_yt(value, proxy, name, datatype,
                             no_progress, ytdl_config, dont_convert)

        if status == 0:
            return name
        else:
            return status

    except Exception as e:
        # traceback.print_exception(e)
        return e


def get_href(url):
    """Get the watch? part of the url in case of urls."""
    queries = parse_qs(urlparse(url=url).query)

    if 'v' not in queries:
        raise ExtractError(url)

    part = f"/watch?v={queries['v'][0]}"
    return part


def _is_verified(desc: List) -> bool:
    """Determine if the music video is provided
    by the music company to YouTube or not.

    In other words, this will just indicate if the
    song is directly provided by the music producer.

    This can be determined in a few ways.

    - If the desc contains `Auto-Generated by YouTube`
    - If the desc contains `Provided to YouTube by <company>`
    """
    if desc is None:
        return False

    desc = desc[0]["text"]
    return bool(match(r'^provided.to.youtube.by.*|^auto.generated.by.youtube', desc.lower()))


def search(query, bettersearch, proxy, kw=[], lim=20):
    """
    Search the song name and return results

    Search the passed query using the `youtube_search` module
    and extract the results accordingly and return.
    """
    # Remove any `plus` in the query
    if '+' in query:
        query = sub(r'\+\s?', '', query)
    logger.debug('Query used: ', query)

    # Add keywords if better search is enabled
    kw = [kw_ for kw_ in kw if kw_ is not None]

    if bettersearch and len(kw):
        query += '+' + '+'.join(kw)

    # Check if proxy is passed.
    proxies = {}
    if proxy is not None:
        proxies['http'] = proxies['https'] = proxy

    # Replace all the spaces with +
    query = query.replace(' ', '+')

    results = VideosSearch(query, limit=lim).result()["result"]

    if not results:
        logger.warning("No search results found!")

    stripped_results = []

    for video in results:
        data = {}
        data['title'] = video['title']
        data['href'] = f"/watch?v={video['id']}"
        data['author_name'] = video['channel']["name"]
        data['duration'] = video['duration']
        data['verified_music'] = _is_verified(video['descriptionSnippet'])

        stripped_results.append(data)

    return stripped_results


def scan_video(url, proxy):
    """Scan the link of the video and return data and."""
    proxies = {}
    if proxy is not None:
        proxies['http'] = proxy
    try:
        search_tmplt = "https://www.youtube.com/oembed?url={}&format=json"
        search_url = search_tmplt.format(url)
        r = requests.get(search_url, proxies=proxies)

        if r.status_code == 200:
            return r.json()
        else:
            return "Unauthorized"

    except Exception:
        return False


def is_playlist(url):
    """
    Check if the passed URL is a youtube playlist
    URL.
    """
    playlist_part = r"https?://(www\.|music\.)?youtube\.com/playlist\?list=.*?$"
    return match(playlist_part, url)


def is_yt_url(url):
    """
    Check if the passed URL is a valid youtube URL.
    """
    yt_url = r"https?://(www\.|music\.)?youtube\.com/watch\?v=.*?$"
    return match(yt_url, url)


def get_playlist(
    url,
    proxy,
    playlist_start=None,
    playlist_end=None,
    playlist_items=None,
    ytdl_config: str = None
):
    """
    Extract the playlist data and return it accordingly.

    The return result will be a dictionary with the following
    entries
    _type: Type of the entity returned.
    url  : URL of the video
    title: Title of the video.
    """
    ydl_opts = ydl_opts_with_config(ytdl_config=ytdl_config)

    extra_opts = {
        'format': 'bestaudio/best',
        'dump_single_json': True,
        'extract_flat': True,
    }
    ydl_opts.update(extra_opts)

    if proxy is not None:
        ydl_opts['proxy'] = proxy
    if playlist_start is not None:
        ydl_opts['playliststart'] = playlist_start
    if playlist_end is not None:
        ydl_opts['playlistend'] = playlist_end
    if playlist_items is not None:
        ydl_opts['playlist_items'] = playlist_items

    # Extract the info now
    songs = yt_dlp.YoutubeDL(ydl_opts).extract_info(url, False)

    # Put another check to see if the passed URL is a playlist
    try:
        if songs["_type"] != "playlist":
            logger.warning("Passed URL is not a playlist URL")
            return None
    except KeyError:
        pass

    # Return the songs now.
    try:
        return songs["entries"], songs["title"]
    except KeyError:
        logger.warning(
            "Something went wrong while extracting the playlist data."
        )
        return None, None


def __get_title_from_yt(url, ytdl_config: str = None):
    """
    Return the title of the passed URL.
    """
    ydl_opts = ydl_opts_with_config(ytdl_config=ytdl_config)

    logger.debug(url)

    ydl = yt_dlp.YoutubeDL(ydl_opts)

    try:
        data = ydl.extract_info(url, False)
        return stringutils.remove_yt_words(data["title"])
    except DownloadError:
        raise ExtractError(url)
    except KeyError:
        logger.error("Wasn't able to extract the name of the song.")
        return ""


def extract_video_id(url: str) -> str:
    """
    Extract the video ID from the URL.
    """
    try:
        return parse_qs(urlparse(url=url).query)["v"][0]
    except KeyError:
        raise ExtractError(url)


def get_title(url, ytdl_config: str = None) -> str:
    """
    Try to get the title of the song.

    This is mostly used when URL is passed or playlist
    links are passed since in those cases the title is
    not explicitly passed.
    """
    # Primarily try to get the title by using Youtube
    # Music.

    # If to verify the title from the user
    verify_title = False

    try:
        title = get_title_from_ytmusic(extract_video_id(url=url))
        return title, verify_title
    except ExtractError:
        logger.debug(f"YtMusic wasn't able to find title for {url}")
        pass

    # Try Youtube as a fallback
    verify_title = True
    title = __get_title_from_yt(url, ytdl_config)
    return title, verify_title


def get_chapters(url, ytdl_config: str = None):
    """Get the chapters of the passed URL.
    """
    ydl_opts = ydl_opts_with_config(ytdl_config=ytdl_config)

    info = yt_dlp.YoutubeDL(ydl_opts).extract_info(url, False)

    return info.get("chapters", None)


if __name__ == '__main__':
    print(defaults.DEFAULT.SONG_QUALITY)
