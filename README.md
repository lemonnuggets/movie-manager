# movie-manager

*WIP*

A python script that runs at startup to manage your movie folder. (Only tested on Windows)
# Prerequisites

[MKVToolNix](https://mkvtoolnix.download/downloads.html#windows)

[VLC Media Player](https://www.videolan.org/vlc/)

[QBitTorrent](https://www.qbittorrent.org/download.php)

# Instructions

Only use if you use VLC as your media player and qBitTorrent as your torrent client.

    git clone https://www.github.com/lemonnuggets/movieman.git
    cd movieman
    pip install -r requirements.txt

Make movieman.py run at start up.

Go to qBitTorrent > Tools > Options > Downloads and check "Copy .torrent files for finished downloads to" and set the destination folder to same path as DUMP_PATH from your .env file.

# Thanks

[Jorti's extract-subs](https://github.com/jorti/extract-subs)

[Subliminal](https://pypi.org/project/subliminal/)

[Watchdog](https://pypi.org/project/watchdog/)

# TODO

- [X] Automatically move movie that user has watched from to-watch/ folder to watched/ folder

- [X] When movies are downloaded, check if subtitles are there. If not then download subtitles.

- [X] Automatically rename movies, folders and subtitles to a uniform format {Name of movie (<year of release>)}.ext}

- [ ] When a .png file is added to the titlescreens folder automatically make it the directory icon of the appropriate movie.

