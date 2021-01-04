"""
movieman
A python script to manage your movies.
"""
# TODO: When movies are downloaded, check if subtitles are there. If not
# then download subtitles.
#
# TODO: Automatically rename movies, folders and subtitles to a uniform format
# {Name of movie (<year of release>)}.ext
#
# TODO: When a .png file is added to the titlescreens folder automatically make
# it the directory icon of the appropriate movie.

import os
import shutil
import time
import tkinter as tk
from tkinter.messagebox import askokcancel, askretrycancel, showinfo
from configparser import ConfigParser
import urllib.parse
import re
import dotenv
import cv2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import substuff

PROG_NAME = "movieman"

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

ROOT_MONITORED_PATH = os.path.realpath(os.getenv('ROOT_MONITORED_PATH'))
VLC_HIST_FILE = os.path.realpath(os.getenv('VLC_HIST_FILE'))    # used to find the how much
                                                                # of the video has already been played.
VLC_ML_XSPF = os.path.realpath(os.getenv('VLC_ML_XSPF'))        # last file that vlc moves before
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
    
    def on_modified(self, event):
        print(event)
        print(event.src_path)
        self.callback(self.src_folder, self.dest_folder, self.file_to_track, event.src_path)

def ask_and_move(src_path, dest_path, message, success_message="Success!", retry_message="Retry?"):
    """
    Shows the user a pop up asking if they want to move src_path 
    to dest_path. If user selects yes then src_path is moved to dest_path.
    """
    window = tk.Tk()

    window.geometry(f"1x1+{round(window.winfo_screenwidth() / 2)}+{round(window.winfo_screenheight() / 2)}")
    window.attributes('-topmost', True)
    window.update()

    answer = askokcancel(title=PROG_NAME, message=message, parent=window)
    while answer:
        try:
            shutil.move(src_path, dest_path)
            break
        except:
            answer = askretrycancel(title=PROG_NAME, message=retry_message, parent=window)
            window.focus_set()
        else:
            showinfo(title=PROG_NAME, message=success_message, parent=window)
            window.focus_set()
    
    window.destroy()
            
def on_vlc_closed(to_watch_folder, watched_folder, ml_xspf, trigger):
    """
    Checks if modified event trigger was ml.xspf. If yes then finds movie in
    to_watch_folder that returns true from is_movie_watched(), and calls ask_and_move
    with the movie folder as source and the watched folder as destination.
    """
    if os.path.exists(trigger) and os.path.samefile(trigger, ml_xspf):
        print('in on_vlc_closed() -> ')
        for content in os.listdir(to_watch_folder):         
            folder_moved = False
            movie_folder = os.path.join(to_watch_folder, content)
            if not os.path.isdir(movie_folder):
                continue
            for file_ in os.listdir(movie_folder):
                movie = os.path.join(movie_folder, file_)
                if not os.path.isfile(movie):
                    continue
                print(f"Movie: {movie}; IsWatched: {is_movie_watched(movie)}")
                if is_movie_watched(movie):
                    print(f"Moving {movie_folder} to {watched_folder}")
                    ask_and_move(movie_folder, watched_folder,
                                 message=f"Move {movie_folder} to {watched_folder}?",
                                 success_message=f"Successfully moved {movie_folder} to {watched_folder}.",
                                 retry_message=f"Unable to move folder. Retry?")
                    folder_moved = True
                    break
            if folder_moved:
                continue
        print("leaving on_vlc_close() ->")
        
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
    return runtime - watched_time <= 60 or watched_time == 0


print(is_movie_watched(r'C:\Users\adamj\Videos\.MOVIES\to-watch\First Cow (2019)\First Cow (2019).mp4'))
new_watched_event_handler = WatchedHandler(on_vlc_closed, TO_WATCH_FOLDER, WATCHED_FOLDER, VLC_ML_XSPF)
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
