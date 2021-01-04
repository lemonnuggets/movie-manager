# movie-manager

*WIP*

A python script that runs at startup to manage your movie folder.

# Instructions

Only use if you use VLC as your media player and qBitTorrent as your torrent client.

    git clone https://www.github.com/lemonnuggets/movieman.git
    cd movieman
    pip install -r requirements.txt
    
Make movieman.py run at start up.

Go to qBitTorrent > Tools > Options > Downloads and check "Copy .torrent files for finished downloads to" and set the destination folder to same path as DUMP_PATH from your .env file.

# Thanks

[Jorti's extract-subs](https://github.com/jorti/extract-subs)

[Python OpenCV2](https://pypi.org/project/opencv-python/)

[Watchdog](https://pypi.org/project/watchdog/)

[Subliminal](https://pypi.org/project/subliminal/)
