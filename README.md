# movieman

A python script that to manage your movie folder. (Only tested on Windows)

## Features

- Automatically move recently watched movies to another folder.

- Automatically download subtitles for movies using Subliminal.

- Automatically rename your movie folder, movie file and subtitle file so that instead of having a name like this

        Another.Round.2020.720p.WEBRip.800MB.x264-GalaxyRG[TGx]

  the name will be like this

        Another Round (2020)

- When a .png file is added to a movie folder in the to watch folder, this .png file is moved to the thumbnails folder and is also set as the icon of the movie directory.

## Prerequisites

[Python 3.x](https://www.python.org/downloads/)

[MKVToolNix](https://mkvtoolnix.download/downloads.html#windows)

[VLC Media Player](https://www.videolan.org/vlc/)

[QBitTorrent](https://www.qbittorrent.org/download.php)

## Instructions

### General Instructions

Ensure that you use VLC media player to watch your movies. This application cannot detect movies that have been watched on
any other media player.

Ensure that you're using qBitTorrent as your torrent client. If your torrent client has a feature to dump finished torrent files into a specified folder then this may work as well. Add DUMP_PATH variable accordingly.

### Installation Instructions

    git clone https://www.github.com/lemonnuggets/movieman.git
    cd movieman
    pip install -r requirements.txt

### Set-Up Instructions

Make sure the #Prerequisites are installed.

#### Automatic Setup

Run the setup.py file and give the required responses very carefully.

*SETUP.PY WILL NOT PROMPT YOU IF YOU MADE MISTAKES IN YOUR INPUTS.*

If you don't understand what the setup.py file is asking for look at the manual setup to get an idea of what values are required.

#### Manual Setup

Add the following environment variables to a .env file in the same folder as movieman.py.

    LOG_PATH="Path to folder where you want log files to be stored. Preferably create a log file in the directory where you've installed the script and put that path here."
    VLC_HIST_FOLDER="Path to folder that opens up when you press Win+R, and run '%APPDATA%\vlc'"
    DUMP_PATH="Path to a folder for QBitTorrent to dump torrent files into"
    THUMBNAILS_FOLDER="Path to the folder where your movie thumbnails are stored"
    TO_WATCH_FOLDER="Path to folder where you keep movies that are yet to be watched"
    WATCHED_FOLDER="Path to folder where you keep the movies that you have watched already"
    OPENSUBTITLES_USERNAME="Opensubtitles Username"
    OPENSUBTITLES_PASSWORD="Opensubtitles Password"
    ADDIC7ED_USERNAME="Addic7ed Username"
    ADDIC7ED_PASSWORD="Addic7ed Password"
    LEGENDASTV_USERNAME="LegendasTV Username"
    LEGENDASTV_PASSWORD="LegendasTV Password"

An example .env file would contain values looking something like this

    LOG_PATH="C:/Users/{username}/OneDrive/Desktop/ProgrammingStuff/python/movieman/log"
    VLC_HIST_FOLDER="C:/Users/{username}/AppData/Roaming/vlc"
    DUMP_PATH="C:/Users/{username}/OneDrive/Desktop/ProgrammingStuff/python/movieman/dump"
    THUMBNAILS_FOLDER="C:/Users/{username}/Videos/.MOVIES/title-screens"
    TO_WATCH_FOLDER="C:/Users/{username}/Videos/.MOVIES/to-watch"
    WATCHED_FOLDER="C:/Users/{username}/Videos/.MOVIES/watched"
    OPENSUBTITLES_USERNAME="username"
    OPENSUBTITLES_PASSWORD="password"
    ADDIC7ED_USERNAME="username"
    ADDIC7ED_PASSWORD="password"
    LEGENDASTV_USERNAME="username"
    LEGENDASTV_PASSWORD="password"

Go to qBitTorrent > Tools > Options > Downloads and check "Copy .torrent files for finished downloads to" and set the destination folder to same path as DUMP_PATH from your .env file.

Make movieman.py run at start up. One way to do this would be to press "WIN + R", type "shell:startup", make a bat file called "movieman.bat" in the folder that opens up. Copy the contents of the movieman.bat.example file from this repo and change the path as required.

## Thanks

[Jorti's extract-subs](https://github.com/jorti/extract-subs)

[Subliminal](https://pypi.org/project/subliminal/)

[Watchdog](https://pypi.org/project/watchdog/)

## TODO

- [X] Automatically move movie that user has watched from to-watch/ folder to watched/ folder

- [X] When movies are downloaded, check if subtitles are there. If not then download subtitles.

- [X] Automatically rename movies, folders and subtitles to a uniform format {Name of movie (<year of release>)}.ext}

- [X] Automatically setup environment and make script run at startup by running setup.py.

- [X] When a .png file is added to a movie folder automatically make it the directory icon of the appropriate movie.
