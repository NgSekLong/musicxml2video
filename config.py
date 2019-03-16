##############For analyzing musicxml##################

#xml file name
xml_file_name = 'input/ttfaf.xml'

#Sound level change of different parts
part_strength = {
    'P1': -4,
    'P2': -12,
}

part_instrument = {
    'P1': 'input/ahhh',
    'P2': 'input/ahhh',
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
total_duration = 500000
#total_duration = 8000

#Divisino the duration to make control the speed of the video & audio
speed_control = 80

segment_duration = 4000
audio_only = False

extended_note = {
    'notes': [1,3,5],
    'octave': 5,
    'duration': 2,
}

#############For Audio Only##########################
#Currently none!


############For Video Only##########################
subvideo = {
    'x_max': 1300,
    'y_max': 500,
}

# 6 core => Video process total duration: 166.392323017
multiprocessing_max_core = 6


background_video = 'input/flame_4s.mp4'
