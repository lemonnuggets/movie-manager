"""
Sets up environment variables, and adds script to startup.
"""
import os
import getpass
# print(os.path.abspath(__file__))
username = getpass.getuser()
script_dir = os.path.dirname(os.path.abspath(__file__))

default_log_path = os.path.join(script_dir, 'logs')
default_dump_path = os.path.join(script_dir, 'dump')
default_vlchist_path=os.path.realpath(f"C:/Users/{username}/AppData/Roaming/vlc")
default_titlescreens_path=os.path.realpath(f"C:/Users/{username}/Videos/.MOVIES/title-screens")
default_towatch_path=os.path.realpath(f"C:/Users/{username}/Videos/.MOVIES/to-watch")
default_watched_path=os.path.realpath(f"C:/Users/{username}/Videos/.MOVIES/watched")

print("............................................................")

print("Do not enter file paths manually as any mistakes in the path WILL lead to errors!!\nAlways copy and paste the paths.")

log_path = input(f"Enter absolute directory path for logs (default = {default_log_path}):\n") or default_log_path
dump_path = input(f"Enter absolute directory path for torrent dumps (default = {default_dump_path}):\n") or default_dump_path
vlchist_path = input(f"Enter absolute directory path for vlchists (default = {default_vlchist_path}):\n") or default_vlchist_path
titlescreens_path = input(f"Enter absolute directory path for titlescreens (default = {default_titlescreens_path}):\n") or default_titlescreens_path
towatch_path = input(f"Enter absolute directory path for movies to be watched (default = {default_towatch_path}):\n") or default_towatch_path
watched_path = input(f"Enter absolute directory path for watched movies (default = {default_watched_path}):\n") or default_watched_path

print("............................................................")

OPENSUBTITLES_USERNAME = input("Enter your OPENSUBTITLES USERNAME:\n")
OPENSUBTITLES_PASSWORD = input("Enter your OPENSUBTITLES PASSWORD:\n")
ADDIC7ED_USERNAME = input("Enter your ADDIC7ED USERNAME:\n")
ADDIC7ED_PASSWORD = input("Enter your ADDIC7ED PASSWORD:\n")
LEGENDASTV_USERNAME = input("Enter your LEGENDASTV USERNAME:\n")
LEGENDASTV_PASSWORD = input("Enter your LEGENDASTV PASSWORD:\n")

print("............................................................")

with open(os.path.join(script_dir, '.env'), 'w') as file:
    file.write(f"LOG_PATH=\"{os.path.realpath(log_path)}\"\n".replace("\\", "/"))
    file.write(f"DUMP_PATH=\"{os.path.realpath(dump_path)}\"\n".replace("\\", "/"))
    file.write(f"VLC_HIST_FOLDER=\"{os.path.realpath(vlchist_path)}\"\n".replace("\\", "/"))
    file.write(f"THUMBNAILS_FOLDER=\"{os.path.realpath(titlescreens_path)}\"\n".replace("\\", "/"))
    file.write(f"TO_WATCH_FOLDER=\"{os.path.realpath(towatch_path)}\"\n".replace("\\", "/"))
    file.write(f"WATCHED_FOLDER=\"{os.path.realpath(watched_path)}\"\n".replace("\\", "/"))
    file.write(f"OPENSUBTITLES_USERNAME=\"{OPENSUBTITLES_USERNAME}\"\n")
    file.write(f"OPENSUBTITLES_PASSWORD=\"{OPENSUBTITLES_PASSWORD}\"\n")
    file.write(f"ADDIC7ED_USERNAME=\"{ADDIC7ED_USERNAME}\"\n")
    file.write(f"ADDIC7ED_PASSWORD=\"{ADDIC7ED_PASSWORD}\"\n")
    file.write(f"LEGENDASTV_USERNAME=\"{LEGENDASTV_USERNAME}\"\n")
    file.write(f"LEGENDASTV_PASSWORD=\"{LEGENDASTV_PASSWORD}\"\n")
    print(f"FINISHED GENERATING .env FILE AT: {os.path.join(script_dir, '.env')}")
    print("Verify that values are as expected.")

print("............................................................")
choice = input("Enter y to run movieman at startup:\n")
if choice in ('y', 'Y'):
    print("Creating files for running movieman at startup")
    with open(os.path.join(script_dir, 'movieman.bat'), 'w') as file:
        file.write(f'@echo off\npythonw.exe "{os.path.join(script_dir, "movieman.py")}"')
    print(f"Created movieman.bat at {os.path.join(script_dir, 'movieman.bat')}")
    startup_dir = os.path.realpath(f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    with open(os.path.join(startup_dir, 'movieman.vbs'), 'w') as file:
        file.write(f"Set WshShell = CreateObject(\"WScript.Shell\")\nWshShell.Run chr(34) & \"{os.path.join(script_dir, 'movieman.bat')}\" & chr(34), 0\nSet WshShell = Nothing")
    print(f"Created movieman.vbs at {os.path.join(startup_dir, 'movieman.vbs')}")
else:
    print("movieman will not run at startup.")

# print(locals())
