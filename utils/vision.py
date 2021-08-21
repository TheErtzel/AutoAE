import cv2
import math
import numpy as np
from mss import mss
from PIL import Image

import utils.logic as logic


class Vision:
    def __init__(self):
        self.static_templates = {
            'gui-party-top': 'assets/party/guiTop.png',
            'own-name': 'assets/ownName.png',
            'own-name-alt': 'assets/ownName-alt.png',
            'party-member-name': 'assets/party/memberName.png',
            'guild-tag-left1': 'assets/party/tags/guild-left1.png',
            'guild-tag-left2': 'assets/party/tags/guild-left2.png',
            'guild-tag-left3': 'assets/party/tags/guild-left3.png',
            'guild-tag-left4': 'assets/party/tags/guild-left4.png',
            'guild-tag-left5': 'assets/party/tags/guild-left5.png',
            'guild-tag-left6': 'assets/party/tags/guild-left6.png'
        }

        self.templates = {k: cv2.imread(v, 0) for (
            k, v) in self.static_templates.items()}

        self.monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        self.screen = mss()

        self.frame = None

    def convert_rgb_to_bgr(self, img):
        return img[:, :, ::-1]

    def crop_foreground(self, image):
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        (thresh, grayScaleImage) = cv2.threshold(
            grayImage, 127, 255, cv2.THRESH_BINARY)
        bbox = cv2.boundingRect(grayScaleImage)
        x, y, w, h = bbox
        foreground = image[y:y+h, x:x+w]
        return foreground

    def take_screenshot(self, monitor={'top': 0, 'left': 0, 'width': 1920, 'height': 1080}, blackAndWhite=True, crop=False, scale=1.0):
        try:
            sct_img = None
            if monitor == None:
                sct_img = self.screen.grab(self.monitor)
            else:
                sct_img = self.screen.grab(monitor)
            img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
            img = np.array(img)
            img = self.convert_rgb_to_bgr(img)
            if crop:
                img = self.crop_foreground(img)

            img = cv2.resize(img, (0, 0), fx=scale, fy=scale)

            if not blackAndWhite:
                return img
            else:
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                (thresh, blackAndWhiteImage) = cv2.threshold(
                    img_gray, 127, 255, cv2.THRESH_BINARY)

                return blackAndWhiteImage
        except Exception as e:
            return []

    def refresh_frame(self, monitor=None, blackAndWhite=True):
        self.frame = self.take_screenshot(monitor, blackAndWhite=True)

    def notInList(self, detectedObjects, newObject):
        for detectedObject in detectedObjects:
            if math.hypot(newObject[0]-detectedObject[0], newObject[1]-detectedObject[1]) < 30:
                return False
        return True

    def find_template_matches(self, name, monitor={'top': 0, 'left': 0, 'width': 1920, 'height': 1080}, threshold=0.85):
        sct_img = None
        if monitor == None:
            sct_img = self.screen.grab(self.monitor)
        else:
            sct_img = self.screen.grab(monitor)
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        img = np.array(img)
        img = self.convert_rgb_to_bgr(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template = self.templates[name]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        detectedObjects = []

        try:
            for pt in zip(*loc[::-1]):
                try:
                    if len(detectedObjects) == 0 or self.notInList(pt):
                        detectedObjects.append(pt)
                except:
                    continue
        except:
            return detectedObjects

        return detectedObjects

    def to_gray(self, image=None):
        if image == None:
            return []

        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def match_image(self, img_grayscale, image, threshold=0.9):
        """
        Matches image in a target grayscaled image
        """

        res = cv2.matchTemplate(img_grayscale, image, cv2.TM_CCOEFF_NORMED)
        matches = np.where(res >= threshold)
        return matches

    def find_image(self, source=None, image=None, threshold=0.9):
        src = None
        if image is None:
            if self.frame is None:
                self.refresh_frame()
            image = self.frame

        if isinstance(source, str):
            src = cv2.imread(source, 0)
            src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
            (thresh, blackAndWhiteImage) = cv2.threshold(
                src, 127, 255, cv2.THRESH_BINARY)
            src = blackAndWhiteImage
        else:
            src = source

        return self.match_image(image, src, threshold)

    def find_template(self, name, image=None, threshold=0.9):
        return self.find_image(source=self.templates[name], image=image, threshold=threshold)

    def scaled_find_image(self, source=None, image=None, threshold=0.9, scales=[1.0, 0.9, 1.1]):
        src = None
        if image is None:
            if self.frame is None:
                self.refresh_frame()
            image = self.frame

        if isinstance(source, str):
            src = cv2.imread(source, 0)
            src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
            (thresh, blackAndWhiteImage) = cv2.threshold(
                src, 127, 255, cv2.THRESH_BINARY)
            src = blackAndWhiteImage
        else:
            src = source

        initial_template = src
        for scale in scales:
            scaled_template = cv2.resize(
                initial_template, (0, 0), fx=scale, fy=scale)
            matches = self.match_image(image, scaled_template,  threshold)
            if np.shape(matches)[1] >= 1:
                return matches
        return matches

    def scaled_find_template(self, name, image=None, threshold=0.9, scales=[1.0, 0.9, 1.1]):
        return self.scaled_find_image(source=self.templates[name], image=image, threshold=threshold, scales=scales)
