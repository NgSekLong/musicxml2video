from multiprocessing import Process, current_process

import os
import time


def square(number):
    result = number * number
    #time.sleep(1)
    # We can use the "os" module in Python to print out the Process ID
    process_id = current_process().name
    print("Process ID: " + str(process_id))

    print("The number " + str(number) + " squares to " + str(result))

if __name__ == '__main__':
    processes = []
    numbers = range(100)

    for number in numbers:
        process = Process(target=square, args=(number,))
        #square(number)
        processes.append(process)

        # Processes are spawned by created a Process object and
        # then calling its start() method.
        process.start()
    process.join()
    print('end')
