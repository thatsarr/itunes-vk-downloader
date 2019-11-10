import vk_api
from vk_api import audio
import vlc
import os

from modules.spinner import spin


class VkDownloader:
    REQUEST_STATUS_CODE = 200

    def __init__(self, tgt_dir):
        self.vk_audio = None
        if not os.path.isdir(tgt_dir):
            raise ValueError
        else:
            self.tgt_dir = tgt_dir

    def auth(self, vk_login, vk_password):
        vk_session = vk_api.VkApi(login=vk_login, password=vk_password)
        try:
            vk_session.auth()
        except:
            return 2
        # vk = vk_session.get_api()  # Теперь можно обращаться к методам API как к обычным классам
        self.vk_audio = audio.VkAudio(vk_session)  # Получаем доступ к audio
        return 0

    def download_songs(self, search_request_lines):
        total_songs = len(search_request_lines)

        failed_requests = []
        for i, line in enumerate(search_request_lines):
            print("\nSong {} of {}".format(i, total_songs))
            res = self.download(self.tgt_dir, line)
            if res == 1:
                failed_requests.append((i, search_request_lines, "not found in VK"))

        return failed_requests

    def download(self, path, search_line):
        print("Searching for \"{}\"".format(search_line))
        res = list(self.vk_audio.search(search_line))
        if len(res) >= 1:
            url = res[0]['url']
            artist = res[0]['artist']
            song = res[0]['title']
            result_string = "{} - {}".format(artist, song)
        else:
            print("[ ERROR ]: 0 search results")
            return 1
        print("Search success, file found: \"{}\"".format(result_string))

        if search_line.lower() != result_string.lower():
            print("[ WARNING ]: search tgt string doesn't match search result (tgt: \"{}\"; res:\"{}\")"
                  .format(search_line, result_string))

        filename_short = "{}-{}.mp3".format(artist, song)
        filename_long = os.path.join(path, filename_short)
        if os.path.exists(filename_long):
            print("File \"%s\" exists. skipping" % filename_long)

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
