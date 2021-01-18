#!/usr/bin/env python3
"""
Copyright 2015 Juan Orti Alcaine <j.orti.alcaine@gmail.com>


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import os
import re
import subprocess
import logging
from logging.handlers import RotatingFileHandler
from subliminal import save_subtitles, scan_video, region, download_best_subtitles, ProviderPool
from babelfish import Language


WDIR = ""
if not os.path.isdir('./logs'):
    os.makedirs('./logs')
logging.basicConfig(handlers=[RotatingFileHandler('./logs/my_log.log', maxBytes=100000, backupCount=10)],
                    level=logging.INFO,
                    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
                    datefmt='%Y-%m-%dT%H:%M:%S')
# logging.basicConfig(level=logging.DEBUG, filename='log.log',
#                     filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

def get_mkv_track_id(file_path):
    """ Returns the track ID of the SRT subtitles track"""
    try:
        raw_info = subprocess.check_output(["mkvmerge", "-i", file_path],
                                            stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as ex:
        logging.error(ex)
        sys.exit(1)
    pattern = re.compile(r'.* (\d+): subtitles \(SubRip/SRT\).*', re.DOTALL)
    matches = pattern.match(str(raw_info))
    if matches:
        return raw_info, matches.group(1)
    else:
        return raw_info, None


def download_subs(file, config):
    logging.info("    Analyzing video file...")
    try:
        video = scan_video(file['full_path'])
    except ValueError as ex:
        logging.error(f"    Failed to analyze video. {ex}")
        return None
    try:
        logging.info("    Choosing subtitle from online providers...")
        best_subtitles = download_best_subtitles(videos = {video}, languages = {Language('eng')}, only_one=True, pool_class=ProviderPool, provider_configs = config)
        if best_subtitles[video]:
            sub = best_subtitles[video][0]
            logging.info("    Choosen subtitle: {f}".format(f=sub))
            logging.info("    Downloading...")
            save_subtitles(video, [sub], single=True)
        else:
            logging.info("    ERROR: No subtitles found online.")
    except Exception as err:
        logging.error(f"    Error downloading subtitles. {err}")


def extract_mkv_subs(file):
    logging.info("    Extracting embedded subtitles...")
    try:
        subprocess.call(["mkvextract", "tracks", file['full_path'],
                         file['srt_track_id'] + ":" + file['srt_full_path']])
        logging.info("    OK.")
    except subprocess.CalledProcessError:
        logging.error("    ERROR: Could not extract subtitles")


def extract_subs(files, config):
    for file in files:
        logging.info("*****************************")
        logging.info("Directory: {d}".format(d=file['dir']))
        logging.info("File: {f}".format(f=file['filename']))
        if file['srt_exists']:
            logging.info("    Subtitles ready. Nothing to do.")
            continue
        if not file['srt_track_id']:
            logging.info("    No embedded subtitles found.")
            download_subs(file, config)
        else:
            logging.info("    Embedded subtitles found.")
            extract_mkv_subs(file)


def main(argv, config=None):
    supported_extensions = ['.mkv', '.mp4', '.avi', '.mpg', '.mpeg']
    if not argv:
        logging.error("Error, no directory supplied")
        sys.exit(1)
    if not os.path.isdir(argv[1]):
        sys.exit("Error, {f} is not a directory".format(f=argv[1]))
    global WDIR
    WDIR = argv[1]
    cache_dir = os.path.join(os.getenv('HOME'), '.subliminal')
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    cache_file = os.path.join(cache_dir, 'subliminal.cachefile.dbm')
    # configure the cache
    region.configure('dogpile.cache.dbm', arguments={'filename': cache_file}, replace_existing_backend=True)
    file_list = []
    for root, dirs, files in os.walk(WDIR):
        for name in files:
            (basename, ext) = os.path.splitext(name)
            if ext in supported_extensions:
                if ext == '.mkv':
                    (raw_track_info, track_id) = get_mkv_track_id(os.path.join(root, name))
                else:
                    raw_track_info = None
                    track_id = None
                srt_full_path = os.path.join(root, basename + ".srt")
                srt_exists = os.path.isfile(srt_full_path)
                file_list.append({'filename': name,
                                  'basename': basename,
                                  'extension': ext,
                                  'dir': root,
                                  'full_path': os.path.join(root, name),
                                  'srt_track_id': track_id,
                                  'srt_full_path': srt_full_path,
                                  'srt_exists': srt_exists,
                                  'raw_info': raw_track_info
                                  })
    extract_subs(file_list, config)


if __name__ == '__main__':
    main(sys.argv)
