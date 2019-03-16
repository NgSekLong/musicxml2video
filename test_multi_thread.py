from multiprocessing import Pool

import os
import time


def sum_square(number):
    s = 0
    time.sleep(1)
    for i in range(number):
        s += i * i
    return s
if __name__ == '__main__':
    numbers = range(5)
    p = Pool()

    result = p.map(sum_square, numbers)
    print(result)

    p.close()
    p.join()

    print('end')
