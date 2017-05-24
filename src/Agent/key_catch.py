import threading
from time import sleep

from pynput import keyboard

g = threading.Lock()
r = threading.RLock()
b = 0
currKey = []


class KeyPressed:
    def __init__(self, key, time):
        self.key = key
        self.time = time


def on_press(key):
    global currKey
    with g:
        if key not in currKey:
            currKey.append(key)


def on_release(key):
    global currKey
    with g:
        if key in currKey:
            currKey.remove(key)


def getCurrKey():
    global b
    global currKey
    r.acquire()
    b += 1
    if (b == 1):
        g.acquire()
    r.release()
    ret = currKey
    r.acquire()
    b -= 1
    if (b == 0):
        g.release()
    r.release()
    return ret


def KeyOnHold():
    while (1):
        ret = getCurrKey()
        if ret:
            print "curr Keys ", getCurrKey()
        sleep(0.1)


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    try:
        keysonhold = threading.Thread(target=KeyOnHold)
        keysonhold.start()
        keysonhold.join()
        listener.join()
    except Exception as e:
        print e