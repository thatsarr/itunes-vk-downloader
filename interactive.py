import argparse
import os
import getpass

from modules.downloader import VkDownloader
from modules.preprocessors import preprocess_itunes_playlist, preprocess_shazam_database

welcome_string = "Welcome to mp3 downloader! (App uses vk.com API for downloading)"

credential_warning_string = "Ypur login and password are needed for downloading. Use this program at your own risk. (" \
                            "IDK, how this data is stored and transmitted) "

def main():
    print(welcome_string, end="\n\n")

    print(credential_warning_string, end="\n\n")

    output_folder = None
    while output_folder is None or not os.path.isdir(output_folder):
        output_folder = input("Provide folder for downloaded songs: ")
        if not os.path.isdir(output_folder): print("\"{}\" is not a folder".format(output_folder))

    try:
        downloader = VkDownloader(output_folder)
    except ValueError:
        print("[ ERROR ]: Output folder %s doesn\'t exist" % args.output)
        return 1

    auth_res = 1
    while auth_res != 0:
        print("Enter your vk.com credentials:")
        vk_login = input("\tlogin: ")

        auth_res = downloader.auth(vk_login, getpass.getpass("\tpassword: "))
        if auth_res != 0:
            print("[ ERROR ]: Wrong credentials")
        else:
            print("Auth success")

    print("Starting songs download. For exit press Ctrl+C")

    while True:
        search_request = input("\nSearch for: ")

        search_results = downloader.search(search_request)
        
        if len(search_results) == 0:
            print("[ ERROR ]: 0 search results")
            continue
        
        print("Search success")
        i = 0   
        while True:
            res = search_results[i]
            print("result #{}: \n\t{}".format(i, repr(res)))
            if i != 0 and i % 10 == 0: 
                decision_index = None 
                while not decision_index:
                    decision = input("Choose song number (0 to {}) or \"N\" for next 10 results: ".format(i))
                    if decision.lower() == "n":
                        decision_index = -1
                    else:
                        try:
                            decision_index = int(decision)
                        except ValueError:
                            continue
                        if decision_index > i:
                            continue
                if decision_index != -1:
                    print("Song #{} was chosen. Song info\n\t{}".format(decision_index, repr(search_results[decision_index])))
                    break           
        
        res = search_results[decision_index]
        url = res['url']
        artist = res['artist']
        song = res['title']
        
        downloader.download(os.path.join(output_folder, "{}-{}.mp3".format(artist, song)), url)


if __name__ == '__main__':
    main()
