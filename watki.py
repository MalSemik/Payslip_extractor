import threading
import time

got_input = False
def still_waiting():
    while not got_input:
        print('Still waiting...')
        time.sleep(3)

thread = threading.Thread(target=still_waiting)
# thread.setDaemon(True)
thread.start()
input()
# got_input = True
print("udalo sie")