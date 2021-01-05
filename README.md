# movieman

A python script that to manage your movie folder. (Only tested on Windows)

## Features

- Automatically move recently watched movies to another folder.

- Automatically download subtitles for movies using Subliminal.

- Automatically rename your movie folder, movie file and subtitle file so that instead of having a name like this
        Another.Round.2020.720p.WEBRip.800MB.x264-GalaxyRG\[TGx]
  the name will be like this
        Another Round (2020)

## Prerequisites

[Python 3.x](https://www.python.org/downloads/)

[MKVToolNix](https://mkvtoolnix.download/downloads.html#windows)

[VLC Media Player](https://www.videolan.org/vlc/)

[QBitTorrent](https://www.qbittorrent.org/download.php)

## Instructions

### General Instructions

Ensure that you use VLC media player to watch your movies. This application cannot detect movies that have been watched on
any other media player.

Ensure that you're using qBitTorrent as your torrent client. If your torrent client has a feature to dump finished torrent files into a specified folder then this may work as well. Add DUMP_PATH varaible accordingly.

### Installation Instructions

    git clone https://www.github.com/lemonnuggets/movieman.git
    cd movieman
    pip install -r requirements.txt

### Set-Up Instructions

Make sure the #Prerequisites are installed.

Add the following environment variables to a .env file in the same folder as movieman.py.

    VLC_HIST_FOLDER="Path to folder that opens up when you press Win+R, and run '%APPDATA%\vlc'"
    DUMP_PATH="Path to a folder for QBitTorrent to dump torrent files into"
    THUMBNAILS_FOLDER="Path to the folder where your movie thumbnails are stored"
    TO_WATCH_FOLDER="Path to folder where you keep movies that are yet to be watched"
    WATCHED_FOLDER="Path to folder where you keep the movies that you have watched already"

An example .env file would contain values looking something like this

    VLC_HIST_FOLDER="C:/Users/{username}/AppData/Roaming/vlc"
    DUMP_PATH="C:/Users/{username}/OneDrive/Desktop/ProgrammingStuff/python/movieman/dump"
    THUMBNAILS_FOLDER="C:/Users/{username}/Videos/.MOVIES/title-screens"
    TO_WATCH_FOLDER="C:/Users/{username}/Videos/.MOVIES/to-watch"
    WATCHED_FOLDER="C:/Users/{username}/Videos/.MOVIES/watched"

Go to qBitTorrent > Tools > Options > Downloads and check "Copy .torrent files for finished downloads to" and set the destination folder to same path as DUMP_PATH from your .env file.

Make movieman.py run at start up.

## Thanks

[Jorti's extract-subs](https://github.com/jorti/extract-subs)

[Subliminal](https://pypi.org/project/subliminal/)

[Watchdog](https://pypi.org/project/watchdog/)

## TODO

- [X] Automatically move movie that user has watched from to-watch/ folder to watched/ folder

- [X] When movies are downloaded, check if subtitles are there. If not then download subtitles.

- [X] Automatically rename movies, folders and subtitles to a uniform format {Name of movie (<year of release>)}.ext}

- [ ] When a .png file is added to the titlescreens folder automatically make it the directory icon of the appropriate movie.

- [ ] Set environment variables interactively by running the script with a ```--set-config``` flag

