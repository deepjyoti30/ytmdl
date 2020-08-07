<div align="center">
  <img src=".github/ytmdl.png">
</div>

<div align="center">
<h1>YouTube Music Downloader</h1>
<h4>Download songs from YouTube by getting the audio from YouTube and the metadata from sources like Itunes and Gaana.</h4>
</div>

<div align="center" width="80%" height="auto">
    <img src=".github/ytmdl.gif">
</div>


<div align="center">

<br/>
<a href="#why-this">Why this?</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#support-the-project">Support the Project</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#prerequisites">Prerequisites</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#setup">Setup</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#usage">Usage</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#change-defaults">Change Defaults</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#acknowledgements">Acknowledgements</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#need-help">Need Help</a>&nbsp;&nbsp;&nbsp;
<br/>
</div>

<div align="center">

<br/>

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)<br/><br/>
<img src="https://img.shields.io/badge/Maintained%3F-Yes-blueviolet?style=for-the-badge">
![Travis (.org)](https://img.shields.io/travis/deepjyoti30/ytmdl?style=for-the-badge) [![License](https://img.shields.io/badge/License-MIT-pink.svg?style=for-the-badge)](LICENSE.md) ![PyPI](https://img.shields.io/pypi/v/ytmdl?style=for-the-badge) ![AUR](https://img.shields.io/aur/version/ytmdl?color=red&style=for-the-badge) ![PyPI - Downloads](https://img.shields.io/pypi/dm/ytmdl?style=for-the-badge) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-lightblue.svg?style=for-the-badge)](http://makeapullrequest.com) [![Telegram](https://img.shields.io/badge/Telegram-YTMDL-blue.svg?style=for-the-badge)](https://t.me/ytmdl)

<p>
<a href="https://ko-fi.com/deepjyoti30"><img src="https://raw.githubusercontent.com/adi1090x/files/master/other/kofi.png" alt="Support me on ko-fi"></a>
</p>
</div>

## Why this?

This app downloads a song by getting the audio from Youtube sources __using__ youtube-dl and then adds song information like
artist name, album name, release date, thumbnail etc by fetching it from sources like Itunes and Gaana.

__NO__. YoutubeDL doesn't do that. All youtube-dl does is lets you download audio from a video that you specify.
__This app is not yet another youtube-dl clone.__

## Support the Project?

If you like my work, consider buying me a coffee or donating. In case you want to become a patron, join my [Pateron](https://www.patreon.com/deepjyoti30)

<p align="left">
<a href="https://www.paypal.me/deepjyoti30" target="_blank"><img alt="undefined" src="https://img.shields.io/badge/paypal-deepjyoti30-blue?style=for-the-badge&logo=paypal"></a>
<a href="https://www.patreon.com/deepjyoti30" target="_blank"><img alt="undefined" src="https://img.shields.io/badge/Patreon-deepjyoti30-orange?style=for-the-badge&logo=patreon"></a>
<a href="https://ko-fi.com/deepjyoti30" target="_blank"><img alt="undefined" src="https://img.shields.io/badge/KoFi-deepjyoti30-red?style=for-the-badge&logo=ko-fi"></a>
</p>

## Prerequisites

 * Python 3.x
 * ffmpeg  

## Setup

 - [PyPi](#pypi)
 - [AUR](#aur)
 - [Gentoo](#gentoo)
 - [Manual](#manual)

    ## PyPi

      Available in **PyPi** [here](https://pypi.org/project/ytmdl/)

      ```sh
      pip install ytmdl
      ```

    ## AUR

      Available in **AUR** [here](https://aur.archlinux.org/packages/ytmdl/)

      ```sh
      yay -S ytmdl
      ```
    ## Gentoo

      Available in **src_prepare-overlay** [here](https://gitlab.com/src_prepare/src_prepare-overlay)

      ```sh
      # First set up src_prepare-overlay (as root)
      emerge -av --noreplace app-eselect/eselect-repository
      eselect repository enable src_prepare-overlay
      emaint sync -r src_prepare-overlay
      # Finally emerge ytmdl (as root)
      emerge -av --autounmask net-misc/ytmdl
      ```

    ## Manual

    - **Hate your stable life? Love living on the bleeding edge?**

        Clone the repo and install manually.

        ```sh
        git clone https://github.com/deepjyoti30/ytmdl && cd ytmdl && sudo python setup.py install
        ```
    

## Usage

```console
usage: ytmdl [-h] [-q] [--song SONG-METADATA] [--choice CHOICE]
             [--artist ARTIST] [--album ALBUM] [--disable-metaadd]
             [--skip-meta] [-m] [--proxy URL] [--url URL]
             [--list PATH TO LIST] [--nolocal] [--format FORMAT] [--trim]
             [--version] [--pl-start NUMBER] [--pl-end NUMBER]
             [--pl-items ITEM_SPEC] [--ignore-errors] [--level LEVEL]
             [--disable-file] [--list-level]
             [SONG_NAME [SONG_NAME ...]]

positional arguments:
  SONG_NAME             Name of the song to download. Can be an URL to a
                        playlist as well. It will be automatically recognized.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Don't ask the user to select songs if more than one
                        search result. The first result in each case will be
                        considered.
  --proxy URL           Use the specified HTTP/HTTPS/SOCKS proxy. To enable
                        SOCKS proxy, specify a proper scheme. For example
                        socks5://127.0.0.1:1080/. Pass in an empty string
                        (--proxy "") for direct connection
  --url URL             Youtube song link.
  --list PATH TO LIST   Download list of songs. The list should have one song
                        name in every line.
  --nolocal             Don't search locally for the song before downloading.
  --format FORMAT       The format in which the song should be downloaded.
                        Default is [MP3]. Available options are [m4a]
  --trim, -t            Trim out the audio from the song. Use underlying
                        speech and music segmentation engine to determine and
                        keep only the music in the file. Useful in songs where
                        there are speeches, noise etc before/after the start
                        of the song. Default is false.
  --version             show the program version number and exit

Metadata:
  --song SONG-METADATA  The song to search in Metadata. Particularly useful
                        for songs that have the names in a different language
                        in YouTube. For Example, greek songs.
  --choice CHOICE       The choice that the user wants to go for. Usefull to
                        pass along with --quiet. Choices start at 1
  --artist ARTIST       The name of the song's artist. Pass it with a song
                        name.
  --album ALBUM         The name of the song's album. Pass it with a song
                        name.
  --disable-metaadd     Disable addition of passed artist and album keyword to
                        the youtube search in order to get a more accurate
                        result. (Default: false)
  --skip-meta           Skip setting the metadata and just copy the converted
                        song to the destination directory. '--manual-meta'
                        will override this option, pass only one of them.
  -m, --manual-meta     Manually enter song details.

Playlist:
  --pl-start NUMBER     Playlist video to start at (default is 1)
  --pl-end NUMBER       Playlist video to end at (default is last)
  --pl-items ITEM_SPEC  Playlist video items to download. Specify indices of
                        the videos present in the playlist seperated by commas
                        like: '--playlist-items 1, 2, 4, 6' if you want to
                        download videos indexed 1, 2, 4 and 6. Range can also
                        be passed like: '--playlist-items 1-3, 5-7' to
                        download the videos indexed at 1, 2, 3, 5, 6, 7.
  --ignore-errors       Ignore if downloading any video fails in a playlist.
                        If passed, the execution will move to the next video
                        in the passed playlist.

Logger:
  --level LEVEL         The level of the logger that will be used while
                        verbosing. Use `--list-level` to check available
                        options.
  --disable-file        Disable logging to files
  --list-level          List all the available logger levels.

```

## Change Defaults

The defaults can be changed by editing the config file in ytmdl folder in your .config folder

>__NOTE__: The config will be created automatically the first time you run ```ytmdl``` and will be present in ```~/.config/ytmdl/config```

In case you want to create the config before the first run and edit it accordingly, do it the following way.

```console
mkdir -p ~/.config/ytmdl; curl https://raw.githubusercontent.com/deepjyoti30/ytmdl/master/config > ~/.config/ytmdl/config
```

This will download the default config from the repo to your ```~/.config/ytmdl``` directory.


### Supported options to change are:

| Name                 |                                                    |
|:--------------------:|----------------------------------------------------|
| `SONG_DIR`           | Directory to save the songs in after editing       |
| `SONG_QUALITY`       | Quality of the song                                |
| `METADATA_PROVIDERS` | Which API providers to use for metadata            |

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
 

## Need Help

Join the [Telegram group](https://t.me/ytmdl) for support.
