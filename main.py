import os
import time
import datetime
from musicxml_processor import get_formated_notes, note_to_file
from audio_process import audio_process
from video_process import video_process
import config


############ Main Process ####################
if __name__ == '__main__':
    start_timestamp = str(int(time.time()))
    directory = 'tmp/'+start_timestamp
    if not os.path.exists(directory):
        os.makedirs(directory)
    notes = get_formated_notes()
    audio_process(notes, start_timestamp)
    if config.audio_only == False:
        video_process(notes, start_timestamp)
