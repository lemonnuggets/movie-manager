"""
https://github.com/c0defreak/subtitler
simple script to obtain subtitle from subdb.com
usage: python2 subtitler.py <moviefilename>
"""

import os
import hashlib
import argparse
import requests



def get_hash(name):

    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


def request_sub(hash_):
    md5 = hash_
    url = "http://api.thesubdb.com/?action=download&hash="+md5+"&language=en"
    header = {'user-agent': 'SubDB/1.0 (subtitler/0.1)'}
    r = requests.get(url, headers=header)
    if r.status_code == 200:
        return r.content
    else:
        return "something nasty happened"


def save_sub(data, filename):
    s_filename = filename[:-4] + ".srt"
    with open(s_filename, "w+") as s_f:
        s_f.write(data)


def main(filename):
    md5 = get_hash(filename)
    data = request_sub(md5)
    save_sub(data, filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    main(args.filename)
