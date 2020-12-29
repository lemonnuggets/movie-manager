# TODO: Find which videos have been watched in the to-watch/ folder
# and move them to the watched/ folder. (check whenever VLC_HIST_FILE
# is changed).
# 
# TODO: When movies are downloaded, check if subtitles are there. If not
# then download subtitles.
# 
# TODO: Automatically rename movies, folders and subtitles to a uniform format
# {Name of movie (<year of release>)}.ext
# 
# TODO: When a .png file is added to the titlescreens folder automatically make
# it the directory icon.

import os
import watchdog
import subtitler

ROOT_MONITORED_PATH = r"C:\Users\adamj\Videos\.MOVIES\"
VLC_HIST_FILE = r"C:\Users\adamj\AppData\Roaming\vlc\vlc-qt-interface.ini" # used to find the how much of the video has already been played.
