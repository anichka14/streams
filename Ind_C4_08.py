import random
import threading
import logging
from time import sleep, time


"""C4.08. Ресторан має N кухарів. Через випадковий час від T1 до T2 до ресторану 
приходить клієнт, робить замовлення та буде очікувати поки готується страва одним 
з кухарів. Час готування кожної страви – випадкове число від T3 до T4. У випадку
коли всі кухарі зайняті, клієнт очікує доки якийсь кухар не звільниться та після цього 
робить замовлення. Промоделювати роботу ресторану та визначити кількість 
клієнтів, які будуть очікувати на звільнення кухаря більше ніж заданий поріг T5 
одиниць часу. Кожен клієнт – це 1 потік."""


logging.basicConfig(level=logging.DEBUG)

N = 2  # кількість кухарів
semaphore = threading.Semaphore(N)

lock = threading.Lock()
start = time()
q = 0  # кількість клієнтів, у яких прийняли замовлення та які очікують на страви
result = 0  # кількість клієнтів, які будуть очікувати на звільнення кухаря більше ніж заданий поріг T5 одиниць часу


def log(message):
    t = time() - start
    name = threading.current_thread().getName()
    logging.debug("[%6.3f] %s: %s", t, name, message)


def client(arr_time, wait_time, time_limit):
    global q, result
    sleep(arr_time)  # час надходження
    log("зайшов у ресторан")
    start_waiting = 0

    with lock:
        if q == N:
            start_waiting = time()
            log("очікує, бо всі кухарі зайняті.")
    with semaphore:
        with lock:
            q += 1
            if start_waiting:
                stop = time()
                if stop - start_waiting > time_limit:
                    log(f"очікував занадто довго: {stop - start_waiting}.")
                    result += 1
        log("робить замовлення.")
        sleep(wait_time)
        with lock:
            q -= 1
    log("отримав своє замовлення.")


if __name__ == "__main__":
    n = 10
    T1 = 3
    T2 = 5
    T3 = 0
    T4 = 2
    T5 = 7
    threads = []
    for i in range(n):
        arrive_time = random.random() * (T4 - T3) + T3
        waiting_time = random.random() * (T2 - T1) + T1
        thread = threading.Thread(
            name=f"Клієнт {i}",
            target=client,
            args=(
                arrive_time,
                waiting_time,
                T5
            )
        )
        threads.append(thread)
        print(
            f"Клієнт {i} заходить до ресторану о {arrive_time:6.3f} та "
            f"отримує замовлення за {waiting_time:6.3f}"
        )
    for i in range(n):
        threads[i].start()
    for i in range(n):
        threads[i].join()
    log("Всі клієнти отримали свої замовлення.")

    print("Кількість клієнтів, які довго очікували на звільнення кухаря: ", result)
