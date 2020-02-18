import concurrent.futures as cf
import time as time
import os
import argparse
import glob
import multiprocessing as mp




def createList(file):
    works = []
    for i in range(0, len(file) + 1):
        for j in range(i + 1, len(file) + 1):
            works.append(str(i) + ',' + str(j))
    return works


def processWork(workIDs, files):
    workIDs = workIDs.split(',')
    print(f'working on {files[int(workIDs[0])]} & {files[int(workIDs[1])]}')
    time.sleep(1)
    print(f'finished working on {files[int(workIDs[0])]} & {files[int(workIDs[1])]}')

if __name__ == '__main__':
    start = time.perf_counter()
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Target directory to analyze")
    parser.add_argument("fileextension", help="What Type of file")

    args = parser.parse_args()
    targetDir = os.path.abspath(args.directory)
    ext = args.fileextension
    files = []
    for r, d, f in os.walk(targetDir):
        for item in f:
            if '.' + ext in item:
                files.append(item)

    works = createList(files)
    print(files)

    with cf.ProcessPoolExecutor() as executor:
        results = [executor.submit(processWork, work, files) for work in works]

    for f in cf.as_completed(results):
        print(f.result())