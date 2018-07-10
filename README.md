# YouTube Music Downloader

## Description

### A simple cross platform script that gets the song from YouTube and the metadata from itunes.

### What you need to do?

### Pass song name. Yeah, thats it.

#### ytmdl in action

[![screenshot](https://i.imgur.com/whdtw8l.png)](https://i.imgur.com/whdtw8l.png)

## Prerequisites

 * Python 3.x

## Setup

### Linux

Run the following commands from you terminal  

```sh
# Clone the repo
git clone https://github.com/deepjyoti30/ytmdl

# Go to the directory
cd ytmdl

# Install dependencies.
pip install -r requirements.txt
```

### Windows


 * Download the zip and extract it.

 * Open cmd in the extracted folder and run the following command

 ```sh
    pip install -r requirements.txt
```

 * Download a zip from <a href = https://ffmpeg.zeranoe.com/>here.</a>

 * Extract.

 * Copy the three files in bin to C:\users\\{username}\appdata\local\programs\python\python36\scripts\


## Usage

```sh

usage: ytmdl.py [-h] [-q] SONG_NAME

positional arguments:
  SONG_NAME    Name of the song to download.

optional arguments:
  -h, --help   show this help message and exit
  -q, --quiet  Don't ask the user to select songs if more than one search
               result. The first result in each case will be considered.

```

## Change Defaults

#### The defaults can be changed by editing the config file in ytmdl folder in your Music Directory

** _Please Run once with the default settings to start using the config_ **

### OR

** _Copy the config file from the ytmdl folder to your Music/ytmdl folder_ **

### Supported options to change are:

| Name           |                                                    |
|:--------------:|----------------------------------------------------|
| `SONG_DIR`     | Directory to save the songs in after editing       |
| `SONG_QUALITY` | Quality of the song                                |

## Acknowledgements

 * Inspired from <a href = https://github.com/tterb/yt2mp3>https://github.com/tterb/yt2mp3</a>

 * Thanks to the developers of youtube-dl, itunespy, mutagen, colorama and Python.

 * Thanks to <a href = https://github.com/biswaroop1547>Biswaroop</a> for testing in windows.
