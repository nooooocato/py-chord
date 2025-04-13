from pynput import keyboard
from pynput.keyboard import Key, Controller
from config import ref, binRule

device = Controller()

prvstate = 0
curstate = 0

frameCount = 0  # how many keys in each chord frame
counter = 0
lock = False


def press_logic(key):
    global curstate
    if hasattr(key, "char"):
        if key.char in ref:
            curstate += ref[key.char]
    #     print("key {0} pressed".format(key.char))  # type(key.char) str
    # print(bin(curstate))
    # else:
    #     if key == keyboard.Key.shift:
    #         curstate += ref["shift"]
    #     else:
    #         pass


def release_logic(key):
    global curstate
    global prvstate
    global lock
    global counter
    global frameCount
    if hasattr(key, "char") and curstate in binRule:
        lock = True
        # for i in range(frameCount):
        #     device.tap(Key.backspace)
        device.tap(Key.esc)
        for char in binRule[curstate]:
            device.tap(char)
        # print(bin(curstate))
    prvstate = curstate
    curstate = 0
    counter = 0
    lock = False
    frameCount = 0



def on_press(key):
    global counter
    global frameCount
    if not lock:
        counter += 1
        frameCount += 1
        press_logic(key)


def on_release(key):
    global counter
    if not lock:
        counter -= 1
        if counter <= 0:
            release_logic(key)
        else:
            counter = 0


# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
