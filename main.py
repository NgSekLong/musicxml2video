import ffmpeg
from pydub import AudioSegment
import random
import os
import time
from musicxml_processor import get_formated_notes, note_to_file

import config


###########Audio part####################
audio_cache = {}
audio_segment = {}
#Implement a audio caching
def check_audio_cache(octave, step_note, note_file):

    key = str(octave) + '-' + str(step_note)
    if key in audio_cache:
        return audio_cache[key]
    audio_cache[key] = AudioSegment.from_file(note_file, "mp4")
    return audio_cache[key]
def insert_to_audio_segment(start, audio):
    segment = int(start / float(config.segment_duration))
    segment_start = int(start - segment * config.segment_duration)
    key = segment
    segment_audio = None
    if key in audio_segment:
        segment_audio = audio_segment[key]
    else:
        segment_audio = AudioSegment.silent(config.segment_duration * float(1.5) )
    audio = AudioSegment.silent(segment_start) + audio
    segment_audio = segment_audio.overlay(audio)
    audio_segment[key] = segment_audio


def audio_process(notes, start_timestamp):
    #output_audio = AudioSegment.silent(400000)
    audio_start_time = time.time()
    max_audio_duration = 0
    for note in notes:
        if not ('step_note' in note):
            #Slient sound
            continue
        note_file = note_to_file(note['octave'], note['step_note'], note['note_instrument'])
        #print(note_file)
        duration = 1000 * note['duration']
        duration = int(duration)
        start = 1000 * note['start']
        if start > max_audio_duration:
            max_audio_duration = start
        start = int(start)
        if start > config.total_duration:
            #Control video length
            continue
        #audio = AudioSegment.from_file(note_file, "mp4")
        audio = check_audio_cache(note['octave'], note['step_note'], note_file)
        audio = audio[:duration]
        #audio = AudioSegment.silent(start) + audio
        if note['note_strength'] != 0:
            audio = audio + note['note_strength']
        #output_audio = output_audio.overlay(audio)
        insert_to_audio_segment(start, audio)
        #Change strength:
        print('Processing Audio: Start: ',start, 'Duration:',duration)

    print('Process patching segmented audio finished')
    max_audio_duration = max_audio_duration + 4000
    output_audio = AudioSegment.silent(max_audio_duration)
    for segment, segment_audio in audio_segment.items():
        print('Processing Audio: Segment: ',segment, 'Segment Duration:',config.segment_duration)
        total_segment_audio = AudioSegment.silent(segment * config.segment_duration) + segment_audio
        output_audio = output_audio.overlay(total_segment_audio)
        #output_audio = AudioSegment.silent(segment * config.segment_duration) + segment_audio
    output_audio.export("tmp/"+start_timestamp+"/sound.wav", format="wav")

    audio_end_time = time.time()
    audio_elapsed = audio_end_time - audio_start_time

    print("Audio process total duration: " + str(audio_elapsed))

#############Video part################3
def video_process(notes, start_timestamp):
    all_video_path = set()
    for note in notes:
        if not ('step_note' in note):
            #Slient sound
            continue

        start = 1000 * note['start']
        start = int(start)


        if start > config.total_duration:
            #Control video length
            continue

        segment = int(start / float(config.segment_duration))
        segment_start = int(start - segment * config.segment_duration)

        segment_video_path = "tmp/"+start_timestamp+"/video_" +str(segment).zfill(3)+ ".mp4"
        all_video_path.add(segment_video_path)
        segment_video = None
        if os.path.exists(segment_video_path):
            os.rename(segment_video_path, segment_video_path + '.old')
            segment_video = ffmpeg.input(segment_video_path + '.old')
        else:
            segment_video = ffmpeg.input(config.background_video)

        print('segment', segment, 'segment_start',segment_start, 'start', start)
        note_file = note_to_file(note['octave'], note['step_note'], note['note_instrument'])
        #clear temp mp4
        if os.path.exists("tmp/"+start_timestamp+"/tmp.mp4"):
            os.remove("tmp/"+start_timestamp+"/tmp.mp4")

        (
            ffmpeg
            .input(note_file)
            .trim(start=0, end=note['duration'])
            .output( 'tmp/'+start_timestamp+'/tmp.mp4')
            .run()
        )
        #output sliced video to temp
        #
        segment_video = ffmpeg.overlay(segment_video,
            ffmpeg.input('tmp/'+start_timestamp+'/tmp.mp4',itsoffset = segment_start/float(1000)),
            x=random.randint(1,config.subvideo['x_max']),
            y=random.randint(1,config.subvideo['y_max']),
            eof_action='pass'
        )
        segment_video = ffmpeg.trim(segment_video, start=0, end=config.segment_duration / float(1000))
        segment_video = ffmpeg.output(segment_video, segment_video_path)
        ffmpeg.run(segment_video)


    #########Combine Video together###################3
    list_path = 'tmp/'+start_timestamp+'/combine_list.txt'
    combine_list = open(list_path,'a')
    all_video_path = sorted(all_video_path)
    for video_path in all_video_path:
        combine_list.write("file '../../" + video_path + "'" + '\n')
    combine_list.close()

    os.system("ffmpeg -f concat -safe 0 -i "+list_path+" -c copy tmp/"+start_timestamp+"/combine_video.mp4")

    (
        ffmpeg
        .output(ffmpeg.input('tmp/'+start_timestamp+'/combine_video.mp4'),
            ffmpeg.input('tmp/'+start_timestamp+'/sound.wav')['a'], 'tmp/'+start_timestamp+'/output.mp4' )
        .run()
    )


############ Main Process ####################



start_timestamp = str(int(time.time()))
directory = 'tmp/'+start_timestamp
if not os.path.exists(directory):
    os.makedirs(directory)

notes = get_formated_notes()
audio_process(notes, start_timestamp)
if config.audio_only == False:
    video_process(notes, start_timestamp)
