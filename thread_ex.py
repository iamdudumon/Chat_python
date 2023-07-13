# import time

# def do_someting():
#     print("1초 잘랭")
#     time.sleep(1)
#     print("다시 깨어남")

# start = time.perf_counter()
# for _ in range(10):
#     do_someting()
# finish = time.perf_counter()

# print(f'총 걸린 시간: {finish - start} 초')

import time
import threading

def do_someting():
    print("1초 잘랭")
    time.sleep(1)
    print("다시 깨어남")

threads = []
start = time.perf_counter()
for _ in range(10):
    thread = threading.Thread(target=do_someting)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
finish = time.perf_counter()

print(f'총 걸린 시간: {finish - start} 초')