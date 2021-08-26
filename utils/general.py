import re
import cv2
import mss
import mss.tools
import numpy as np
import pyautogui
import pytesseract
from tkinter import *
from datetime import datetime

import utils.constants as consts
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'


def GetTimestamp():
    dateTimeObj = datetime.now()
    timeObj = dateTimeObj.now().time()
    return timeObj.strftime("%H:%M:%S.%f")


def getKeyIndex(key: str = 'f1'):
    index = -1
    try:
        index = consts.KeyList.index(key)
    except ValueError:
        index = -1
    return index


def getKey(key: str = 'f1'):
    index = getKeyIndex(key)
    if index != -1:
        return consts.KeyList[index]
    else:
        return 'f1'


def convert_rgb_to_bgr(img):
    return img[:, :, ::-1]


def scale(img):
    scale_percent = 200  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized


def toGrayScale(image=None):
    if image is None:
        return None
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def CropForeground(imageFile=None):
    if imageFile is None:
        return None

    originalImage = cv2.imread(imageFile)
    grayImage = toGrayScale(originalImage.copy())

    (thresh, grayScaleImage) = cv2.threshold(
        grayImage, 127, 255, cv2.THRESH_BINARY)
    bbox = cv2.boundingRect(grayScaleImage)
    x, y, w, h = bbox
    foreground = originalImage[y:y+h, x:x+w]
    return foreground


def TakeScreenshot(file='', location={'top': 0, 'left': 0, 'width': 1080, 'height': 1920}, crop=True):

    with mss.mss() as sct:
        # The screen part to capture
        monitor = {'top': location['top'], 'left': location['left'],
                   'width': location['width'], 'height': location['height']}
        output = "\\images\\tmp\\sct-{top}x{left}_{width}x{height}.png".format(
            **monitor)
        if file != '':
            output = f'{file}'

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        screenshot = cv2.cvtColor(np.array(sct_img), cv2.COLOR_BGR2RGB)
        cv2.imwrite(output, screenshot)
        if crop:
            image = CropForeground(output)
            cv2.imwrite(output, convert_rgb_to_bgr(scale(image)))
        return output
