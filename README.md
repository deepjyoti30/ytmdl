# YouTube Music Downloader

## Description

### A simple cross platform script that gets the song from YouTube and the metadata from itunes.

### What you need to do?

### Pass the url and the song name. Yeah, thats it.

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

# Move to directory first
python ytmdl.py [URL] [TITLE]

```

## Acknowledgements

 * Inspired from <a href = https://github.com/tterb/yt2mp3>https://github.com/tterb/yt2mp3</a>

 * Thanks to the developers of youtube-dl, itunespy, mutagen, colorama and Python.

 * Thanks to <a href = https://github.com/biswaroop1547>Biswaroop</a> for testing in windows.
