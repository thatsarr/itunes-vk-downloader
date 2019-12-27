import vk_api
from vk_api import audio
import vlc
import os

from modules.spinner import spin


class VkDownloader:
    REQUEST_STATUS_CODE = 200

    def __init__(self, interactive = True):
        self.interactive = interactive
        self.vk_audio = None

    def auth(self, vk_login, vk_password):
        vk_session = vk_api.VkApi(login=vk_login, password=vk_password)
        try:
            vk_session.auth()
        except:
            return 2
        # vk = vk_session.get_api()  # Теперь можно обращаться к методам API как к обычным классам
        self.vk_audio = audio.VkAudio(vk_session)  # Получаем доступ к audio
        return 0

    def search(self, search_request):
        print("Searching for \"{}\"".format(search_request))
        res = list(self.vk_audio.search(search_request))
        if len(res) == 0:
            return None
        else:
            return res

    def choose_search_result(self, search_line, search_results):
        for search_result in search_results:
            artist = search_result['artist']
            song = search_result['title']
            result_string = "{}-{}".format(artist, song)
            if search_line.lower().replace(" ", "") != result_string.lower().replace(" ", ""):
                print("[ WARNING ]: search tgt string doesn't match search result (tgt: \"{}\"; res:\"{}\")"
                      .format(search_line, result_string))
                if not self.interactive:
                    print("Going to next result")
                else:
                    decision = input("Go to next result (1) or skip line (2) or download anyway (3)? : ")
                    if decision == "2":
                        return None
                    elif decision == "3":
                        return search_result
            else:
                return search_result
        return None


    def download_songs(self, tgt_dir, search_request_lines):
        if not os.path.isdir(tgt_dir):
            raise ValueError

        total_songs = len(search_request_lines)

        failed_requests = []
        for i, line in enumerate(search_request_lines):
            line = line.replace("\n", "")
            print("\nSong {} of {}".format(i, total_songs))
            search_results = self.search(line)
            if search_results is None:
                failed_requests.append((i, search_request_lines, "not found in VK"))
                continue;
            search_result = self.choose_search_result(line, search_results)
            if search_result is None:
                continue

            self.download(tgt_dir, search_result)

        return failed_requests

    def download(self, tgt_dir, search_result):
        if not os.path.isdir(tgt_dir):
            raise ValueError

        url = search_result['url']
        artist = search_result['artist']
        song = search_result['title']
        result_string = "{}-{}.mp3".format(artist, song)

        filename_short = "{}-{}.mp3".format(artist, song)
        filename_long = os.path.join(tgt_dir, filename_short)

        if os.path.exists(filename_long):
            print("File \"%s\" exists. skipping" % filename_long)
            return

        print("Preparing for download \"{}\" mp3".format(result_string))
        inst = vlc.Instance("--quiet")
        p = inst.media_player_new()
        cmd1 = "sout=#transcode{vcodec=none,acodec=mp3,ab=128,channels=2," \
               "samplerate=44100,scodec=none}:std{access=file{no-overwrite},mux=mp3,dst='%s'}" % \
               (filename_long)
        cmd2 = "no-sout-rtp-sap"
        cmd3 = "no-sout-standard-sap"
        cmd4 = "sout-keep"
        med = inst.media_new(url, cmd1, cmd2, cmd3, cmd4)
        med.get_mrl()
        p.set_media(med)
        p.play()

        print("Download started")

        # with open(os.path.join(path, "{}-{}.mp3".format(artist, song)), 'wb') as f:
        #     f.write(r.content)
        while (p.get_state() != 6):
            spin()

        print("Download finished")

        p.stop()
        p.release()
        inst.release()
        return 0
