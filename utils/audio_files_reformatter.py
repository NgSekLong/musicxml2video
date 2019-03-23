from shutil import copyfile
from os.path import expanduser
import os



OUTPUT_TO_INPUT_DIR = 'yee1'

SRC_DIR = expanduser("~") + '/Music/cleaned'

FILE_PREFIX = '1'

ORI_OCTAVE = 4

ORI_STEP_NOTE = 1



middle_step_note_position = ORI_OCTAVE * 12 + ORI_STEP_NOTE - 1
start_step_note_position = middle_step_note_position - 12 * 4
for i in range(1,96):
    step_note_position = start_step_note_position + i - 1
    octave_pointer = int(step_note_position / float(12))
    step_note_pointer = step_note_position % 12 + 1
    print('file: ' + str(i) + ' octave: ' + str(octave_pointer) + ' stepnote: ' + str(step_note_pointer))



    src_file = SRC_DIR + '/' + FILE_PREFIX + str(i).zfill(3) + '.mp3'
    des_file = os.path.dirname(os.path.realpath(__file__)) + '/../input/' + OUTPUT_TO_INPUT_DIR + '/' + str(octave_pointer) + '/' + str(step_note_pointer) + '.mp3'
    #print ('src file location: ' + src_file)
    print ('des file location: ' + des_file)

    #Make dirs
    if not os.path.exists(os.path.dirname(des_file)):
        try:
            os.makedirs(os.path.dirname(des_file))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    copyfile(src_file, des_file)
    #print(os.path.dirname(os.path.realpath(__file__)))
