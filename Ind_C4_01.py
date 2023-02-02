import threading
import logging
from queue import Queue
from time import sleep, perf_counter

"""C4.01. У файлі F містяться текст. Один потік раз в T1 одиниць часу зчитує один
рядок файлу F та передає в чергу. Два інших потоки отримують рядки з черги та
обробляють кожен рядок за T2 та T3 одиниць часу, відповідно. Обробка рядка – це
його запис у окремий файл (для кожного потоку різний)."""

logging.basicConfig(level=logging.DEBUG)

q = Queue()
start = perf_counter()


def open_and_read_file(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        text = f.read().split("\n")
        return text


def write_file(file_name, text):
    with open(file_name, "a+", encoding="utf-8") as f:
        f.write(text + "\n")


def log(text):  # відслідковуємо роботу потоків
    t = perf_counter() - start  # поточний час (коли було зроблено виклик)
    name = threading.current_thread().getName()
    logging.debug("[%6.3f] %s: %s", t, name, text)


def reader(file_name, process_time):
    text = open_and_read_file(file_name=file_name)
    for i in range(len(text)):
        sleep(process_time)
        log(f"Рядок {i}: '{text[i]}' зчитано.")
        q.put((text[i], i))
    q.put(None)


def consumer_1(process_time):
    while True:
        item = q.get()
        if not item:
            q.put(None)
            break
        text, i = item
        log(f"Рядок {i}: '{text}' отримано з черги.")
        write_file("output1.txt", text)
        log(f"Рядок {i}: '{text}' оброблено.")
        sleep(process_time)
        q.task_done()


def consumer_2(process_time):
    while True:
        item = q.get()
        if not item:
            q.put(None)
            break
        text, i = item
        log(f"Рядок {i}: '{text}' отримано з черги.")
        write_file("output2.txt", text)
        log(f"Рядок {i}: '{text}' оброблено.")
        sleep(process_time)
        q.task_done()


if __name__ == "__main__":
    T1 = 3
    T2 = 1
    T3 = 1
    th1 = threading.Thread(name="Перший потік", target=reader, args=("file.txt", T1))
    th2 = threading.Thread(name="Другий потік", target=consumer_1, args=(T2,))
    th3 = threading.Thread(name="Третій потік", target=consumer_2, args=(T3,))

    th2.start()
    logging.debug(f"start {th2}")
    th3.start()
    logging.debug(f"start {th3}")
    th1.start()
    logging.debug(f"start {th1}")
    th1.join()
    th2.join()
    th3.join()
    logging.debug(f"finish {th1}")
    logging.debug("Кінець!")
