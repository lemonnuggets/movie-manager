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
from configparser import ConfigParser
import urllib.parse
import watchdog
import subtitler
import dotenv
import re
import cv2

ROOT_MONITORED_PATH = os.getenv('ROOT_MONITORED_PATH')
VLC_HIST_FILE = os.getenv('VLC_HIST_FILE')  # used to find the how much
                                            # of the video has already been played.

configur = ConfigParser(interpolation=None)
configur.read(VLC_HIST_FILE)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

def get_new_movie_filename(file_path):
    """
    Argument: path to file that name is required for
    Return Value: New file path with name in correct format
    """
    file_name = os.path.splitext(os.path.basename(os.path.realpath(file_path)))[0]
    new_file_name = re.sub(r"\.", " ", file_name)
    new_file_name = re.sub(r"\(|\)|\[|\]|\{|\}", "", new_file_name)
    match_from_beginning = re.search(r"(.*)\b(18|19|20\d{2})\b", new_file_name) # doing it this way will make it so that
    match_from_end = re.search(r"\b(18|19|20\d{2})\b.*", new_file_name)         # files like "blade.runner.2049.2017.mp4"
    if not (match_from_end and match_from_beginning):                           # will become "blade runner 2049 (2017).mp4"
        return None                                                             # and not "blade runner (2049).mp4"
    name = match_from_beginning.group(1)                                        
    year = match_from_end.group(1)                                              
    new_file_name = f"{name}({year})"
    return new_file_name

def is_movie_watched(movie_path):
    """
    Returns True if movie at movie_path has been watched such that less than one minute remains.
    (Checks VLC_HIST_FILE to get info about recently watched movies)
    Returns False if file isn't in recently watched files or if it's been watched for less 
    than the entire length - 1 minute.
    """
    file_paths = [os.path.realpath(urllib.parse.unquote(string[8:])) for string in configur.get('RecentsMRL', 'list').split(", ")]
    if not os.path.realpath(movie_path) in file_paths:
        return False
    times = [time for time in configur.get('RecentsMRL', 'times').split(', ')]
    watched_time = int(times[file_paths.index(movie_path)]) / 1000

    video = cv2.VideoCapture(movie_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    runtime = frame_count / fps
    return runtime - watched_time <= 60  

print(is_movie_watched("a"))
print(is_movie_watched(r'C:\Users\adamj\Videos\.MOVIES\to-watch\First Cow (2019)\First Cow (2019).mp4'))
# print(configur.get('RecentsMRL', 'times'))
# print(get_new_movie_filename(r'C:\Users\adamj\Videos\.MOVIES\to-watch\First Cow (2019)\First Cow (2019).mp4'))
# print(get_new_movie_filename(r'C:\Users\adamj\Videos\.MOVIES\to-watch\First Cow (2019)\El.Camino.A.Breaking.Bad.Movie.2019.1080p.WEBRip.x264-[YTS.LT].mp4'))
