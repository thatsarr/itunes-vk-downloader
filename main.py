import argparse
import os

from downloader import download

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str,
                    help="Input txt file (playlist imported fro iTunes. "
                         "It is assumed to be in \"utf-16le\" encoding, "
                         "\"\\r\" as newline separator, "
                         "one or more \"\\t\" as items separator.")
parser.add_argument("output", type=str,
                    help="Output folder path for music downloading")

parser.add_argument("--input-type", choices=['ready-txt', 'itunes-playlist'], dest="input_type")
parser.add_argument("--start-number", type=int, dest="start_number")
args = parser.parse_args()


def preprocess(fname, tgt_fname):
    pass


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

tmp_fname = args.input + ".tmp"
preprocess(args.input, tmp_fname)

total_songs = file_len(os.path.abspath(tmp_fname)) -1
print("{} songs found".format(total_songs))

failed_files = []
with open(tmp_fname, "rt") as f:
    # skipping first line
    line = f.readline()
    i = 1
    if args.start_number:
        while i != args.start_number:
            f.readline()
            i += 1
    line = f.readline()
    while len(line) != 0:
        values = line.split('|')
        songname = values[0]
        artist = values[1]
        print("\nSong {} of {}".format(i, total_songs))
        res = download(artist, songname)
        if res == 1:
            failed_files.append((i, artist, songname, "not found in VK"))
        line = f.readline()
        i += 1
    print("All songs downloaded")
    print("Cleaning tmp files")
    os.remove(tmp_fname)
    print("Status: ", end='')
    if len(failed_files) == 0:
        print("Total success")
    else:
        print("Partial success")
        print("Files downloaded: {} of {}".format(total_songs - len(failed_files), total_songs))
        print("Failed:")
        for failed_song in failed_files:
            print("\t#%d: %s - %s, %s" % failed_song)
    print("exited")
