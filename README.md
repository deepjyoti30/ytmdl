# YouTube Music Downloader

#### ytmdl in action

<p align="right">
  <a href="https://pypi.python.org/pypi/ytmdl/"><img src="https://img.shields.io/pypi/v/ytmdl.svg" alt="PyPi Version"/></a>
  <a href="https://pypi.python.org/pypi/ytmdl/"><img src="https://pypip.in/py_versions/ytmdl/badge.svg" alt="PyPI Python Versions"/></a>
  <a href="https://github.com/deepjyoti30/ytmdl/blob/master/LICENSE"><img src="https://img.shields.io/github/license/deepjyoti30/ytmdl.svg" alt="License"/></a>
</p>

![GIF](https://i.imgur.com/YhEmZwo.gif)

1. [Prerequisites](#prerequisites)
2. [Important](#important)
3. [Setup](#setup)
4. [Usage](#usage)
5. [Change Defaults](#change-defaults)
6. [Acknowledgements](#acknowledgements)

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
