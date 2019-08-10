"""Definition of functions that are used to interact with youtube."""

import requests
from bs4 import BeautifulSoup
import os
import youtube_dl
from ytmdl import defaults, utility, download


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

        # Name of the temp file
        name = os.path.join(defaults.DEFAULT.SONG_TEMP_DIR, song_name)

        # Start downloading the song
        """response = requests.get(url, stream=True)
        with open(name, 'wb') as out_file:
            copyfileobj(response.raw, out_file)
        """
        download.download(url, name)

        return name
    except Exception:
        return False


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
    # Initialize some tuples
    video = []
    urls = []

    # Add keywords if better search is enabled
    if bettersearch:
        for keyword in kw:
            if keyword is not None:
                querry += ' ' + keyword

    # Replace all the spaces with +
    querry = querry.replace(' ', '+')

    url = "https://www.youtube.com/results?search_query={}".format(querry)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    count = 0
    videos = soup.findAll('a', attrs={'class': 'yt-uix-tile-link'})

    for vid in videos:
        if lim == count:
            break

        url = vid['href']

        data = scan_video(url)

        if data == "Unauthorized":
            pass
        elif not data:
            break
        else:
            video.append(data)
            urls.append(url)
            count += 1

    return (video, urls)


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
