import cv2
import numpy as np

class ObjectDetector:
    def __init__(self, templates):
        # templates is a dictionary with enemy names as keys and their image files as values
        self.templates = {name: cv2.imread(template, 0) for name, template in templates.items()}

    def detect_objects(self, screen):
        # Convert screen to grayscale
        gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        detected_objects = []

        for name, template in self.templates.items():
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):  # Switch columns and rows
                detected_objects.append((name, pt[0], pt[1], pt[0] + w, pt[1] + h))

        return detected_objects
