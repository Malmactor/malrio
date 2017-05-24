import threading
from time import sleep

from pynput import keyboard, keyboard

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
        if key == keyboard.Key.esc:
            return False
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
    #lock r to lock g
    r.acquire()
    b += 1
    if (b == 1):
        g.acquire()
    r.release()

    cks = currKey

    #release r and g
    r.acquire()
    b -= 1
    if (b == 0):
        g.release()
    r.release()
    res = ""
    for i in cks:
        if keyboard.Key.space != i:
            res += str(i)
    if keyboard.Key.space in cks:
        res += " "
    return res


def KeyOnHold(callback):
    while (1):
        ret = getCurrKey()
        if ret:
            print "curr Keys ", ret
            callback(ret)
        sleep(0.1)

def init_listener(callback):
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        try:
            keysonhold = threading.Thread(target=KeyOnHold,args=[callback])
            keysonhold.start()
            keysonhold.join()
            listener.join()
        except Exception as e:
            print e