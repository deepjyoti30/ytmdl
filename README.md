<div align="center">
<h1>YouTube Music Downloader</h1>
</div>

<div align="center" width="80%" height="auto">
    <img src=".github/ytmdl.gif">
</div>


<div align="center">

<br/>
<a href="#prerequisites">Prerequisites</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#setup">Setup</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#usage">Usage</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#change-defaults">Change Defaults</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#acknowledgements">Acknowledgements</a>&nbsp;&nbsp;&nbsp;
<br/>
</div>

<div align="center">

<br/>

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)<br/><br/>
![Travis (.org)](https://img.shields.io/travis/deepjyoti30/ytmdl?style=for-the-badge) [![License](https://img.shields.io/badge/License-MIT-pink.svg?style=for-the-badge)](LICENSE.md) ![PyPI](https://img.shields.io/pypi/v/ytmdl?style=for-the-badge) ![AUR](https://img.shields.io/aur/version/ytmdl?color=red&style=for-the-badge) ![PyPI - Downloads](https://img.shields.io/pypi/dm/ytmdl?style=for-the-badge) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-lightblue.svg?style=for-the-badge)](http://makeapullrequest.com)

<!--[![Build Status][img-travis-ci]][Passing]&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[![GitHub release](https://img.shields.io/github/release/Naereen/StrapDown.js.svg)](https://GitHub.com/Naereen/StrapDown.js/releases/)[![PRs Welcome][prs-badge]][prs]-->


</div>


## Prerequisites

 * Python 3.x
 * ffmpeg  

## Setup

- **Hate your stable life? Love living on the bleeding edge?**

    Clone the repo and install manually.

    ```sh
    git clone https://github.com/deepjyoti30/ytmdl && cd ytmdl && sudo python setup.py install
    ```

- **Get the last released version?**

    Available in **AUR** [here](https://aur.archlinux.org/packages/ytmdl/)

    ```sh
    yay -S ytmdl
    ```

    Available in **PyPi** [here](https://pypi.org/project/ytmdl/)

    ```sh
    pip install ytmdl
    ```

    **Please install ffmpeg manually**

## Usage

```console
usage: ytmdl [-h] [-q] [--song SONG-METADATA] [--choice CHOICE] [--artist ARTIST]
             [--album ALBUM] [--disable-metaadd] [--proxy URL] [--url URL] [-s]
             [--list PATH TO LIST] [--nolocal] [--version] [--level LEVEL]
             [--disable-file] [--list-level]
             [SONG_NAME [SONG_NAME ...]]

positional arguments:
  SONG_NAME             Name of the song to download.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Don't ask the user to select songs if more than one search
                        result. The first result in each case will be considered.
  --proxy URL           Use the specified HTTP/HTTPS/SOCKS proxy. To enable SOCKS
                        proxy, specify a proper scheme. For example
                        socks5://127.0.0.1:1080/. Pass in an empty string (--proxy
                        "") for direct connection
  --url URL             Youtube song link.
  -s, --setup           Setup the config file
  --list PATH TO LIST   Download list of songs. The list should have one song name in
                        every line.
  --nolocal             Don't search locally for the song before downloading.
  --version             show the program version number and exit

Metadata:
  --song SONG-METADATA  The song to search in Metadata. Particularly useful for songs
                        that have the names in a different language in YouTube. For
                        Example, greek songs.
  --choice CHOICE       The choice that the user wants to go for. Usefull to pass
                        along with --quiet. Choices start at 1
  --artist ARTIST       The name of the song's artist. Pass it with a song name.
  --album ALBUM         The name of the song's album. Pass it with a song name.
  --disable-metaadd     Disable addition of passed artist and album keyword to the
                        youtube search in order to get a more accurate result.
                        (Default: false)

Logger:
  --level LEVEL         The level of the logger that will be used while verbosing.
                        Use `--list-level` to check available options.
  --disable-file        Disable logging to files
  --list-level          List all the available logger levels.

```

## Change Defaults

#### The defaults can be changed by editing the config file in ytmdl folder in your .config folder

### Supported options to change are:

| Name           |                                                    |
|:--------------:|----------------------------------------------------|
| `SONG_DIR`     | Directory to save the songs in after editing       |
| `SONG_QUALITY` | Quality of the song                                |

#### SONG_DIR also takes values that are extracted from the song
##### Example format is `/your/desired/path$Album->Artist->Title` to save in the following way

```sh
|--your
    |--desired
           |--path
                |--Album
                        |--Artist
                                |--Title
                                    |--Song.mp3
```

#### Adding any tag at the end of the SONG_DIR between [] will be considered the name of the song.
##### Example format is `/your/desired/path$Album->Artist->[Title]` to save in the following way

```sh
|--your
    |--desired
        |--path
            |--Album
                |--Artist
                    |--Title.mp3
```

Supported options are:

| Name          |                               |
|:-------------:|-------------------------------|
| `Artist`      | Artist Of the Song            |
| `Album`       | Album Of the Song             |
| `Title`       | Title Of the Song             |
| `Genre`       | Genre Of the Song             |
| `TrackNumber` | TrackNumber Of the Song       |
| `ReleaseDate` | ReleaseDate Of the Song       |


## Acknowledgements

 * Inspired from <a href = https://github.com/tterb/yt2mp3>https://github.com/tterb/yt2mp3</a>

 * Thanks to the developers of youtube-dl, itunespy, mutagen, colorama and Python.

 * Thanks to itunes and gaana for their awesome API's.

 * Thanks to <a href = https://github.com/NISH1001>Nishan Pantha</a> for search logic.

 * Thanks to <a href = https://github.com/biswaroop1547>Biswaroop</a> for testing in windows.
