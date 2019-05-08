import threading
import time

def fonction(env):
    while(not env['stop']):
        print(env['lettre'])
        time.sleep(0.1)

envi = {'lettre': 'a', 'stop': False}
thread = threading.Thread(None, fonction, None, [envi])
thread.start()
time.sleep(0.5)
envi['lettre'] = 'b'
time.sleep(1)
envi['stop'] = True
time.sleep(0.1)
print(thread.isAlive())

