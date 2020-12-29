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
from dotenv import load_dotenv
 
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

ROOT_MONITORED_PATH = os.getenv('ROOT_MONITORED_PATH')
VLC_HIST_FILE = os.getenv('VLC_HIST_FILE')  # used to find the how much 
                                            # of the video has already been played.
