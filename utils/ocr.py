import cv2
import pytesseract
import numpy as np
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'


def textFromImage(image):
    try:
        # Load image, grayscale, Otsu's threshold
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Morph open to remove noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        opening = cv2.morphologyEx(
            thresh, cv2.MORPH_OPEN, kernel, iterations=1)

        # Find contours and remove small noise
        cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 50:
                cv2.drawContours(opening, [c], -1, 0, -1)

        # Invert and apply slight Gaussian blur
        result = 255 - opening
        #result = cv2.GaussianBlur(result, (3, 3), 0)

        # Perform OCR
        text = pytesseract.image_to_string(
            result, lang='eng', config='--psm 6').replace('♀', '').replace('\n\x0c', '').strip()

        return text
    except Exception as e:
        return ''
