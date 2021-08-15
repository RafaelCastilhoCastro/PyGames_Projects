import time

start_time = time.time()
while True:
    print('tick')
    time.sleep(1.0 - ((time.time() - start_time) % 1.0))cd..