import ffmpeg
import random
import os
import time
import datetime
from musicxml_processor import note_to_file
import config
from multiprocessing import Process, Pool, Manager
import datetime


def segment_video_mutliprocess( segment_video_infos ):
    segment_video_start_time = time.time()

    segment = segment_video_infos['segment']
    start_timestamp = segment_video_infos['start_timestamp']
    segment_video_path = "tmp/"+start_timestamp+"/video_" +str(segment).zfill(3)+ ".mp4"
    segment_video_input_file = config.background_video
    segment_video = ffmpeg.input(segment_video_input_file)
    counter = 0
    for segment_video_info in segment_video_infos['data']:
        counter+=1

        segment_start = segment_video_info['segment_start']
        step_note = segment_video_info['step_note']
        note_instrument = segment_video_info['note_instrument']
        duration = segment_video_info['duration']
        octave = segment_video_info['octave']

        if config.one_video_only['enabled']:
            note_file = note_instrument + '/video.mp4'
        else:
            note_file = note_to_file(octave, step_note, note_instrument)

        segment_video_output_file = segment_video_path
        # if os.path.exists(segment_video_path):
        #     os.rename(segment_video_path, segment_video_path + '.old')
        #     segment_video_input_file = segment_video_path + '.old'
        # else:
        #     segment_video_input_file = config.background_video

        split_preventing_offset = 1/float(counter + 1000)
        itsoffset = segment_start/float(1000) + split_preventing_offset
        x=random.randint(config.subvideo['x_min'],config.subvideo['x_max'])
        y=random.randint(config.subvideo['y_min'],config.subvideo['y_max'])
        end=config.segment_duration / float(1000)
        trim_end=itsoffset + duration



        temp_video = ffmpeg.input(note_file,itsoffset = itsoffset)
        temp_video = ffmpeg.trim(temp_video,start=0, end=trim_end )

        if config.green_screen['enabled'] == True:
            gs_color = config.green_screen['color']
            gs_similarity = config.green_screen['similarity']
            gs_blend = config.green_screen['blend']
            temp_video = ffmpeg.filter(temp_video, 'colorkey', color = gs_color, similarity = gs_similarity, blend = gs_blend)
            #output sliced video to temp
        segment_video = ffmpeg.overlay(segment_video,temp_video,x=x,y=y,eof_action='pass')
        segment_video = ffmpeg.trim(segment_video, start=0, end=end)
        # Process a batch of video
        if counter > config.video_batch['limit']:
            continue;
            print('Warning: The number of video to be process is too much ( larger than ' +str(config.video_batch['limit'])+' ), maybe need to change speed_control?')
        #print ('segment_video_info', segment_video_info)
    output_segment_video(segment_video, segment_video_path)
    # segment_video = ffmpeg.output(segment_video, segment_video_path, preset='ultrafast',
    #     loglevel=config.ffmpeg['error_level'], threads=config.ffmpeg['threads'])
    # ffmpeg.run(segment_video)


            #os.system("ffmpeg -i "+segment_video_input_file+" -itsoffset "+str(segment_start/float(1000))+" -i "+temp_mp4+" -loglevel panic -preset ultrafast -filter_complex '[1:v]colorkey=0x"+green_screen_color+":"+green_screen_similarity+":"+gs_blend+"[ckout];[0:v][ckout]overlay[out]' -map '[out]' " + segment_video_output_file)


    segment_video_end_time = time.time()
    segment_video_elapsed = segment_video_end_time - segment_video_start_time

    print('Video process segment: '  + str(segment) + ' done, total duration: '+ str(datetime.timedelta(seconds=segment_video_elapsed)))
    return segment_video_path
def output_segment_video(segment_video, segment_video_path):
    # if os.path.exists(segment_video_path):
    #     os.rename(segment_video_path, segment_video_path + '.old')
    #     segment_video_input_file = segment_video_path + '.old'
    # else:
    #     segment_video_input_file = config.background_video
    segment_video = ffmpeg.output(segment_video, segment_video_path, preset='ultrafast',
        loglevel=config.ffmpeg['error_level'], threads=config.ffmpeg['threads'])

    segment_video = ffmpeg.overwrite_output(segment_video)
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
            all_segment_video_infos[segment] = {
                "segment" : segment,
                "start_timestamp" : start_timestamp,
                "data" : [],
            }
        all_segment_video_infos[segment]["data"].append(segment_video_info)

    #change all_segment_video_infos from dict to list

    #print('all_segment_video_infos before dict to list', all_segment_video_infos)
    all_segment_video_infos_list = []
    for key, value in all_segment_video_infos.items():
        all_segment_video_infos_list.append(value)
    all_segment_video_infos = all_segment_video_infos_list
    #print('all_segment_video_infos', all_segment_video_infos)


    ######################Multiprocess by using Pool#########################
    if config.multiprocessing['enabled']:
        p = Pool(processes=config.multiprocessing['max_core'])
        #all_segment_video_infos = range(1,5)
        all_video_path = p.map(segment_video_mutliprocess, all_segment_video_infos)
        p.close()
        p.join()
    else:
        all_video_path = []
        for segment_video_infos in all_segment_video_infos:
            all_video_path.append(segment_video_mutliprocess(segment_video_infos))


    ######################Multiprocess by using Pool End#########################

    #########Combine Video together###################3
    list_path = 'tmp/'+start_timestamp+'/combine_list.txt'
    combine_list = open(list_path,'a')

    # Sort the list
    all_video_path = sorted(all_video_path)
    for video_path in all_video_path:
        combine_list.write("file '../../" + video_path + "'" + '\n')
    combine_list.close()

    os.system("ffmpeg -loglevel panic -f concat -safe 0 -i "+list_path+" -c copy tmp/"+start_timestamp+"/combine_video.mp4")

    print("Combining video segment together")
    (
        ffmpeg
        .output(ffmpeg.input('tmp/'+start_timestamp+'/combine_video.mp4',  loglevel=config.ffmpeg['error_level']),
            ffmpeg.input('tmp/'+start_timestamp+'/sound.wav')['a'], 'tmp/'+start_timestamp+'/output.mp4' )
        .run()
    )
    video_end_time = time.time()
    video_elapsed = video_end_time - video_start_time

    print("Video process total duration: " + str(datetime.timedelta(seconds=video_elapsed)))
