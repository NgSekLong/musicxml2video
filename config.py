##############For analyzing musicxml##################

#xml file name
xml_file_name = 'input/heisapirate.xml'

#Sound level change of different parts
part_strength = {
    'P1': -4,
    'P2': -12,
}

part_instrument = {
    'P1': 'input/yee1',
    'P2': 'input/yee1',
}

#Note to number transformation
transform_note_to_number = {
    'C' : 1,
    'D' : 3,
    'E' : 5,
    'F' : 6,
    'G' : 8,
    'A' : 10,
    'B' : 12,
}

max_octave = 7
min_octave = 2

##############For both Audio and Video################
#Set it to very high to make sure the whole video & audio is being heard
total_duration = 1000000
#total_duration = 8000

#Divisino the duration to make control the speed of the video & audio
speed_control = 12

segment_duration = 4000
audio_only = False

extended_note = {
    'enabled' : False,
    'notes': [1,3,5],
    'octave': 5,
    'duration': 2,
}

#############For Audio Only##########################
audio_file_suffix = 'mp3'

############For Video Only##########################
background_video = 'input/pirate_ship_1980_4s.mp4'

video_batch = {
    'limit' : 95,
}
one_video_only = {
    'enabled' : True,
}
subvideo = {
    'x_min': -400,
    'y_min': -100,
    'x_max': 1500,
    'y_max': 700,
}

green_screen = {
    'enabled' : True,
    'color' : '00ff00',
    'similarity' : '0.05',
    'blend' : '1',
}
#is_remove_green_screen = True
multiprocessing = {
    'enabled' : True,
    'max_core' : 2,
}

#panic, error, warning, info
ffmpeg = {
    'error_level' : 'error',
    'threads' : 3,
}
