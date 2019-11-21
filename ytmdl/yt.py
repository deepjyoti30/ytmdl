"""Definition of functions that are used to interact with youtube."""

import requests
from bs4 import BeautifulSoup
import os
import youtube_dl
import re
from ytmdl import defaults, utility
from downloader_cli.download import Download
import traceback

from ytmdl.logger import Logger


logger = Logger("yt")


def get_youtube_streams(url):
    """Get both audio & vidoe stream urls for youtube using youtube-dl.

    PS: I don't know how youtube-dl does the magic
    """
    cli = "youtube-dl -g {}".format(url)
    output, error = utility.exe(cli)
    stream_urls = output.split("\n")

    url = stream_urls[1]
    return url


def GRAB_SONG(link):
    """Return true if the song is downloaded else false."""
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'outtmpl': os.path.join(defaults.DEFAULT.SONG_TEMP_DIR,
                                '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec':  'mp3',
            'preferredquality': defaults.DEFAULT.SONG_QUALITY
        }]
    }

    # Download the song with youtube-dl
    try:
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        ydl.download([link])
        return True
    except TimeoutError:
        print('Timed Out! Are you connected to internet?\a')
        return False
    else:
        return False


def dw(value, song_name='ytmdl_temp.mp3'):
    """Download the song."""
    try:
        # Get the audio stream link
        url = get_youtube_streams(value)

        # If song_name doesnt have mp3 extension, add it
        if not song_name.endswith('.mp3'):
            song_name += '.mp3'

        # Replace the spaces with hashes
        song_name = song_name.replace(' ', '#')
        song_name = song_name.replace('/', '#')

        # The directory where we will download to.
        dw_dir = defaults.DEFAULT.SONG_TEMP_DIR
        logger.info("Saving the files to: {}".format(dw_dir))

        if not os.path.exists(dw_dir):
            os.makedirs(dw_dir)

        # Name of the temp file
        name = os.path.join(dw_dir, song_name)

        # Start downloading the song
        Download(url, name).download()

        return name
    except Exception as e:
        traceback.print_exception(e)
        return e


def get_href(url):
    """Get the watch? part of the url in case of urls."""
    pos_watch = url.index('/watch?v=')

    part = url[pos_watch:]

    return part


def search(querry, bettersearch, kw=[], lim=10):
    """Search the querry in youtube and return lim number of results.

    Querry is the keyword, i:e name of the song
    lim is the number of songs that will be added to video array and returned
    """

    # Add keywords if better search is enabled
    if bettersearch:
        for keyword in kw:
            if keyword is not None:
                querry += ' ' + keyword

    # Replace all the spaces with +
    querry = querry.replace(' ', '+')

    url = "https://www.youtube.com/results?search_query={}".format(querry)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    videos = soup.findAll('div', attrs={'class': 'yt-lockup-content'})

    if not videos:
        return []

    if len(videos) > lim:
        videos = videos[:lim]

    extracted_data = []

    for video in videos:
        a = video.find_all('a')
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


def scan_video(url):
    """Scan the link of the video and return data and."""
    try:
        search_tmplt = "http://www.youtube.com/oembed?url={}&format=json"
        search_url = search_tmplt.format(url)
        r = requests.get(search_url)

        if r.status_code == 200:
            return r.json()
        else:
            return "Unauthorized"

    except Exception:
        return False


if __name__ == '__main__':
    print(defaults.DEFAULT.SONG_QUALITY)
