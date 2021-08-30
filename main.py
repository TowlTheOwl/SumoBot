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

def save_actions(action, actionNum):
    with open('action.txt', 'a') as actionFile:
        actionFile.write(str(actionNum) + ' ' + (action) + '\n')


import numpy as np
import time
from ctypes import windll
from os import path, remove
from random import randint
import keyboard
import win32api
import win32con
import mss
import mss.tools
from multiprocessing import Process, Queue


# CAPTURE THE SCREEN (TAKE A SCREENSHOT)
def screen_grab(queue1):
    while True:
        with mss.mss() as sct:
            mon = sct.monitors[1]
            queue1.put(sct.grab(mon))
        time.sleep(0.01)


# USE MACHINE LEARNING TO CLASSIFY THE ACTION
def classify(queue1, queue2):
    while True:
        if force_stop() == 1:
            image = queue1.get()
            if image is not None:
                img_array = np.array(image)
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
                queue2.put(output)
            else:
                pass


# USE THE OUTPUT TO MAKE ACTION
def execute_action(queue2, acc='ctrl+g'):
    actionNum = 1
    while True:
        if force_stop() == 1:
            action = queue2.get()
            if action is not None:
                st = time.time()
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
                # -------
                autoclickerstatus = autoclicker  # save the last autoclicker value
                Process(target=save_actions, args=(action, actionNum)).start()
                actionNum += 1

# STOP AFTER VICTORY/LOSS
def force_stop():
    with open('state.txt', 'r') as text:
        state = text.read()
    # 0 = Waiting; 1 = Running; 2 = Lost; 3 = Won
    if state == '0':
        return 0
    if state == '1':
        return 1
    if state == '2':
        return 2
    if state == '3':
        return 3

def state_detection(queue1):
    while True:
        image = queue1.get()
        if image is not None:
            pixelMap = np.array(image)

            # WHEN "1" APPEARS
            pixels = [pixelMap[380, 950][:-1],pixelMap[390, 970][:-1],pixelMap[390, 940][:-1],pixelMap[460, 970][:-1],pixelMap[470, 920][:-1],pixelMap[490, 940][:-1],pixelMap[470, 980][:-1],pixelMap[490, 1000][:-1]]
            tv_GO = [(85, 85, 255),(21, 21, 63),(85, 85, 255),(21, 21, 63),(85, 85, 255),(21, 21, 63),(85, 85, 255),(21, 21, 63)]#:true value:
            correctList=compareTuples(pixels, tv_GO, 5)
            if len(correctList)>=7:
                print('GO')
                with open('state.txt', 'w') as text:
                    text.write('1')

            # WHEN LOST
            pixels = [pixelMap[420, 470][:-1], pixelMap[430, 490][:-1], pixelMap[430, 520][:-1],
                      pixelMap[430, 550][:-1], pixelMap[430, 570][:-1], pixelMap[430, 600][:-1],
                      pixelMap[430, 1220][:-1], pixelMap[430, 1270][:-1]]
            tv_GO = [(85, 85, 255), (21, 21, 63), (85, 85, 255), (21, 21, 63), (85, 85, 255), (21, 21, 63),
                     (85, 85, 255), (21, 21, 63)]
            correctList = compareTuples(pixels, tv_GO, 5)
            if len(correctList) >= 7:
                print('LOST')
                with open('state.txt', 'w') as text:
                    text.write('2')
                time.sleep(0.05)
                for i in ['w', 'a', 's', 'd', 'shift', 'ctrl', 'spacebar']:
                    keyboard.release(i)

            # WHEN WON
            pixels = [pixelMap[430, 340][:-1], pixelMap[430, 380][:-1], pixelMap[430, 900][:-1],
                      pixelMap[430, 940][:-1], pixelMap[430, 1010][:-1], pixelMap[430, 1050][:-1],
                      pixelMap[430, 1570][:-1], pixelMap[430, 1610][:-1]]
            tv_GO = [(85, 255, 85), (21, 63, 21), (85, 255, 85), (21, 63, 21), (85, 255, 85), (21, 63, 21),
                     (85, 255, 85), (21, 63, 21)]
            correctList = compareTuples(pixels, tv_GO, 5)
            if len(correctList) >= 7:
                print('WON')
                with open('state.txt', 'w') as text:
                    text.write('3')
                time.sleep(0.05)
                for i in ['w', 'a', 's', 'd', 'shift', 'ctrl', 'spacebar']:
                    keyboard.release(i)
        if keyboard.is_pressed("p"):
            with open('state.txt', 'w') as text:
                text.write('0')
            time.sleep(0.05)
            for i in ['w', 'a', 's', 'd', 'shift', 'ctrl', 'spacebar']:
                keyboard.release(i)
            print('FORCE STOPPED')



# LAUNCH ALL PROGRAMS TOGETHER

if __name__ == '__main__':
    np.set_printoptions(threshold=np.inf)
    with open('state.txt', 'w') as text:
        text.write('0')
    user32 = windll.user32
    user32.SetProcessDPIAware()
    print('started')
    open('action.txt', 'w').close()
    print('action file deleted')


    # gives image
    queue1 = Queue()
    # gives action
    queue2 = Queue()

    Process(target=state_detection, args=(queue1,)).start()
    Process(target=screen_grab, args=(queue1,)).start()
    Process(target=classify, args=(queue1, queue2)).start()
    Process(target=execute_action, args=(queue2,)).start()
