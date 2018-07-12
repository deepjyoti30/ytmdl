# YouTube Music Downloader

#### ytmdl in action

[![screenshot](https://i.imgur.com/whdtw8l.png)](https://i.imgur.com/whdtw8l.png)

1. [Prerequisites](#prerequisites)
2. [Important](#important)
3. [Setup](#setup)
4. [Usage](#usage)
5. [Change Defaults](#change-defaults)
6. [Acknowledgements](#acknowledgements)

## Prerequisites

 * Python 3.x

## Important
#### _After every clone please run the following in order to update the config file with the changes._

```sh
python setupConfig.py
```

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

# Copy the config
python setupConfig.py
```

### Windows


 * Download the zip and extract it.

 * Open cmd in the extracted folder and run the following command

 ```sh
    pip install -r requirements.txt

    # Copy the config
    python setupConfig.py
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
  -q, --quiet  Do not ask the user to select songs if more than one search
               result. The first result in each case will be considered.
  --url URL    Youtube song link.

```

## Change Defaults

#### The defaults can be changed by editing the config file in ytmdl folder in your .config folder

### Supported options to change are:

| Name           |                                                    |
|:--------------:|----------------------------------------------------|
| `SONG_DIR`     | Directory to save the songs in after editing       |
| `SONG_QUALITY` | Quality of the song                                |

#### SONG_DIR now takes values that are extracted from the song
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

 * Thanks to <a href = https://github.com/biswaroop1547>Biswaroop</a> for testing in windows.
