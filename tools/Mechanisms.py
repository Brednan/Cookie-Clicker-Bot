import mss
from PIL import Image
import cv2
import pyautogui
import numpy as np

class Mechanisms():
    def take_screenshot(self, monitor:int, cache_path):
        with mss.mss() as mss_instance:
            try:
                selected_monitor = mss_instance.monitors[monitor]
                screenshot = mss_instance.grab(monitor=selected_monitor)

                img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
                img.save(fp=cache_path, format='PNG')
            except IndexError:
                print('Monitor not found!')
            except:
                print('unknown error capturing screen!')
    
    def locate_object(self, template:str):
        match = cv2.matchTemplate(cv2.imread('./tools/ss_cache/screen.png'), cv2.imread(template), cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
        threshold = 0.8

        if max_val >= threshold:
            pyautogui.moveTo(x=min_loc[0], y=min_loc[1])

        temp_shape = cv2.imread(template).shape[0]
        print(temp_shape)
