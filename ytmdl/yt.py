"""Definition of functions that are used to interact with youtube."""

from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import os
import youtube_dl
from ytmdl import defaults


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


video = []
urls = []


def get_href(url):
    """Get the watch? part of the url in case of urls."""
    pos_watch = url.index('/watch?v=')

    part = url[pos_watch:]

    return part


def search(querry, lim=5):
    """Search the querry in youtube and return lim number of results.

    Querry is the keyword, i:e name of the song
    lim is the number of songs that will be added to video array and returned
    """
    # Replace all the spaces with +
    querry = querry.replace(' ', '+')

    url = "https://www.youtube.com/results?search_query={}".format(querry)

    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    count = 0
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        if lim == count:
            break

        url = vid['href']

        try:
            data = scan_video(url)
        except Exception:
            # If something was wrong, append the last result and return
            video.append(data)
            urls.append(url)
            break

        video.append(data)
        urls.append(url)
        count += 1
    return (video, urls)


def scan_video(url):
    """Scan the link of the video and return data and."""
    search_tmplt = "http://www.youtube.com/oembed?url={}&format=json"
    search_url = search_tmplt.format(url)
    data = requests.get(search_url).json()

    return data
