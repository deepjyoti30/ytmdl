<div align="center">
  <img src=".github/ytmdl.png">
</div>

<div align="center">
<h1>YouTube Music Downloader</h1>
<h4>Download songs from YouTube by getting the audio from YouTube and the metadata from sources like Itunes, Spotify, Gaana etc.</h4>
</div>

<div align="center" width="60%" height="auto">
  <br>
    <img src=".github/ytmdl.gif">
</div>

<div align="center">

<br/>

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)<br/><br/>
<img src="https://img.shields.io/badge/Maintained%3F-Yes-blueviolet?style=for-the-badge">
![Travis (.org)](https://img.shields.io/travis/deepjyoti30/ytmdl?style=for-the-badge) ![[RepoStatus](https://repostatus.deepjyoti30.dev)](https://apis.deepjyoti30.dev/repostatus/badge?repo=deepjyoti30%2Fytmdl&style=for-the-badge) [![License](https://img.shields.io/badge/License-MIT-pink.svg?style=for-the-badge)](LICENSE.md) ![PyPI](https://img.shields.io/pypi/v/ytmdl?style=for-the-badge) ![AUR](https://img.shields.io/aur/version/ytmdl?color=red&style=for-the-badge) [![Downloads](https://img.shields.io/badge/dynamic/json?style=for-the-badge&maxAge=86400&label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fytmdl)](https://img.shields.io/badge/dynamic/json?style=for-the-badge&maxAge=86400&label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fytmdl) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-lightblue.svg?style=for-the-badge)](http://makeapullrequest.com) [![Telegram](https://img.shields.io/badge/Telegram-YTMDL-blue.svg?style=for-the-badge)](https://t.me/ytmdl)

<p>
<a href="https://ko-fi.com/deepjyoti30"><img src="https://raw.githubusercontent.com/adi1090x/files/master/other/kofi.png" alt="Support me on ko-fi"></a>
</p>

<br/>

### \[[Web App](#web-app)] \[[Why This?](#why-this)] \[[Support the Project](#support-the-project)] \[[Installation](#installation)] \[[Configuration](#configuration)] \[[WiKi](https://github.com/deepjyoti30/ytmdl/wiki/)]

<br/>
</div>

## Web App

Ytmdl also has an web app, you can try it out [here](https://ytmdl.deepjyoti30.dev/)

## Why this?

This app downloads a song by getting the audio from Youtube sources **using** youtube-dl and then adds song information like
artist name, album name, release date, thumbnail etc by fetching it from sources like Itunes, Spotify, Gaana and other sources.

**NO**. YoutubeDL doesn't do that. All youtube-dl does is lets you download audio from a video that you specify.
**This app is not yet another youtube-dl clone.**

## Support the Project?

Help the development of this project by becoming a backer or a sponsor.

### [Become a Backer](https://opencollective.com/ytmdl#backer)

### [Become a sponsor](https://opencollective.com/ytmdl#sponsor)

If you like my work, consider buying me a coffee or donating. In case you want to become a patron, join my [Pateron](https://www.patreon.com/deepjyoti30)

<p align="left">
<a href="https://www.paypal.me/deepjyoti30" target="_blank"><img alt="undefined" src="https://img.shields.io/badge/paypal-deepjyoti30-blue?style=for-the-badge&logo=paypal"></a>
<a href="https://www.patreon.com/deepjyoti30" target="_blank"><img alt="undefined" src="https://img.shields.io/badge/Patreon-deepjyoti30-orange?style=for-the-badge&logo=patreon"></a>
<a href="https://ko-fi.com/deepjyoti30" target="_blank"><img alt="undefined" src="https://img.shields.io/badge/KoFi-deepjyoti30-red?style=for-the-badge&logo=ko-fi"></a>
</p>

## Requirements

- Python 3.6.1
- ffmpeg

## Installation

- [PyPi](#pypi)
- [Arch Linux](#arch-linux)
- [Gentoo](#gentoo)
- [NixOS](#nixos)
- [Windows](#windows)
- [Manual](#manual)

### PyPI

```console
pip install ytmdl
```

> NOTE: System wide installation requires `sudo`

### Arch Linux

`ytmdl` is available in AUR as `ytmdl`. It can be found [here](https://aur.archlinux.org/packages/ytmdl/)

> NOTE: The git version is availble as `ytmdl-git` in AUR.

### Gentoo

`ytmdl` can be installed in Gentoo by the following commands

```console
# First set up src_prepare-overlay (as root)
emerge -av --noreplace app-eselect/eselect-repository
eselect repository enable src_prepare-overlay
emaint sync -r src_prepare-overlay
# Finally emerge ytmdl (as root)
emerge -av --autounmask net-misc/ytmdl
```

Available in **src_prepare-overlay** [here](https://gitlab.com/src_prepare/src_prepare-overlay)

### NixOS

`ytmdl` can be installed using Nix with the command

```console
nix-env -iA nixos.ytmdl
```

### Windows

You need to install `ffmpeg` in order for `ytmdl` to work properly. This can be done by downloading the `ffmpeg` binary from [here](https://ffmpeg.org/download.html). Once downloaded, extract the file and find the `ffmpeg.exe` file. Copy the directory's path and add it to PATH in the following way.

```console
setx path "%path%;C:\your\path\here\"
```

Once `ffmpeg` is installed, install `ytmdl` using the following command

```console
pip install ytmdl --upgrade
```

> NOTE: You'll need to have Python 3.6.1 or more installed.

Optionally, also install the latest version of `downloader-cli` and `simber` using the following command:

```console
pip install simber downloader-cli --upgrade
```

### Manual

You can manually install `ytmdl` by cloning this repository and running the `setup.py` script.

1. Install `setuptools` if it isn't already:

   ```console
    pip install setuptools
   ```

1. Clone this repo:

   ```console
   git clone https://github.com/deepjyoti30/ytmdl
   ```

1. Move into the `ytmdl` directory and run the `setup.py` script:

   ```console
   cd ytmdl
   sudo python setup.py install
   ```

## Usage

```console
usage: ytmdl [-h] [-q] [-o OUTPUT_DIR] [--song SONG-METADATA]
             [--choice CHOICE] [--artist ARTIST] [--album ALBUM]
             [--disable-metaadd] [--skip-meta] [-m] [--itunes-id ITUNES_ID]
             [--spotify-id SPOTIFY_ID] [--disable-sort] [--ask-meta-name]
             [--on-meta-error ON_META_ERROR] [--proxy URL] [--url URL]
             [--list PATH TO LIST] [--nolocal] [--format FORMAT] [--trim]
             [--version] [--keep-chapter-name] [--download-archive FILE]
             [--ignore-chapters] [--ytdl-config PATH] [--dont-transcode]
             [--filename NAME] [--pl-start NUMBER] [--pl-end NUMBER]
             [--pl-items ITEM_SPEC] [--ignore-errors] [--title-as-name]
             [--level LEVEL] [--disable-file] [--list-level]
             [SONG_NAME [SONG_NAME ...]]

positional arguments:
  SONG_NAME             Name of the song to download. Can be an URL to a
                        playlist as well. It will be automatically recognized.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Don't ask the user to select songs if more than one
                        search result. The first result in each case will be
                        considered.
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        The location for the song to be downloaded to. When no
                        argument is passed, the default locations of SONG_DIR
                        or XDG_MUSIC_DIR are used.
  --proxy URL           Use the specified HTTP/HTTPS/SOCKS proxy. To enable
                        SOCKS proxy, specify a proper scheme. For example
                        socks5://127.0.0.1:1080/. Pass in an empty string
                        (--proxy "") for direct connection
  --url URL             Youtube song link.
  --list PATH TO LIST   Download list of songs. The list should have one song
                        name in every line.
  --nolocal             Don't search locally for the song before downloading.
  --format FORMAT       The format in which the song should be downloaded.
                        Default is mp3, but can be set in config. Available
                        options are ['mp3', 'm4a', 'opus']
  --trim, -t            Trim out the audio from the song. Use underlying
                        speech and music segmentation engine to determine and
                        keep only the music in the file. Useful in songs where
                        there are speeches, noise etc before/after the start
                        of the song. Default is false.
  --version             show the program version number and exit
  --keep-chapter-name   Keep the title extracted from the chapter in order to
                        search for the metadata. If not passed, the user will
                        be asked if they'd like to change the title with which
                        the metadata will be searched.
  --download-archive FILE
                        Skip downloading songs that are present in the passed
                        file. The songs are matched by using the videoId. All
                        downloaded song Id's are automatically added to the
                        file.
  --ignore-chapters     Ignore chapters if available in the video and treat it
                        like one video
  --ytdl-config PATH    Path to the youtube-dl config location or the
                        directory
  --dont-transcode      Don't transcode the audio after downloading.
                        Applicable for OPUS format only. (Default: false)
  --filename NAME       Final filename after the song is ready to be used.
                        This will be given priority over automatic detection
                        unless dynamic filename path is set through config

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
  --itunes-id ITUNES_ID
                        Direct lookup from itunes. If passed, metadata will be
                        automatically added.
  --spotify-id SPOTIFY_ID
                        Direct lookup for Spotify tracks using the ID. If
                        passed, metadata will be automatically added.
  --disable-sort        Disable sorting of the metadata before asking for
                        input. Useful if the song is in some other language
                        and/or just a few providers are used.
  --ask-meta-name       Ask the user to enter a separate name for searching
                        the metadata (Default: false)
  --on-meta-error ON_META_ERROR
                        What to do if adding the metadata fails for some
                        reason like lack of metadata or perhaps a network
                        issue. Options are ['exit', 'skip', 'manual']

Playlist:
  --pl-start NUMBER     Playlist video to start at (default is 1)
  --pl-end NUMBER       Playlist video to end at (default is last)
  --pl-items ITEM_SPEC  Playlist video items to download. Specify indices of
                        the videos present in the playlist separated by commas
                        like: '--playlist-items 1, 2, 4, 6' if you want to
                        download videos indexed 1, 2, 4 and 6. Range can also
                        be passed like: '--playlist-items 1-3, 5-7' to
                        download the videos indexed at 1, 2, 3, 5, 6, 7.
  --ignore-errors       Ignore if downloading any video fails in a playlist.
                        If passed, the execution will move to the next video
                        in the passed playlist.
  --title-as-name       Use the title of the video as the name of the song to
                        search for metadata. If not passed, user will be asked
                        if they want to use a different name and continue
                        accordingly.

Logger:
  --level LEVEL         The level of the logger that will be used while
                        verbosing. Use `--list-level` to check available
                        options.
  --disable-file        Disable logging to files
  --list-level          List all the available logger levels.

```

## Configuration

### Setup

The defaults can be changed by editing the config file in ytmdl folder in your .config folder

The config will be created automatically the first time you run `ytmdl` and will be present in ~/.config/ytmdl/config

However, it can be created manually by the following command

```console
mkdir -p ~/.config/ytmdl; curl https://raw.githubusercontent.com/deepjyoti30/ytmdl/master/examples/config > ~/.config/ytmdl/config
```

Above command will download the config from the repo and save it in the `~/.config/ytmdl/` directory.

### Supported Options

As of the latest development branch, the following options can be changed from the config

|         Name         | Description                                      | Default                        |
| :------------------: | ------------------------------------------------ | ------------------------------ |
|      `SONG_DIR`      | Directory to save the songs in after editing     | Current directory              |
|    `SONG_QUALITY`    | Quality of the song                              | 320kbps                        |
| `METADATA_PROVIDERS` | Which API providers to use for metadata          | all supported options are used |
|   `DEFAULT_FORMAT`   | Default format of the song                       | mp3                            |
|   `ON_META_ERROR`    | What to do if error occurs while writing meta    | exit                           |
|   `ITUNES_COUNTRY`   | Which region to use while searching from Itunes  | US                             |
|  `SPOTIFY_COUNTRY`   | Which market to use while searching from Spotify | US                             |

### Advanced Configuration

#### Dynamically storing songs

`SONG_DIR` field also takes values that are extracted from the song being downloaded

The `SONG_DIR` field needs to be passed some special values in order to achieve that. The string is scanned and when a `$` sign occurs, the special string will start and each directory can be separated by using an `->` sign.

To save the song in the `/dir/<album_name>/<artist_name>/<title>/<song_name>.mp3` format, the following needs to be added in the `SONG_DIR` field.

```
SONG_DIR="/dir$Album->Artist->Title"
```

Above will extract to the following directory structure when a song named `Cradles` by artist `Sub Urban` from the album `Cradles - Single`

```
|--dir
   |--Cradles - Single
      |--Sub Urban
         |--Cradles
            |--Cradles.mp3
```

In order to pass the name with which the song should be saved, the last attribute can be passed between `[]`.

If the `SONG_DIR` field is `/dir$Album->[Artist]` will extract to the following directory structure

```
|--dir
   |--Cradles - Single
      |--Sub Urban.mp3
```

#### Supported options for dynamic storing

As of the latest source, the following options can be passed to the special string in order to create dynamic directories

|     Name      |                         |
| :-----------: | ----------------------- |
|   `Artist`    | Artist Of the Song      |
|    `Album`    | Album Of the Song       |
|    `Title`    | Title Of the Song       |
|    `Genre`    | Genre Of the Song       |
| `TrackNumber` | TrackNumber Of the Song |
| `ReleaseDate` | ReleaseDate Of the Song |
