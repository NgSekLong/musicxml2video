import ffmpeg
import random
import os
import time
from musicxml_processor import note_to_file
import config
from multiprocessing import Process, Manager


def segment_video_mutliprocess(segment, segment_video_infos, start_timestamp, all_video_path_dict):
    for segment_video_info in segment_video_infos:

        segment_start = segment_video_info['segment_start']
        step_note = segment_video_info['step_note']
        note_instrument = segment_video_info['note_instrument']
        duration = segment_video_info['duration']
        octave = segment_video_info['octave']


        segment_video_path = "tmp/"+start_timestamp+"/video_" +str(segment).zfill(3)+ ".mp4"
        all_video_path_dict[segment] = segment_video_path

        segment_video = None
        if os.path.exists(segment_video_path):
            os.rename(segment_video_path, segment_video_path + '.old')
            segment_video = ffmpeg.input(segment_video_path + '.old')
        else:
            segment_video = ffmpeg.input(config.background_video)

        note_file = note_to_file(octave, step_note, note_instrument)

        temp_mp4 = "tmp/"+start_timestamp+"/tmp"+str(segment)+".mp4"
        #clear temp mp4
        if os.path.exists(temp_mp4):
            os.remove(temp_mp4)

        (
            ffmpeg
            .input(note_file)
            .trim(start=0, end=duration)
            .output( temp_mp4)
            .run()
        )
        #output sliced video to temp
        segment_video = ffmpeg.overlay(segment_video,
            ffmpeg.input(temp_mp4,itsoffset = segment_start/float(1000)),
            x=random.randint(1,config.subvideo['x_max']),
            y=random.randint(1,config.subvideo['y_max']),
            eof_action='pass'
        )
        segment_video = ffmpeg.trim(segment_video, start=0, end=config.segment_duration / float(1000))
        segment_video = ffmpeg.output(segment_video, segment_video_path)
        ffmpeg.run(segment_video)

def video_process(notes, start_timestamp):
    video_start_time = time.time()
    all_video_path = set()
    all_segment_video_infos = {}
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

        segment_video_info = {
            "segment_start" : segment_start,
            "step_note" : note['step_note'],
            "note_instrument" : note['note_instrument'],
            "octave" : note['octave'],
            "duration" : note['duration'],
        }
        if not (segment in all_segment_video_infos):
            all_segment_video_infos[segment] = []
        all_segment_video_infos[segment].append(segment_video_info)

    print('all_segment_video_infos', all_segment_video_infos)
    processes = []

    manager = Manager()
    all_video_path_dict = manager.dict()
    for segment, segment_video_infos in all_segment_video_infos.items():
        process = Process(target=segment_video_mutliprocess, args=(segment, segment_video_infos, start_timestamp, all_video_path_dict))
        processes.append(process)

        # Processes are spawned by created a Process object and
        # then calling its start() method.
        process.start()
    for process in processes:
        process.join()

    print ('all_video_path_dict.values', all_video_path_dict.values())


    #########Combine Video together###################3
    list_path = 'tmp/'+start_timestamp+'/combine_list.txt'
    combine_list = open(list_path,'a')
    # dict to list
    all_video_path = []
    for key, value in all_video_path_dict.items():
        temp = [key,value]
        all_video_path.append(value)

    # Sort the list
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
    video_end_time = time.time()
    video_elapsed = video_end_time - video_start_time

    print("Video process total duration: " + str(video_elapsed))
