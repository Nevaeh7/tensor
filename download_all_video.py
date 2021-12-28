import multiprocessing.dummy
import sys
import warnings
from pathlib import Path

import pandas as pd
#from youtube_dl import YoutubeDL
from yt_dlp import YoutubeDL

warnings.filterwarnings('ignore')
# raw = False
# part = False
download_videos = False

NUMS = 80  # maximal items you can download
iMaxDuration = 600  # maximal duration in seconds
YDL_OPTIONS = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'writeautomaticsub': True,
    'writesubtitles': True,
}

download_path = "./test"
YDL_OPTIONS_AUDIO_ONLY = {
    'format': 'bestaudio[ext=m4a]',
}


def search(arg, nums):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            videos = ydl.extract_info(f"ytsearch{nums}:{arg}",
                                      download=False)['entries']
        except Exception:
            return "Network link failed!"
    return videos


def download(index):
    print("index", index)
    folder, name, action, arg = info_list[index]

    path = Path(folder) / name / action / 'videos'
    path.mkdir(exist_ok=True, parents=True)

    YDL_OPTIONS['outtmpl'] = str(path / (arg + ".mp4"))
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            video = ydl.extract_info(
                "https://www.youtube.com/watch?v={}".format(arg),
                download=True)
            YDL_OPTIONS_AUDIO_ONLY['outtmpl'] = str(path / (arg + ".m4a"))
            with YoutubeDL(YDL_OPTIONS_AUDIO_ONLY) as ydl_audio:
                audio = ydl_audio.extract_info(
                    "https://www.youtube.com/watch?v={}".format(arg),
                    download=True)
                return True
        except Exception:
            video = ydl.extract_info(
                "https://www.youtube.com/watch?v={}".format(arg),
                download=False)
            return False


def filter(arg):
    try:
        if arg["duration"] > iMaxDuration:
            return None
        else:
            return arg
    except Exception:
        return None


CPU = 10
folder, animal_name, action, id_list = "".join(sys.argv[1:]).split("||")
print(folder)
print(animal_name)
print(action)
print(id_list)

info_list = [[folder, animal_name, action] for i in range(len(id_list))]
video_index = [i for i in range(0, len(info_list))]

if download_videos:
    with multiprocessing.dummy.Pool(CPU) as pool:
        pool.map(download, video_index)