OUTPUT_DIR = 'data/output'
FAILED_DIR = 'data/failed'
INPUT_DIR = 'data/input'
WORK_DIR = 'data/work'

REVERSE_BCD = False

PROCESSES = 8

from os import makedirs, listdir, path, unlink
import time
from shutil import move
from multiprocessing import Process
from Queue import Queue
from threading import Thread
import json
import sys

import psmcdr

def convert(filename):
    """CDR->JSON conversion, move to output"""
    input_path = path.join(WORK_DIR, filename)
    work_path = input_path + '.json'
    output_path = path.join(OUTPUT_DIR, filename + '.json')
    data = file(input_path).read()
    result = psmcdr.parseCdrs(data, reverseBcd=REVERSE_BCD)
    output = json.dumps(result, sort_keys=True, indent=4)
    file(work_path, 'w+').write(output)
    move(work_path, output_path)
    unlink(input_path)

def worker(queue):
    """Listens to the queue and dispatches the converter for each job"""

    while True:
        f = queue.get()
        if f is None:
            break
        print 'got %s' % f
        p = Process(target=convert, args=(f,))
        p.start()
        p.join()
        print '%s converted' % f

if __name__ == '__main__':
    # Daemon mode if --daemon is set. Otherwise just run once (e.g. from cron)
    if len(sys.argv) > 1 and sys.argv[1] == '--daemon':
        daemon = True
    else:
        daemon = False

    # Create directories if necessary
    for d in OUTPUT_DIR, FAILED_DIR, INPUT_DIR, WORK_DIR:
        if not path.isdir(d):
            makedirs(d)

    # Set up job queue. New files go in here after being moved to WORK_DIR
    queue = Queue()

    # Create a pool of workers and start them
    pool = [Thread(target=worker, args=(queue,)) for _ in range(PROCESSES)]
    map(lambda x: x.setDaemon(True), pool)
    map(lambda x: x.start(), pool)

    # Monitor input directory for new files
    while True:
        for f in [x for x in listdir(INPUT_DIR) if x.endswith('.cdr')]:
            move(path.join(INPUT_DIR, f), path.join(WORK_DIR, f))
            queue.put(f)
        if not daemon:
            break
        time.sleep(1)

    # Close workers (You only ever get here if not daemon)
    for _ in range(PROCESSES):
        queue.put(None)

