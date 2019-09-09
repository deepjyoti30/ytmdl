<div align="center">
<h1>YouTube Music Downloader</h1>
</div>

<div align="center">
    <!--img src='https://i.imgur.com/YhEmZwo.gif'-->
    <img src="ytmdl.gif">
</div>


<!--p align="center">
  <a href="https://pypi.python.org/pypi/ytmdl/"><img src="https://img.shields.io/pypi/v/ytmdl.svg" alt="PyPi Version"/></a>
  <a href="https://pypi.python.org/pypi/ytmdl/"><img src="https://pypip.in/py_versions/ytmdl/badge.svg" alt="PyPI Python Versions"/></a>
  <a href="https://github.com/deepjyoti30/ytmdl/blob/master/LICENSE"><img src="https://img.shields.io/github/license/deepjyoti30/ytmdl.svg" alt="License"/></a>
</p-->

<div align="center">

<br/>
<a href="#prerequisites">Prerequisites</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#important">Important</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#setup">Setup</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#usage">Usage</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#change-defaults">Change Defaults</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#acknowledgements">Acknowledgements</a>&nbsp;&nbsp;&nbsp;

</div>

<div align="center">

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)<br/><br/>
![Travis (.org)](https://img.shields.io/travis/deepjyoti30/ytmdl?style=for-the-badge) [![License](https://img.shields.io/badge/License-MIT-pink.svg?style=for-the-badge)](LICENSE.md) ![PyPI](https://img.shields.io/pypi/v/ytmdl?style=for-the-badge) ![PyPI - Downloads](https://img.shields.io/pypi/dm/ytmdl?style=for-the-badge) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-lightblue.svg?style=for-the-badge)](http://makeapullrequest.com)

<!--[![Build Status][img-travis-ci]][Passing]&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[![GitHub release](https://img.shields.io/github/release/Naereen/StrapDown.js.svg)](https://GitHub.com/Naereen/StrapDown.js/releases/)[![PRs Welcome][prs-badge]][prs]-->


</div>


## Prerequisites

 * Python 3.x
 * ffmpeg  

## Important
#### _After every update run the following._

```sh
ytmdl -s
```

## Setup

### Linux

Run the following commands from you terminal  

```sh
# Install ffmpeg
sudo apt-get install ffmpeg

# Install ytmdl
sudo pip install ytmdl

# Setup the config file
ytmdl -s
```

### Windows

 * Download the repo and extract it.

 * Run the following in cmd

 ```sh
    # Copy the config
    python ytmdl.py -s
```

 * Download ffmpeg from <a href = https://ffmpeg.zeranoe.com/>here.</a>

 * Extract.

 * Copy the three files in bin to C:\users\\{username}\appdata\local\programs\python\python36\scripts\


## Usage

```sh

usage: ytmdl [-h] [-q] [--version] [--url URL] [-s] [-l LIST] [--nolocal]
                [SONG_NAME]

positional arguments:
  SONG_NAME             Name of the song to download.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Dont ask the user to select songs if more than one
                        search result. The first result in each case will be
                        considered.
  --version             show the program version number and exit
  --url URL             Youtube song link.
  -s, --setup           Setup the config file
  -l LIST, --list LIST  Download list of songs. The list should have one song
                        name in every line.
  --nolocal             Dont search locally for the song before downloading.


```

_In case of windows, use ```python ytmdl.py``` instead of ```ytmdl``` above_

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
