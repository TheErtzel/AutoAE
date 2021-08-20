import cv2
import pytesseract
import numpy as np
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'


def textFromImage(image):
    try:
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = np.array(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.threshold(
            blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Morph open to remove noise and invert image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(
            thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening

        # Perform text extraction
        text = pytesseract.image_to_string(
            invert, lang='eng', config='--psm 6')
        return text.replace('♀', '').replace('\n\x0c', '').strip()
    except Exception as e:
        return ''


def textFoundInImage(image, text):
    textFound = False
    try:
        imageString = textFromImage(image)

        for line in imageString.splitlines():
            curText = line.lower()
            for toFind in text:
                toFind = toFind.lower()
                if toFind in curText:
                    textFound = True
                    break
    except Exception as e:
        return False
    return textFound
