import os
from multiprocessing import Pool
import sys




start_timestamp = str(int(time.time()))
directory = 'tmp/'+start_timestamp
if not os.path.exists(directory):
    os.makedirs(directory)

notes = get_formate_notes()
audio_process(notes, start_timestamp)


processes = ['audio_process.py', 'audio_process.py', 'audio_process.py']


def run_process(process):
    os.system('python {}'.format(process))


pool = Pool(processes=3)
pool.map(run_process, processes)
