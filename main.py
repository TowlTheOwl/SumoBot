def compareTuples(list_a, list_b, threshold):
    """
    list_a,b: list of tuples
    threshold: threshold of which to accept 
    """
    if threshold<0:
        raise ValueError("threshold must be greater or equal to 0")
    passed=[] #list of indicies which the tuples matched or are close.
    for i in range(len(list_a)):
        passing=True
        for j in range(len(list_a[i])):
            if not (list_a[i][j]<=list_b[i][j]+threshold and list_a[i][j]>=list_b[i][j]-threshold):
                passing=False
                break
        if passing:
            passed.append(i)
    return passed



import concurrent.futures
import time
from ctypes import windll
from os import path, remove
from random import randint

import keyboard
import win32api
import win32con
from PIL import ImageGrab, Image


# CAPTURE THE SCREEN (TAKE A SCREENSHOT)
def screen_capture():
    img = ImageGrab.grab(bbox=(0, 0, 1920, 1080), include_layered_windows=True)
    print("Captured!")
    img.save(r'img.jpg')


# USE MACHINE LEARNING TO CLASSIFY THE ACTION
def classify():
    print('classify')
    while not path.isfile(r'img.jpg'):
        continue
    try:
        image = Image.open(open(r"img.jpg", 'rb'))
        pixelMap = image.load()
    except Exception as ec:
        print(ec)
        image = None
        #print(image)


    if image is not None:
        last_pixel = pixelMap[1919, 1079]
        if last_pixel == (128, 128, 128):
            #print('image not completed')
            pass
        else:

            # DOES SOME CALCULATION

            # OUTPUTS 14-DIGIT OUTPUT
            for i in range(8):
                value = randint(0, 1)
                if i == 0:
                    output = str(value)
                else:
                    output = output + str(value)
            for i in range(6):
                value = randint(0, 9)
                output = output + str(value)
            with open('action.txt', 'w') as data:
                print(output, file=data)
    else:
        #print('bad image')
        pass

    #print('task finished')

# USE THE OUTPUT TO MAKE ACTION
def mojimo(acc='ctrl+g'):
    print('mojimo')
    with open('action.txt', 'r') as data:
        action = data.read()
        print(1)
    if action != '':
        st = time.time()
        print(2)
        # setup the local vars.
        print(f'current action: {action}')

        duration = 0.05  # actions taken every 'duration' in sec.
        # to be set to 0 because the same action is to be taken until the next line updates.
        t = time.time()
        keylist = []
        autoclicker = False
        autoclickerstatus = False  # saves past status of autoclicker
        mouse = tuple()
        # ----
        line = list(map(int, action))
        if len(line) < 13:
            raise AssertionError
        if line[0] == 1:
            keylist.append('w')
        if line[1] == 1:
            keylist.append('a')
        if line[2] == 1:
            keylist.append('s')
        if line[3] == 1:
            keylist.append('d')
        if line[4] == 1:
            keylist.append('shift')
        if line[5] == 1:
            keylist.append('ctrl')
        if line[6] == 1:
            keylist.append('spacebar')

        autoclicker = bool(line[7])
        mouse = (line[8] * 100 + line[9] * 10 + line[10], line[11] * 100 + line[12] * 10 + line[13])
        for key in list(set(['w', 'a', 's', 'd', 'shift', 'ctrl', 'spacebar']) - set(keylist)):
            # clear any pressed keys
            keyboard.release(key)
            print(key + " was released")
        for key in (keylist):
            # press the key according to the string.
            keyboard.press(key)
            print(key + ' was pressed')
        for _ in range(500000000):
            if time.time() - t >= duration:
                break

        t += duration  # update t
        # ----
        if autoclicker != autoclickerstatus:
            # when the program needs to toggle
            keyboard.send(acc)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(((mouse[0] - 500) / 30) / 1920 * 65535.0),
                             int(((mouse[1] - 500) / 30) / 1080 * 65535.0))  # replace 1920,1080 with screen res.
        print(f'mouse moved by {mouse}')
        # -------
        autoclickerstatus = autoclicker  # save the last autoclicker value
        print(time.time() - st)


# STOP AFTER VICTORY/LOSS
def force_stop():
    with open('state.txt', 'r') as text:
        state = text.read()
    if state == '0':
        return 0
    if state == '1':
        return 1

def state_detection():
    while True:

        while not path.isfile('img.jpg'):
            continue

        try:
            image = Image.open(open(r"img.jpg", 'rb'))
            pixelMap = image.load()
        except Exception as ec:
            image = None
        if image is not None:
            # WHEN "GO" APPEARS
            pixels = [pixelMap[870, 430],pixelMap[890, 430],pixelMap[920, 430],pixelMap[950, 430],pixelMap[980, 430],pixelMap[1000, 430],pixelMap[1040, 430],pixelMap[1065, 430]]
            tv_GO = [(255,255,255),(63,63,63),(255,255,255),(62,63,65),(255,255,255),(63,63,63),(255,255,255),(63,63,63)]#:true value:
            correctList=compareTuples(pixels, tv_GO, 5)
            if len(correctList)>=7:
                print('GO')
                with open('state.txt', 'w') as text:
                    text.write('1')
        if keyboard.is_pressed("p"):
            with open('state.txt', 'w') as text:
                text.write('0')



def repeat_sc():
    while True:
        screen_capture()
def repeat_classify():
    while force_stop() == 0:
        continue
    while force_stop() == 1:
        classify()
def repeat_macro():
    while force_stop() == 0:
        continue
    while force_stop() == 1:
        mojimo()


# LAUNCH ALL PROGRAMS TOGETHER

if __name__ == '__main__':
    with open('state.txt', 'w') as text:
        text.write('0')
    user32 = windll.user32
    user32.SetProcessDPIAware()
    print('started')
    open('action.txt', 'w').close()
    print('action file deleted')
    try:
        remove('img.jpg')
    except FileNotFoundError:
        pass
        print('file not found')
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.submit(repeat_sc)
        executor.submit(repeat_classify)
        executor.submit(repeat_macro)
        executor.submit(state_detection)
