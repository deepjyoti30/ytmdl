"""Definition of functions that are used to interact with youtube."""

import requests
from bs4 import BeautifulSoup
import os
import youtube_dl
import re
from ytmdl import defaults, utility, stringutils
from downloader_cli.download import Download
import traceback
from sys import stdout

from ytmdl.logger import Logger


logger = Logger("yt")


def get_youtube_streams(url):
    """Get both audio & video stream urls for youtube using youtube-dl.

    PS: I don't know how youtube-dl does the magic
    """
    cli = "youtube-dl -g {}".format(url)
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


def dw_using_yt(link, proxy, song_name, datatype):
    """
    Download the song using YTDL downloader and use downloader CLI's
    functions to be used to display a progressbar.

    The function will be called by using hooks.
    """
    if datatype == 'mp3':
        format_ = 'bestaudio/best'
    elif datatype == 'm4a':
        format_ = 'bestaudio[ext=m4a]'

    ydl_opts = {
        'quiet': True,
        'outtmpl': song_name,
        'format': format_,
        'nocheckcertificate': True,
        'progress_hooks': [progress_handler],
    }

    if proxy is not None:
        ydl_opts['proxy'] = proxy

    ydl = youtube_dl.YoutubeDL(ydl_opts)

    try:
        ydl.download([link])
        return 0
    except Exception as e:
        logger.warning("{}".format(e))
        return e


def dw(value, proxy=None, song_name='ytmdl_temp.mp3', datatype='mp3'):
    """
    Download the song.

    The song can be downloaded in various types.

    Default type is mp3 as ytmdl was solely designed to download
    MP3 songs, however due to user requests other formats are
    added.
    """
    # If song_name doesn't have mp3 extension, add it
    if datatype == "mp3" and not song_name.endswith(datatype):
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
        status = dw_using_yt(value, proxy, name, datatype)

        if status == 0:
            return name
        else:
            return status

    except Exception as e:
        # traceback.print_exception(e)
        return e


def get_href(url):
    """Get the watch? part of the url in case of urls."""
    pos_watch = url.index('/watch?v=')

    part = url[pos_watch:]

    return part


def search(query, bettersearch, proxy, kw=[], lim=10):
    """Search the query in youtube and return lim number of results.

    Query is the keyword, i:e name of the song
    lim is the number of songs that will be added to video array and returned
    """

    # Add keywords if better search is enabled
    if bettersearch:
        for keyword in kw:
            if keyword is not None:
                query += ' ' + keyword

    # Check if proxy is passed.
    proxies = {}
    if proxy is not None:
        proxies['http'] = proxy

    # Replace all the spaces with +
    query = query.replace(' ', '+')

    url = "https://www.youtube.com/results?search_query={}".format(query)
    videos = []

    try:
        response = requests.get(url, proxies=proxies)
        soup = BeautifulSoup(response.text, "lxml")
        videos = soup.findAll('div', attrs={'class': 'yt-lockup-content'})
    except requests.exceptions.ConnectionError:
        logger.critical("Connection Error! Are you connected to internet?")
    except requests.exceptions.Timeout:
        logger.critical("Timed Out! Are you connected to internet?")
    except Exception:
        traceback.print_exc()

    if not videos:
        return []

    if len(videos) > lim:
        videos = videos[:lim]

    extracted_data = []

    for video in videos:
        a = video.find_all('a')
        # This check is necessary because in some cases the search results
        # contain channel names etc.
        if len(a) <= 1: continue
        data = {}
        data['title'] = a[0]['title']
        data['href'] = a[0]['href']
        data['author_name'] = a[1].text
        duration_unprocessed = video.span.text
        duration = re.sub(r'\ |\-|\.|Duration', '', duration_unprocessed)
        data['duration'] = re.subn(r':', '', duration, 1)[0]

        extracted_data.append(data)

    return extracted_data


def scan_video(url, proxy):
    """Scan the link of the video and return data and."""
    proxies = {}
    if proxy is not None:
        proxies['http'] = proxy
    try:
        search_tmplt = "http://www.youtube.com/oembed?url={}&format=json"
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
    playlist_part = "https://www.youtube.com/playlist?list"
    if playlist_part in url:
        return True
    else:
        return False


def get_playlist(
            url,
            proxy,
            playlist_start=None,
            playlist_end=None,
            playlist_items=None
        ):
    """
    Extract the playlist data and return it accordingly.

    The return result will be a dictionary with the following
    entries
    _type: Type of the entity returned.
    url  : URL of the video
    title: Title of the video.
    """
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'nocheckcertificate': True,
        'dump_single_json': True,
        'extract_flat': True,
    }

    if proxy is not None:
        ydl_opts['proxy'] = proxy
    if playlist_start is not None:
        ydl_opts['playliststart'] = playlist_start
    if playlist_end is not None:
        ydl_opts['playlistend'] = playlist_end
    if playlist_items is not None:
        ydl_opts['playlist_items'] = playlist_items

    # Extract the info now
    songs = youtube_dl.YoutubeDL(ydl_opts).extract_info(url, False)

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
        return None


def get_title(url):
    """
    Return the title of the passed URL.
    """
    ydl_opts = {"quiet": True}
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    data = ydl.extract_info(url, False)

    try:
        return stringutils.remove_yt_words(data["title"])
    except KeyError:
        logger.error("Wasn't able to extract the name of the song.")
        return ""


if __name__ == '__main__':
    print(defaults.DEFAULT.SONG_QUALITY)
