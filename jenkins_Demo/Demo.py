#coding=utf-8
import pyautogui
import time

s, h = pyautogui.size()
print(s, h)
time.sleep(10)
pyautogui.moveTo(s/2,h/2)

def drag(n):
    pyautogui.dragRel(xOffset=n,yOffset=0,duration=1)
    pyautogui.dragRel(xOffset=0,yOffset=n,duration=1)
    pyautogui.dragRel(xOffset=-n,yOffset=0,duration=1)
    pyautogui.dragRel(xOffset=0,yOffset=-n,duration=1)
def dragy(n):
    pyautogui.dragRel(xOffset=0,yOffset=-n,duration=1)
    pyautogui.dragRel(xOffset=n,yOffset=0,duration=1)
    pyautogui.dragRel(xOffset=0,yOffset=n,duration=1)
    pyautogui.dragRel(xOffset=-n,yOffset=0,duration=1)
# pyautogui.dragRel(xOffset=100,yOffset=100,duration=1)
ls = [20,40,60,80,100,120,140,160,180]
# ls = [20, 40]
for n in ls:
    drag(n)
    drag(-n)
    dragy(n)
    dragy(-n)

