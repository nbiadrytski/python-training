import queue
import threading
import time
import random
import datetime


employees = [(0, 'Директор'),
         (1, 'Бухгалтер 1'),
         (1, 'Бухгалтер 2'),
         (50, 'Начальник IT отдела'),
         (60, 'Главный программист'),
         (70, 'Программист'),
         (75, 'Дизайнер'),
         (99, 'Уборщик')]

random.shuffle(employees)


def worker(que):
    while True:
        job = que.get()  # получаем задание из очереди в виде кортежа (приоритет, должность)
        # Выводим информацию о начале обслуживания сотрудника
        print(f'[+] {job[1]} начал обслуживаться в {datetime.datetime.now().strftime("%H:%M:%S")}')
        time.sleep((100 - job[0]) / 10)
        print(f'[-] {job[1]} закончил обслуживаться в {datetime.datetime.now().strftime("%H:%M:%S")}')
        que.task_done()


q = queue.PriorityQueue()  # Создаем приоритетную очередь и наполняем ее заданиями
for item in employees:
    q.put(item)

for i in range(2):  # Создаем 2 потока которые будут обслуживать очередь.
    t = threading.Thread(target=worker, args=(q,))
    t.setDaemon(True)
    t.start()

q.join()  # Блокируем выполнение программы до выполнения всех заданий в очереди

# [+] Директор начал обслуживаться в 12:14:15
# [+] Бухгалтер 1 начал обслуживаться в 12:14:15
# [-] Бухгалтер 1 закончил обслуживаться в 12:14:25
# [+] Бухгалтер 2 начал обслуживаться в 12:14:25
# [-] Директор закончил обслуживаться в 12:14:25
# [+] Начальник IT отдела начал обслуживаться в 12:14:25
# [-] Начальник IT отдела закончил обслуживаться в 12:14:30
# [+] Главный программист начал обслуживаться в 12:14:30
# [-] Главный программист закончил обслуживаться в 12:14:34
# [+] Программист начал обслуживаться в 12:14:34
# [-] Бухгалтер 2 закончил обслуживаться в 12:14:35
# [+] Дизайнер начал обслуживаться в 12:14:35
# [-] Программист закончил обслуживаться в 12:14:37
# [+] Уборщик начал обслуживаться в 12:14:37
# [-] Уборщик закончил обслуживаться в 12:14:37
# [-] Дизайнер закончил обслуживаться в 12:14:38
