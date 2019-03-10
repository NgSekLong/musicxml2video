import ffmpeg
from pydub import AudioSegment
import random
import os
import time
from ttfnf import get_note_stream


#print (get_note_stream())
# notes = [{
#     'note': 'input/g.mp4',
#     'start': 0,
#     'duration': 3,
# },{
#     'note': 'input/c.mp4',
#     'start': 5,
#     'duration': 1,
# },
# {
#     'note': 'input/c.mp4',
#     'start': 3,
#     'duration': 1,
# }]

#Set to a very high number for full song production
#TOTAL_DURATION = 60000
TOTAL_DURATION = 10000000

SEGMENT_DURATION = 4000

SUBVIDEO_X_MAX = 1300
SUBVIDEO_Y_MAX = 500

BACKGROUND_IMAGE = 'input/flame_4s.mp4'

def note_to_file(octave, step_note):
    #temp change octave
    if octave < 3:
        octave = 3
    if octave > 6:
        octave = 6
    return 'input/music/' + str(octave) + '/' + str(step_note) + '.mp4'

def get_formate_notes():
    musicxml_notes = get_note_stream()
    #musicxml_notes = get_note_stream()[:50]
    notes = []
    common_division = 80
    #common_division = 25

    for note in musicxml_notes:
        new_note = {
            'duration': (note['duration'] *1.1) / float(common_division),
            'start': note['start'] / float(common_division),
            'note_strength': note['note_strength'],
            #'step': note['step'],
        }
        if 'step' in note:
            new_note['step'] = note['step']
        if 'step_note' in note:
            new_note['step_note'] = note['step_note']
        if 'ori_octave' in note:
            new_note['ori_octave'] = note['ori_octave']
        if 'octave' in note:
            new_note['octave'] = note['octave']
        if 'alter' in note:
            new_note['alter'] = note['alter']
        notes.append(new_note)

    #print(notes)
    for note in notes:
        print(note)
    return notes


###########Audio part####################
def audio_process(notes, start_timestamp):
    output_audio = AudioSegment.silent(350000)# AudioSegment.from_file("g.mp4", "mp4")
    for note in notes:
        if not ('step_note' in note):
            #Slient sound
            continue
        note_file = note_to_file(note['octave'], note['step_note'])
        print(note_file)
        duration = 1000 * note['duration']
        duration = int(duration)
        start = 1000 * note['start']
        start = int(start)
        if start > TOTAL_DURATION:
            #Temp continue to test full song
            continue
        audio = AudioSegment.from_file(note_file, "mp4")
        audio = audio[:duration]
        audio = AudioSegment.silent(start) + audio
        if note['note_strength'] != 0:
            audio = audio + note['note_strength']
        output_audio = output_audio.overlay(audio)
        #Change strength:
        print('Processing Audio: Start: ',start, 'Duration:',duration)
    output_audio.export("tmp/"+start_timestamp+"/sound.wav", format="wav")
    #exit()

#############Video part################3
def video_process(notes, start_timestamp):
    #stream = ffmpeg.input('input/background.mp4')
    # stream = ffmpeg.input('input/black.mp4')
    # stream = ffmpeg.output(stream, 'tmp/'+start_timestamp+'/processing_1.mp4')
    # ffmpeg.run(stream)
    all_video_path = set()
    for note in notes:
        if not ('step_note' in note):
            #Slient sound
            continue

        start = 1000 * note['start']
        start = int(start)


        if start > TOTAL_DURATION:
            #Temp continue to test full song
            continue

        segment = int(start / float(SEGMENT_DURATION))
        segment_start = int(start - segment * SEGMENT_DURATION)

        segment_video_path = "tmp/"+start_timestamp+"/video_" +str(segment).zfill(3)+ ".mp4"
        all_video_path.add(segment_video_path)
        segment_video = None
        if os.path.exists(segment_video_path):
            os.rename(segment_video_path, segment_video_path + '.old')
            segment_video = ffmpeg.input(segment_video_path + '.old')
        else:
            segment_video = ffmpeg.input(BACKGROUND_IMAGE)

        print('segment', segment, 'segment_start',segment_start, 'start', start)
        #continue
        #stream = ffmpeg.input('tmp/'+start_timestamp+'/processing_1.mp4')
        note_file = note_to_file(note['octave'], note['step_note'])
        #clear temp mp4
        if os.path.exists("tmp/"+start_timestamp+"/tmp.mp4"):
            os.remove("tmp/"+start_timestamp+"/tmp.mp4")

        (
            ffmpeg
            .input(note_file)
            .trim(start=0, end=note['duration'])
            .output( 'tmp/'+start_timestamp+'/tmp.mp4')
            #.output('output.mp4')
            .run()
        )
        #exit()
        #output sliced video to temp
        #
        segment_video = ffmpeg.overlay(segment_video,
            ffmpeg.input('tmp/'+start_timestamp+'/tmp.mp4',itsoffset = segment_start/float(1000)),
            x=random.randint(1,SUBVIDEO_X_MAX),
            y=random.randint(1,SUBVIDEO_Y_MAX),
            eof_action='pass'
        )
        segment_video = ffmpeg.trim(segment_video, start=0, end=SEGMENT_DURATION / float(1000))
        segment_video = ffmpeg.output(segment_video, segment_video_path)
        ffmpeg.run(segment_video)


        # os.remove("tmp/"+start_timestamp+"/processing_1.mp4")
        # os.rename('tmp/'+start_timestamp+'/processing_2.mp4','tmp/'+start_timestamp+'/processing_1.mp4')
        #exit()
    # stream = ffmpeg.output(stream, 'tmp/output_without_sound.mp4')
    # ffmpeg.run(stream)

    #########Combine Video together###################3
    list_path = 'tmp/'+start_timestamp+'/combine_list.txt'
    combine_list = open(list_path,'a')
    all_video_path = sorted(all_video_path)
    for video_path in all_video_path:
        combine_list.write("file '../../" + video_path + "'" + '\n')
    combine_list.close()

    os.system("ffmpeg -f concat -safe 0 -i "+list_path+" -c copy tmp/"+start_timestamp+"/combine_video.mp4")

    # (
    #     ffmpeg
    #     .input('tmp/mylist.txt', format='concat', safe=0)
    #     #.filter('concat')
    #     .trim(start=0, end=note['duration'])
    #     .output( 'tmp/'+start_timestamp+'/combined_video.mp4', c='copy')
    #     #.output('output.mp4')
    #     .run()
    # )
    #exit()

    # combine_video = ffmpeg.input('input/black.mp4')
    # # for video_path in all_video_path:
    # #     combine_video = ffmpeg.concat(combine_video, ffmpeg.input(video_path))
    # for video_path in all_video_path:
    #     #combine_video = ffmpeg.concat(combine_video, **[ffmpeg.input(video_path)])
    #     combine_video = ffmpeg.input(combine_video, format='concat', safe=0)
    # combine_video = ffmpeg.output(combine_video, 'tmp/'+start_timestamp+'/combined_video.mp4', c='copy')
    # ffmpeg.run(combine_video)

    # (
    #     ffmpeg
    #     .concat(
    #         in_file.trim(start_frame=10, end_frame=20),
    #         in_file.trim(start_frame=30, end_frame=40),
    #     )
    #     .overlay(overlay_file.hflip())
    #     .drawbox(50, 50, 120, 120, color='red', thickness=5)
    #     .output('out.mp4')
    #     .run()
    # )
    #exit()


    # (
    #     ffmpeg
    #     .input('c.mp4')
    #     .overlay(
    #         ffmpeg.input('g_20_20.mp4',itsoffset = 1)
    #     , x=100)
    #     #.filter('amerge', inputs = 2['a'],)
    #     .output( 'output_without_sound.mp4')
    #     #.output('output.mp4')
    #     .run()
    # )

    (
        ffmpeg
        #.filter('amerge', inputs = 2['a'],)
        .output(ffmpeg.input('tmp/'+start_timestamp+'/combine_video.mp4'),
            ffmpeg.input('tmp/'+start_timestamp+'/sound.wav')['a'], 'output_'+start_timestamp+'.mp4')
        #.output('output.mp4')
        .run()
    )
    #os.remove("tmp/sound.wav")
    #os.remove("tmp/processing_1.mp4")


############ Main Process ####################



start_timestamp = str(int(time.time()))
directory = 'tmp/'+start_timestamp
if not os.path.exists(directory):
    os.makedirs(directory)

notes = get_formate_notes()
audio_process(notes, start_timestamp)
video_process(notes, start_timestamp)
