import xml.etree.ElementTree as ET
import config

#Transform Note to Number
config.transform_note_to_number = {
    'C' : 1,
    'D' : 3,
    'E' : 5,
    'F' : 6,
    'G' : 8,
    'A' : 10,
    'B' : 12,
}



def get_note_stream():
    # This can be any musicxml file, for this time we use ttfaf.xml
    # You can get this full score here: https://musescore.com/user/10791406/scores/3320776
    tree = ET.parse(config.xml_file_name)
    root = tree.getroot()

    note_stream = []

    time_pointer = 0
    for part in root:
        if part.tag == 'part':
            time_pointer = 0
            note_strength = 0
            note_instrument = None
            if part.attrib['id'] in config.part_strength:
                note_strength = config.part_strength[part.attrib['id']]
            if part.attrib['id'] in config.part_instrument:
                note_instrument = config.part_instrument[part.attrib['id']]
            for measure in part:
                for note in measure :
                    single_note = {}
                    if note.tag == 'note':
                        duration = note.find('duration')
                        single_note['duration'] = int(duration.text)
                        if not(note.find('chord') is None):
                            #If if chord, remove previous
                            time_pointer -= int(duration.text)
                        single_note['start'] = time_pointer
                        time_pointer += int(duration.text)

                        pitch =  note.find('pitch')
                        altered_octave = 0
                        if not (pitch is None):
                            step = pitch.find('step')
                            if not (step is None):
                                single_note['step'] = step.text
                                single_note['step_note'] = config.transform_note_to_number[step.text]
                            alter = pitch.find('alter')
                            if not (alter is None):
                                single_note['alter'] = int(alter.text)
                                single_note['step_note'] = single_note['step_note'] + single_note['alter']
                                if single_note['step_note'] < 1:
                                    single_note['step_note'] += 12
                                    altered_octave=-1
                                if single_note['step_note'] < -1:
                                    single_note['step_note'] -= 12
                                    altered_octave=-1
                            octave = pitch.find('octave')
                            if not (octave is None):
                                single_note['ori_octave'] = int(octave.text)
                                single_note['octave'] = single_note['ori_octave'] + altered_octave

                        single_note['note_strength'] = note_strength
                        single_note['note_instrument'] = note_instrument

                        #single_note['note'] = 'input/c.mp4'
                        note_stream.append(single_note)
                    elif note.tag == 'backup':
                        #print(note.tag, note.attrib)
                        duration = note.find('duration')
                        time_pointer -= int(duration.text)
    #Reverse to make high sound in top of overlay
    note_stream.reverse()
    return note_stream

def get_formated_notes():
    musicxml_notes = get_note_stream()

    notes = []

    for note in musicxml_notes:
        is_need_extended_note = False
        new_note = {}
        if 'step' in note:
            new_note['step'] = note['step']
        if 'step_note' in note:
            new_note['step_note'] = note['step_note']
            if note['step_note'] in config.extended_note['notes'] and note['octave'] == config.extended_note['octave']:
                is_need_extended_note = True
        if 'ori_octave' in note:
            new_note['ori_octave'] = note['ori_octave']
        if 'octave' in note:
            new_note['octave'] = note['octave']
        if 'alter' in note:
            new_note['alter'] = note['alter']
        new_note['duration'] = (note['duration'] *1.1 * (config.extended_note['duration'] if is_need_extended_note else 1) ) / float(config.speed_control)
        new_note['start'] = note['start'] / float(config.speed_control)
        new_note['note_strength'] = note['note_strength']
        new_note['note_instrument'] = note['note_instrument']



        notes.append(new_note)

    for note in notes:
        print(note)
    return notes

def note_to_file(octave, step_note, instrument):
    #temp change octave
    if octave < 2:
        octave = 2
    if octave > 7:
        octave = 7
    return instrument + '/' + str(octave) + '/' + str(step_note) + '.mp4'
