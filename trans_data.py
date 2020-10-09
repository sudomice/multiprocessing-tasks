import os.path
import requests
import threading
import multiprocessing
from datetime import datetime
import csv


URL = "<some get url>"

def thread_worker(in_q, count):
    # Each thread performs the actual work. In this case, we will assume
    # that the work is to fetch a given URL API call and write to csv.
    filename = f'{threading.current_thread().name}-{count}.csv'
    field_names= ['description', 'merchant_name', 'merchant_website', 'merchant_logo', 'clean_name']
    file_exists = os.path.isfile(filename)

    while True:
        task = in_q.get()
        if task is None:
            break
        line_count = task[0]
        sample = task[1]
        print(line_count)
        resp = dict(requests.get(URL+sample).json())
        resp['description'] = sample
        with open('data/'+filename, 'w+') as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            if not file_exists:
                writer.writeheader()
            try:
                writer.writerow(resp)
            except ValueError:
                print(resp)


def process_woker(threads, in_q, count):
    # Start thread workers.
    thread_workers = []
    for ii in range(threads):
        w = threading.Thread(target=thread_worker, args=(in_q, str(ii)+count,))
        w.start()
        thread_workers.append(w)

    # Wait for thread workers to terminate.
    for w in thread_workers:
        w.join()

def main():
    processes = 4
    threads = 50
    process_workers = []
    in_q = multiprocessing.Queue()

    for count in range(processes):
        w = multiprocessing.Process(target=process_woker, args=(threads, in_q, str(count)))
        w.start()
        process_workers.append(w)
    with open('test.csv', 'r') as f:
        reader = csv.reader(f)
        line_count = 0
        for row in reader:
            if line_count == 0:
                pass
            else:
                in_q.put((line_count, row[0]))
            line_count += 1

    # Send sentinel for each thread worker to quit.
    for _ in range(processes * threads):
        in_q.put(None)

    # Wait for workers to terminate.
    for w in process_workers:
        w.join()

if __name__ == "__main__":
    main()