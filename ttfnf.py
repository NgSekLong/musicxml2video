import xml.etree.ElementTree as ET

#Transform Note to Number
transform_note_to_number = {
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
    tree = ET.parse('input/ttfaf.xml')
    root = tree.getroot()

    note_stream = []
    #Sound level change of different parts
    part_strang = {
        'P1': -4,
        'P2': -12,
    }

    time_pointer = 0
    for part in root:
        if part.tag == 'part':
            time_pointer = 0
            note_strength = part_strang[part.attrib['id']]
            for measure in part:
                for note in measure :
                    single_note = {}
                    if note.tag == 'note':
                        #print('Note info:')
                        duration = note.find('duration')
                        single_note['duration'] = int(duration.text)
                        if not(note.find('chord') is None):
                            #If if chord, remove previous
                            time_pointer -= int(duration.text)
                        single_note['start'] = time_pointer
                        time_pointer += int(duration.text)

                        #print('duration', duration.text)
                        pitch =  note.find('pitch')
                        altered_octave = 0
                        if not (pitch is None):
                            step = pitch.find('step')
                            if not (step is None):
                                single_note['step'] = step.text
                                single_note['step_note'] = transform_note_to_number[step.text]
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
                        #single_note['note'] = 'input/c.mp4'
                        note_stream.append(single_note)
                    elif note.tag == 'backup':
                        #print(note.tag, note.attrib)
                        duration = note.find('duration')
                        time_pointer -= int(duration.text)
    #Reverse to make high sound in top of overlay
    note_stream.reverse()
    return note_stream
