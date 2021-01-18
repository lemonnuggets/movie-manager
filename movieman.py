#!/usr/bin/env python3
"""
movieman
A python script to manage your movies.
"""
import os
import shutil
import time
import tkinter as tk
from tkinter.messagebox import askokcancel, askretrycancel
from configparser import ConfigParser
import urllib.parse
import re
import logging
from logging.handlers import RotatingFileHandler
import dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import substuff

# TODO: Test file by running it as usual.

# TODO: Stop shell from popping up.

# TODO: When a .png file is added to the titlescreens folder automatically make
# it the directory icon of the appropriate movie.

PROG_NAME = "movieman"

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)
VLC_HIST_FOLDER = os.path.realpath(os.getenv('VLC_HIST_FOLDER'))            # used to find the how much
VLC_HIST_FILE = os.path.join(VLC_HIST_FOLDER, 'vlc-qt-interface.ini')       # of the video has already been played.
VLC_ML_XSPF = os.path.join(VLC_HIST_FOLDER, 'ml.xspf')                      # last file that vlc moves before

DUMP_PATH = os.path.realpath(os.getenv('DUMP_PATH'))                        # Folder for finished torrents.
WATCHED_FOLDER = os.path.realpath(os.getenv('WATCHED_FOLDER'))
TO_WATCH_FOLDER = os.path.realpath(os.getenv('TO_WATCH_FOLDER'))

OPENSUBTITLES_USERNAME=os.getenv('OPENSUBTITLES_USERNAME')
OPENSUBTITLES_PASSWORD=os.getenv('OPENSUBTITLES_PASSWORD')
ADDIC7ED_USERNAME=os.getenv('ADDIC7ED_USERNAME')
ADDIC7ED_PASSWORD=os.getenv('ADDIC7ED_PASSWORD')
LEGENDASTV_USERNAME=os.getenv('LEGENDASTV_USERNAME')
LEGENDASTV_PASSWORD=os.getenv('LEGENDASTV_PASSWORD')

SUB_CONFIG = {"opensubtitles": {"username": OPENSUBTITLES_USERNAME, "password": OPENSUBTITLES_PASSWORD},
              "addic7ed": {"username": ADDIC7ED_USERNAME, "password": ADDIC7ED_PASSWORD},
              "legendastv": {"username": LEGENDASTV_USERNAME, "password": LEGENDASTV_PASSWORD}}

MOV_EXTENSIONS = ('.mkv', '.mp4', '.avi', '.mpg', '.mpeg')
SUB_EXTENSIONS = ('.srt', '.scc', '.vtt', '.ttml', '.aaf')

configur = ConfigParser(interpolation=None)
configur.read(VLC_HIST_FILE)
if not os.path.isdir('./logs'):
    os.makedirs('./logs')
logging.basicConfig(handlers=[RotatingFileHandler('./logs/my_log.log',
                                                  maxBytes=100000, backupCount=10)],
                    level=logging.INFO,
                    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
                    datefmt='%Y-%m-%dT%H:%M:%S')

class MovieHandler(FileSystemEventHandler):
    """
    Handler to watch for required events regarding the movie files.
    """
    def __init__(self, on_modified_callback=None, src_folder=None,
                 dest_folder=None, file_to_track=None, folder_to_track=None):
        self.src_folder = src_folder
        self.dest_folder = dest_folder
        self.on_modified_callback = on_modified_callback
        self.file_to_track = file_to_track
        self.folder_to_track = folder_to_track

    def on_any_event(self, event):
        logging.info(f"ANY EVENT -> {event}")

    def on_modified(self, event):
        if self.on_modified_callback and self.src_folder and self.dest_folder and self.file_to_track:
            self.on_modified_callback(self.src_folder, self.dest_folder,
                                      self.file_to_track, event.src_path)
        else:
            self.on_modified_callback(event.src_path)

def is_movie_watched(movie_path):
    """
    Argument: path to movie to be checked
    Return Value: Returns True if movie at movie_path has been watched such that
    less than one minute remains. (Checks VLC_HIST_FILE to get info about recently
    watched movies).
    Returns False if file isn't in recently watched files or if it's been watched
    for less than the entire length - 1 minute.
    """
    logging.info(f"in is_movie_watched({movie_path}) ->")
    if not os.path.isfile(movie_path):
        return False
    file_paths = [os.path.realpath(urllib.parse.unquote(string[8:]))
                  for string in configur.get('RecentsMRL', 'list').split(", ")]
    if not os.path.realpath(movie_path) in file_paths:
        return False
    times = [time for time in configur.get('RecentsMRL', 'times').split(', ')]
    watched_time = int(times[file_paths.index(movie_path)]) / 1000
    logging.info(f"leaving is_movie_watched({movie_path}) ->")
    return watched_time == 0

def ask_and_move(src_path, dest_path, message, success_message="Success!", retry_message="Retry?"):
    """
    Shows the user a pop up asking if they want to move src_path
    to dest_path. If user selects yes then src_path is moved to dest_path.
    """
    logging.info(f"in ask_and_move({src_path}, {dest_path}, {message}, {success_message}, {retry_message}) ->")
    window = tk.Tk()

    window.geometry(f"1x1+{round(window.winfo_screenwidth() / 2)}+{round(window.winfo_screenheight() / 2)}") # center window
    window.attributes('-topmost', True) # Open window on top of all other windows
    window.update()

    answer = askokcancel(title=PROG_NAME, message=message, parent=window)
    while answer:
        try:
            shutil.move(src_path, dest_path)
            break
        except Exception as err:
            logging.error(err)
            answer = askretrycancel(title=PROG_NAME, message=retry_message, parent=window)
            window.focus_set()
    logging.info(f"leaving ask_and_move({src_path}, {dest_path}, {message}, {success_message}, {retry_message}) ->")
    window.destroy()

def on_vlc_closed(to_watch_folder, watched_folder, ml_xspf, trigger):
    """
    Checks if modified event trigger was ml.xspf. If yes then finds movie in
    to_watch_folder that returns true from is_movie_watched(), and calls ask_and_move
    with the movie folder as source and the watched folder as destination.
    """
    if os.path.exists(trigger) and os.path.samefile(trigger, ml_xspf):
        logging.info('in on_vlc_closed() -> ')
        for content in os.listdir(to_watch_folder):
            folder_moved = False
            movie_folder = os.path.join(to_watch_folder, content)
            if not os.path.isdir(movie_folder):
                continue
            for file_ in os.listdir(movie_folder):
                movie = os.path.join(movie_folder, file_)
                if not os.path.isfile(movie):
                    continue
                logging.info(f"Movie: {movie}; IsWatched: {is_movie_watched(movie)}")
                if is_movie_watched(movie):
                    logging.info(f"Moving {movie_folder} to {watched_folder}")
                    ask_and_move(movie_folder, watched_folder,
                                 message=f"Move {movie_folder} to {watched_folder}?",
                                 success_message=f"Successfully moved {movie_folder} to {watched_folder}.",
                                 retry_message="Unable to move folder. Retry?")
                    folder_moved = True
                    break
            if folder_moved:
                continue
        logging.info("leaving on_vlc_close() ->")

def get_new_movie_filename(path):
    """
    Argument: path to file/dir that name is required for
    Return Value: New file/dir name (extension not included for file)
    """
    if os.path.isfile(path):
        file_name = os.path.splitext(os.path.basename(os.path.realpath(path)))[0]
    else:
        file_name = os.path.basename(path)
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

def ask_and_rename(to_be_renamed):
    """
    Arguments:
    to_be_renamed- List in the format [(old_file, new_file)]
    ReturnValue:
    Return True if files renamed correctly.
    Return False if files not renamed correctly.
    Shows the user a pop up asking if they want to rename the
    files/dirs in to_be_named.
    """
    logging.info(f"in ask_and_rename({to_be_renamed}) ->")
    message = ["Do you want to:-"]
    for (old_path, new_path) in to_be_renamed:
        message.append(f"Rename {old_path} to {new_path}")
    message = "\n".join(message)
    success_message = "Successfully renamed files!"
    retry_message = "Unable to rename files. Want to try again?"

    window = tk.Tk()
    logging.info(f"Message = {message}")

    window.geometry(f"1x1+{round(window.winfo_screenwidth() / 2)}+{round(window.winfo_screenheight() / 2)}") # center window
    window.attributes('-topmost', True) # Open window on top of all other windows
    window.update()

    answer = askokcancel(title=PROG_NAME, message=message, parent=window)
    logging.info(f"Answer = {answer}")
    success = False
    while answer:
        try:
            for (old_path, new_path) in to_be_renamed:
                logging.info(f"Old path = {old_path}; New Path = {new_path}")
                os.rename(old_path, new_path)
            success = True
            break
        except Exception as err:
            logging.error(err)
            answer = askretrycancel(title=PROG_NAME, message=retry_message, parent=window)
            window.focus_set()
    window.destroy()
    logging.info(f"leaving ask_and_rename({to_be_renamed}) ->")
    return success

def clear_except(dir_, needed_file):
    """
    Arguments:
    Dir_: Directory to delete files from
    needed_file: File to be ignored
    ReturnValue:
    0 if dir_ or needed_file isn't a proper directory
    and file respectively.
    1 otherwise
    """
    logging.info(f"in clear_except({dir_}, {needed_file}) ->")
    if not os.path.isdir(dir_):
        logging.error(f"{dir_} isn't a valid directory.")
        return 0
    if not os.path.isfile(needed_file):
        logging.error(f"{needed_file} doesn't exist.")
        return 0
    for file_ in os.listdir(dir_):
        path = os.path.join(dir_, file_)
        logging.info(f"Checking {path}")
        if not os.path.samefile(needed_file, path):
            try:
                logging.info(f"Removing {path}")
                os.remove(path)
            except Exception as err:
                logging.error(err)
    logging.info(f"leaving clear_except({dir_}, {needed_file}) ->")
    return 1

def rename_dir_and_contents(dir_):
    """
    Rename movie folder(dir_), movie file and subtitle file.
    """
    logging.info(f"in rename_dir_and_contents({dir_}) ->")
    old_name = os.path.basename(dir_)
    new_name = get_new_movie_filename(dir_)
    if new_name == None or old_name == new_name:
        return 0
    to_be_renamed = []
    new_dir_path = os.path.join(os.path.dirname(dir_), new_name)
    # to_be_renamed.append((dir_, new_dir_name)))
    success = ask_and_rename([(dir_, new_dir_path)])
    if not success:
        return False
    dir_ = new_dir_path
    for root, dirs, files in os.walk(dir_):
        for name in files:
            file_ = os.path.join(root, name)
            logging.info(f"FILE: {file_}")
            extension = os.path.splitext(file_)[1]
            if extension in (*MOV_EXTENSIONS, *SUB_EXTENSIONS):
                to_be_renamed.append((file_, os.path.join(os.path.dirname(file_), new_name + extension)))
    logging.info(f"Asking to rename:- {to_be_renamed}")
    success = ask_and_rename(to_be_renamed)
    logging.info(f"leaving rename_dir_and_contents({dir_}) ->")
    return success

def sub_and_rename(dir_path):
    """
    Get subtitle files and rename movie folder.
    """
    logging.info(f"in sub_and_rename({dir_path})->")
    substuff.main(['substuff.py', dir_path], SUB_CONFIG)
    rename_dir_and_contents(dir_path)
    logging.info(f"leaving sub_and_rename({dir_path})->")

def on_torrent_finished(torrent):
    """
    Runs when torrent file is modified in DUMP_PATH. Clears all other files
    in the DUMP_PATH.
    Since torrent file is added to the folder on torrent completion,
    this means that some torrent finished downloading. Therefore it looks
    for this new movie folder and if it doesnt't have the same name as the
    torrent file, then it checks if there are any folders that need to be renamed,
    and renames them.
    """
    logging.info(f"in on_torrent_finished({torrent}) ->")
    clear_except(DUMP_PATH, torrent)
    old_name = os.path.splitext(os.path.basename(torrent))[0]
    dir_path_1 = os.path.join(TO_WATCH_FOLDER, old_name)
    dir_path_2 = os.path.join(WATCHED_FOLDER, old_name)
    if os.path.isdir(dir_path_1):
        sub_and_rename(dir_path_1)
    elif os.path.isdir(dir_path_2):
        sub_and_rename(dir_path_2)
    else:
        paths = []
        for dir_ in os.listdir(TO_WATCH_FOLDER):
            sub_and_rename(os.path.join(TO_WATCH_FOLDER, dir_))
        for dir_ in os.listdir(WATCHED_FOLDER):
            sub_and_rename(os.path.join(WATCHED_FOLDER, dir_))
    logging.info(f"leaving on_torrent_finished({torrent}) ->")

def show_script_started():
    """
    Initial pop-up to show that script is running
    """
    window = tk.Tk()

    window.geometry(f"1x1+{round(window.winfo_screenwidth() / 2)}+{round(window.winfo_screenheight() / 2)}") # center window
    window.attributes('-topmost', True) # Open window on top of all other windows
    window.update()
    message = "MOVIEMAN IS NOW RUNNING..."

    answer = askokcancel(title=PROG_NAME, message=message, parent=window)
    window.destroy()

new_watched_event_handler = MovieHandler(on_modified_callback=on_vlc_closed, src_folder=TO_WATCH_FOLDER,
                                         dest_folder=WATCHED_FOLDER, file_to_track=VLC_ML_XSPF)
new_watched_observer = Observer()                                           # monitoring VLC_HIST_FOLDER
new_watched_observer.schedule(new_watched_event_handler, VLC_HIST_FOLDER)   # To detect when vlc is closed and
new_watched_observer.start()                                                # which movies were recently watched.
logging.info("Started observing->" + VLC_HIST_FOLDER)
new_movie_event_handler = MovieHandler(on_modified_callback=on_torrent_finished)
new_movie_observer = Observer()
new_movie_observer.schedule(new_movie_event_handler, DUMP_PATH)
new_movie_observer.start()
logging.info("Started observing->" + DUMP_PATH)

try:
    show_script_started()
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    new_watched_observer.stop()
    logging.info("Stopped observing->" + VLC_HIST_FOLDER)
    logging.info("Stopped observing->" + DUMP_PATH)
