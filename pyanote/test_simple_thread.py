import threading
import time

def fonction(controleur):
    while(not controleur['stop']):
        print(controleur['lettre'])
        time.sleep(0.1)

controleur = {'lettre': 'a', 'stop': False}
thread = threading.Thread(None, fonction, None, [controleur])
thread.start()
time.sleep(0.5)
controleur['lettre'] = 'b'
time.sleep(1)
controleur['stop'] = True
time.sleep(0.1)
print(thread.isAlive())

