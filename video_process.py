import ffmpeg
import random
import os
import time
from musicxml_processor import note_to_file
import config

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
