import vk_api
from vk_api import audio
import vlc
import time
import os

from spinner import spin

REQUEST_STATUS_CODE = 200
name_dir = 'music_vk'
login = 'your_login'
password = 'your_password'
my_id = 'your_vk_id'

vk_session = vk_api.VkApi(login=login, password=password)
vk_session.auth()
vk = vk_session.get_api()  # Теперь можно обращаться к методам API как к обычным
# классам
vk_audio = audio.VkAudio(vk_session)  # Получаем доступ к audio


def download(path, artist, song):
    print("Searching for \"{} - {}\"".format(artist, song))
    res = list(vk_audio.search("{} - {}".format(artist, song)))
    if len(res) >= 1:
        url = res[0]['url']
        artist = res[0]['artist']
        song = res[0]['title']
    else:
        return 1
    print ("Search success, file found: \"{} - {}\"".format(artist, song))

    filename_short = "{}-{}.mp3".format(artist, song)
    filename_long = os.path.join(path, filename_short)
    if os.path.exists(filename_long):
        print("File \"%s\" exists. skipping" % filename_long)

    print("Preparing for downloading corresponding mp3")
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
    while(p.get_state() != 6):
        spin()

    print("Download finished")

    p.stop()
    p.release()
    inst.release()
    return 0