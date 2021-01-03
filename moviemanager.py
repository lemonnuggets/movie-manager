"""
A python script to manage your movies.
"""
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

"""
Instead of using the vlc-qt-interface file changes to try and find if a movie has been watched,
use the last file that vlc modifies/moves/closes to notice that vlc has just been closed and then
ask the user if they have finished watching the most recent movie in RecentMRL, if the time watched is 0.
"""

import os
import shutil
import time
from configparser import ConfigParser
import urllib.parse
import re
import dotenv
import cv2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subtitler

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

ROOT_MONITORED_PATH = os.path.realpath(os.getenv('ROOT_MONITORED_PATH'))
VLC_HIST_FILE = os.path.realpath(os.getenv('VLC_HIST_FILE'))    # used to find the how much
                                                                # of the video has already been played.
WATCHED_FOLDER = os.path.realpath(os.getenv('WATCHED_FOLDER'))
TO_WATCH_FOLDER = os.path.realpath(os.getenv('TO_WATCH_FOLDER'))
VLC_HIST_FOLDER = os.path.realpath(os.getenv('VLC_HIST_FOLDER'))
print(ROOT_MONITORED_PATH, VLC_HIST_FILE, WATCHED_FOLDER, TO_WATCH_FOLDER, VLC_HIST_FOLDER)

configur = ConfigParser(interpolation=None)
configur.read(VLC_HIST_FILE)

class WatchedHandler(FileSystemEventHandler):
    def __init__(self, callback, src_folder=None, dest_folder=None, file_to_track=None):
        self.src_folder = src_folder
        self.dest_folder = dest_folder
        self.callback = callback
        self.file_to_track = file_to_track
    
    def on_any_event(self, event):
        print("ANY EVENT ->",event)
    
    def on_moved(self, event):
        print("in on_moved() -> ")
        self.callback(self.src_folder, self.dest_folder, self.file_to_track, event.dest_path)
        
        
    # def on_modified(self, event):
        # print(event)
        # print(event.src_path)
        # self.callback(self.src_folder, self.dest_folder, self.file_to_track, event.src_path)

def on_watched_new(to_watch_folder, watched_folder, hist_file, trigger):
    print("in on_watched_new() -> ")
    if os.path.exists(trigger) and os.path.samefile(trigger, hist_file):
        for content in os.listdir(to_watch_folder):
            folder_moved = False
            movie_folder = os.path.join(to_watch_folder, content)
            if not os.path.isdir(movie_folder):
                continue
            for file_ in os.listdir(movie_folder):
                movie = os.path.join(movie_folder, file_)
                if not os.path.isfile(movie):
                    continue
                if is_movie_watched(movie):
                    print(f"Moving {movie_folder} to {watched_folder}")
                    shutil.move(movie_folder, watched_folder)
                    folder_moved = True
                    break
            if folder_moved:
                continue
    print("leaving on_watched_new() ->")
            

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
    Argument: path to movie to be checked
    Return Value: Returns True if movie at movie_path has been watched such that less than one minute remains.
    (Checks VLC_HIST_FILE to get info about recently watched movies)
    Returns False if file isn't in recently watched files or if it's been watched for less
    than the entire length - 1 minute.
    """
    if not os.path.isfile(movie_path):
        return False
    file_paths = [os.path.realpath(urllib.parse.unquote(string[8:]))
                  for string in configur.get('RecentsMRL', 'list').split(", ")]
    if not os.path.realpath(movie_path) in file_paths:
        return False
    times = [time for time in configur.get('RecentsMRL', 'times').split(', ')]
    watched_time = int(times[file_paths.index(movie_path)]) / 1000

    video = cv2.VideoCapture(movie_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    runtime = frame_count / fps
    return runtime - watched_time <= 60


# print(is_movie_watched("a"))
print(is_movie_watched(r'C:\Users\adamj\Videos\.MOVIES\to-watch\First Cow (2019)\First Cow (2019).mp4'))
# print(configur.get('RecentsMRL', 'times'))
# print(get_new_movie_filename(r'C:\Users\adamj\Videos\.MOVIES\to-watch\First Cow (2019)\First Cow (2019).mp4'))
# print(get_new_movie_filename(r'C:\Users\adamj\Videos\.MOVIES\to-watch\First Cow (2019)\El.Camino.A.Breaking.Bad.Movie.2019.1080p.WEBRip.x264-[YTS.LT].mp4'))
new_watched_event_handler = WatchedHandler(on_watched_new, TO_WATCH_FOLDER, WATCHED_FOLDER, VLC_HIST_FILE)
new_watched_observer = Observer()
new_watched_observer.schedule(new_watched_event_handler, VLC_HIST_FOLDER)
new_watched_observer.start()
print("Started observing-> " + VLC_HIST_FOLDER)

try: 
    while True:
        time.sleep(10)
        print('timer')
except KeyboardInterrupt:
    new_watched_observer.stop()
    print("Stopped observing-> " + VLC_HIST_FOLDER)
