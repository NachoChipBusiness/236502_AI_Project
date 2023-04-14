# System and processes imports
import os
import time

# Code design imports
from typing import List, Dict

# Audio analysis imports
import asyncio
from shazamio import Shazam

import spotipy
import spotipy.oauth2 as oauth2

# Dataset imports
import pandas as pd
import re

# Root directory of audio files
AUDIO_FILES_DIRECTORY: str = os.path.join(os.getcwd(), ".misc\\original_gtzan_dataset\\Data\\genres_original")

# ================ First Step: Song Recognition ================ #
async def create_song_recognition_generator(filename: str):
    '''
    Create Shazam generator that will focus on identifying the song kept under the given filename
    :param filename: The path to the audio file
    :return: asynchronous shazam generator for given audio filename
    '''
    shazam = Shazam()
    result = await shazam.recognize_song(filename)
    return result

def identify_song(filename: str) -> Dict[str, str]:
    try:
        generator = create_song_recognition_generator(filename)
        generator_loop = asyncio.get_event_loop()

        start_timer = time.time()
        raw_info = generator_loop.run_until_complete(generator)
        finish_timer = time.time()

        song_info = {"filename": os.path.basename(filename), "song": raw_info["track"]["title"], "artist":raw_info["track"]["subtitle"], "calculation_time":finish_timer-start_timer, "raw_info":raw_info}

    except:
        song_info = {"filename": os.path.basename(filename), "song": None, "artist":None, "calculation_time":-1, "raw_info":None}

    return song_info

def identify_songs_in_database():
    songs_info: List[Dict[str, str]] = []

    # Iterate over all of the audio files in the directory tree
    for root, dirs, files in os.walk(AUDIO_FILES_DIRECTORY):
        for filename in files:
            if filename.endswith('.wav'):
                songs_info.append(identify_song(os.path.join(root, filename)))

    songs_df = pd.DataFrame(songs_info)
    songs_df.to_csv("shazamio_filenames_songs.csv", index=False, encoding='utf-8')

def main():
    identify_songs_in_database()

if __name__ == "__main__":
    main()
