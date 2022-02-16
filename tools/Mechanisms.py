import mss
from PIL import Image
import cv2
import pyautogui
import numpy as np

class Mechanisms():
    def take_screenshot(self, monitor:int, cache_path):
        with mss.mss() as mss_instance:
            selected_monitor = mss_instance.monitors[monitor]
            screenshot = mss_instance.grab(monitor=selected_monitor)

            img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
            img.save(fp=cache_path, format='PNG')

    
    def locate_object(self, template:str, threshold):
        match = cv2.matchTemplate(cv2.imread('./tools/ss_cache/screen.png'), cv2.imread(template), cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
        threshold = 0.8
        temp_shape = cv2.imread(template).shape

        if max_val >= threshold:
            coordinates = max_loc
            print(len(temp_shape[0:2]))
            coordinates = tuple(map(lambda a, b: a + b, coordinates, temp_shape[0:2]))
            return (coordinates)

        else:
            return None
    
    def click_object(self, location):
        pyautogui.moveTo(x=location[0], y=location[1])
