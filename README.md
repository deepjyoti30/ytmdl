<div align="center">
<h1>YouTube Music Downloader</h1>
</div>

<div align="center" width="80%" height="auto">
    <img src=".github/ytmdl.gif">
</div>


<!--p align="center">
  <a href="https://pypi.python.org/pypi/ytmdl/"><img src="https://img.shields.io/pypi/v/ytmdl.svg" alt="PyPi Version"/></a>
  <a href="https://pypi.python.org/pypi/ytmdl/"><img src="https://pypip.in/py_versions/ytmdl/badge.svg" alt="PyPI Python Versions"/></a>
  <a href="https://github.com/deepjyoti30/ytmdl/blob/master/LICENSE"><img src="https://img.shields.io/github/license/deepjyoti30/ytmdl.svg" alt="License"/></a>
</p-->

<div align="center">

<br/>
<a href="#prerequisites">Prerequisites</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#setup">Setup</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#usage">Usage</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#change-defaults">Change Defaults</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#acknowledgements">Acknowledgements</a>&nbsp;&nbsp;&nbsp;
<br/>
</div>

<div align="center">

<br/>

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)<br/><br/>
![Travis (.org)](https://img.shields.io/travis/deepjyoti30/ytmdl?style=for-the-badge) [![License](https://img.shields.io/badge/License-MIT-pink.svg?style=for-the-badge)](LICENSE.md) ![PyPI](https://img.shields.io/pypi/v/ytmdl?style=for-the-badge) ![PyPI - Downloads](https://img.shields.io/pypi/dm/ytmdl?style=for-the-badge) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-lightblue.svg?style=for-the-badge)](http://makeapullrequest.com)

<!--[![Build Status][img-travis-ci]][Passing]&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[![GitHub release](https://img.shields.io/github/release/Naereen/StrapDown.js.svg)](https://GitHub.com/Naereen/StrapDown.js/releases/)[![PRs Welcome][prs-badge]][prs]-->


</div>


## Prerequisites

 * Python 3.x
 * ffmpeg  

## Setup

### Linux

Available in **AUR** [here](https://aur.archlinux.org/packages/ytmdl/)

```sh
yay -S ytmdl
```

Available in **PyPi** [here](https://pypi.org/project/ytmdl/)


```sh
pip install ytmdl
```


## Usage

```console

usage: ytmdl [-h] [-q] [--choice CHOICE] [--artist ARTIST] [--album ALBUM]
             [--version] [--url URL] [--disable-metaadd] [-s] [--list LIST]
             [--nolocal]
             SONG_NAME [SONG_NAME ...]

positional arguments:
  SONG_NAME          Name of the song to download.

optional arguments:
  -h, --help         show this help message and exit
  -q, --quiet        Don't ask the user to select songs if more than one
                     search result. The first result in each case will be
                     considered.
  --choice CHOICE    The choice that the user wants to go for. Usefull to pass
                     along with --quiet. Choices start at 1
  --artist ARTIST    Name of the artist
  --album ALBUM      Name of the album.
  --version          show the program version number and exit
  --url URL          Youtube song link.
  --disable-metaadd  Disable addition of passed artist and album keyword to
                     the youtube search in order to get a more accurate
                     result. (Default: false)
  -s, --setup        Setup the config file
  --list LIST        Download list of songs. The list should have one song
                     name in every line.
  --nolocal          Dont search locally for the song before downloading.

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

#### Adding any tag at the end of the SONG_DIR between [] will be considerd the name of the song.
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
