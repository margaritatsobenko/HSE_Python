from fib import find_n_fib
from multiprocessing import Process
from threading import Thread
import time


def count_synch_time(big_number, steps_number):
    start = time.time()
    for _ in range(steps_number):
        find_n_fib(big_number)
    end = time.time() - start
    return end


def count_process_time(big_number, steps_number):
    start = time.time()
    temp = []
    for _ in range(steps_number):
        cur = Process(target=find_n_fib, args=(big_number,))
        temp.append(cur)
        cur.start()

    for el in temp:
        el.join()

    end = time.time() - start
    return end


def count_thread_time(big_number, steps_number):
    start = time.time()
    temp = []
    for _ in range(steps_number):
        cur = Thread(target=find_n_fib, args=(big_number,))
        temp.append(cur)
        cur.start()

    for el in temp:
        el.join()
    end = time.time() - start
    return end


def main():
    file_name = "artifacts/easy.txt"
    with open(file_name, 'w') as t:
        t.write(f"Time when using synchronization: {count_synch_time(100000, 10):.4f}s\n")
        t.write(f"Time when using processes: {count_process_time(100000, 10):.4f}s\n")
        t.write(f"Time when using threads: {count_thread_time(100000, 10):.4f}s")


if __name__ == '__main__':
    main()
