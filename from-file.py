import argparse
import os
import getpass

from modules.downloader import VkDownloader
from modules.preprocessors import preprocess_itunes_playlist, preprocess_shazam_database

welcome_string = "Welcome to mp3 downloader!\nNow music mentioned in source \"%s\" will be downloaded to output folder " \
                 "folder \"%s\". vk.com API will be used for download. "

credential_warning_string = "Ypur login and password are needed for downloading. Use this program at your own risk. (" \
                            "IDK, how this data is stored and transmitted) "

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str,
                    help="Input file name. Parsed according to \"--input-type\" argument")
parser.add_argument("output", type=str,
                    help="Output folder path for music downloading")

parser.add_argument("--input-type", choices=['ready-txt', 'itunes-playlist', "shazam-database"],
                    dest="input_type", required=True,
                    help="\t\'ready-txt\': file that contains lines ready for search request (for example \"Metallica "
                         "- Fuel\"). This input type is used \"as-is\"\n"
                         "\t\'itunes-playlist\': input is an exported playlist from itunes in form of one or more \"\\t\" separated "
                         "csv with \\r as newline separator and in \"utf-16le\" encoding. Only 1st and 2nd columns are used (song name and artist name "
                         "correspondingly)\n"
                         "\t\'shazam-database\': input is a sqlite database file from \"Shazam\". "
                         "Used columns: \"status\", \"json\" in \"tag\" table")
parser.add_argument("--start-number", type=int, dest="start_number",
                    help="Number of song to start (used for interrupted downloading process)")
args = parser.parse_args()


def preprocess_input():
    if args.input_type == 'ready-txt':
        if os.path.isfile(args.input):
            with open(args.input) as f:
                content = f.readlines()
            return content
        else:
            return None
    if args.input_type == 'itunes-playlist':
        if os.path.isfile(args.input):
            return preprocess_itunes_playlist()
        else:
            return None
    if args.input_type == 'shazam-database':
        if os.path.isfile(args.input):
            return preprocess_shazam_database(args.input)
        else:
            return None


def main():
    print(welcome_string % (args.input, args.output), end="\n\n")

    print(credential_warning_string, end="\n\n")

    auth_res = 1
    while auth_res != 0:
        print("Enter your vk.com credentials:")
        vk_login = input("\tlogin: ")
        # vk_id = input("\tid: ")
        vk_password = getpass.getpass("\tpassword: ")

        try:
            downloader = VkDownloader(args.output)
        except ValueError:
            print("[ ERROR ]: Output folder %s doesn\'t exist" % args.output)
            return 1

        auth_res = downloader.auth(vk_login, vk_password)
        if auth_res != 0:
            print("[ ERROR ]: Wrong credentials")
        else:
            print("Auth success")

    request_lines = preprocess_input()

    total_songs = len(request_lines)
    print("{} entries found".format(total_songs))

    print("Starting download")
    failed_requests = downloader.download_songs(args.output, request_lines)

    if len(failed_requests) != 0:
        print("Files downloaded: {} of {}".format(total_songs - len(failed_requests), total_songs))
        print("Failed:")
        for failed_request in failed_requests:
            print("\t#%d: %s, %s" % failed_request)

    if len(failed_requests) == 0:
        print("-------------------------------\n\nStatus:\n\tTotal success")
    else:
        print("-------------------------------\n\nStatus:\n\tPartial success. See above logs for info")


if __name__ == '__main__':
    main()
