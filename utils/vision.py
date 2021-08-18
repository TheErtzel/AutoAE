import cv2
from mss import mss
from PIL import Image
import numpy as np
import time

class Vision:
    def __init__(self):
        self.static_templates = {
            'health-bar': 'assets/healthBar.png',
            'stamina-bar': 'assets/stamBar.png',
            'gui-party-top': 'assets/party/guiTop.png',
            'own-name': 'assets/ownName.png',
            'party-member-name': 'assets/party/memberName.png'
        }

        self.templates = { k: cv2.imread(v, 0) for (k, v) in self.static_templates.items() }

        self.monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        self.screen = mss()

        self.frame = None

    def convert_rgb_to_bgr(self, img):
        return img[:, :, ::-1]

    def take_screenshot(self, monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}):
        sct_img = None
        if monitor == None: sct_img = self.screen.grab(self.monitor)
        else: sct_img = self.screen.grab(monitor)
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        img = np.array(img)
        img = self.convert_rgb_to_bgr(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        return img_gray

    def refresh_frame(self, monitor = None):
        self.frame = self.take_screenshot(monitor)

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
        else: src = source

        return self.match_image(image, src, threshold)

    def find_template(self, name, image=None, threshold=0.9):
        return self.find_image(self.templates[name], image, threshold)

    def scaled_find_image(self, source=None, image=None, threshold=0.9, scales=[1.0, 0.9, 1.1]):
        src = None
        if image is None:
            if self.frame is None:
                self.refresh_frame()
            image = self.frame
        
        if isinstance(source, str):
            src = cv2.imread(source, 0)
            src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        else: src = source

        initial_template = src
        for scale in scales:
            scaled_template = cv2.resize(initial_template, (0,0), fx=scale, fy=scale)
            matches = self.match_image(image, scaled_template,  threshold)
            if np.shape(matches)[1] >= 1:
                return matches
        return matches

    def scaled_find_template(self, name, image=None, threshold=0.9, scales=[1.0, 0.9, 1.1]):
        return self.scaled_find_image(self.templates[name], image, threshold, scales)