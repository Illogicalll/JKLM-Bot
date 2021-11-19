from PIL import ImageGrab, Image
import cv2
import numpy as np
import pytesseract
import pyperclip
from pynput.keyboard import Key, Controller
import time
import keyboard as kb
import tkinter as tk
from tkinter import simpledialog

keyboard = Controller()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
wordsfile = open(r"C:\Users\Will\Desktop\jklm\words.txt", 'r')
words = []
for line in wordsfile:
    words.append(line.rstrip('\n'))
wordsfile.close()
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", 
            "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

def paste():
    keyboard.press(Key.ctrl_l)
    keyboard.press('v')
    keyboard.release(Key.ctrl_l)
    keyboard.release('v')
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def submitword(syllable):
    for word in words:
        if syllable in word:
            pyperclip.copy(word)
            paste()
            words.remove(word)
            time.sleep(0.5)
            break

def process(image):
    string = ''
    string = pytesseract.image_to_string(image, lang='eng', config='--psm 6')
    syllable = ''
    if len(string) > 1:
        for char in string:
            if char not in alphabet:
                string.replace(char, '')
        syllable = string[:-2]
        syllable = syllable.lower()
    submitword(syllable)

def main():
    x = 805
    y = 540
    offx = 50
    offy = 30
    img = ImageGrab.grab(bbox=(x, y, x + offx, y + offy))
    img = np.array(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    thresh = 255 - thresh
    process(thresh)

while kb.is_pressed('`') == False:
    if kb.is_pressed('1'):
        root = tk.Tk()
        root.withdraw()
        userinp = simpledialog.askstring(title="Syllable Scan Override", prompt="Enter Syllable:")
        submitword(userinp)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    main()