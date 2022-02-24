import mss
from PIL import Image, ImageGrab
import cv2
import pyautogui
import ctypes
import time

class Mechanisms():
    def take_screenshot(self, monitor:int, cache_path):
        with mss.mss() as mss_instance:
            selected_monitor = mss_instance.monitors[monitor]
            screenshot = mss_instance.grab(monitor=selected_monitor)

            img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
            img.save(fp=cache_path, format='PNG')

    
    def locate_object_template_match(self, template:str, threshold, screen):
        try:
            match = cv2.matchTemplate(screen, cv2.imread(template), cv2.TM_CCOEFF_NORMED)
            temp_shape = cv2.imread(template).shape
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)

            if max_val >= threshold:
                max_loc = (max_loc[0] + (temp_shape[1]/2), max_loc[1] + (temp_shape[0]/2))
                return max_loc
            
            else:
                return None
        except:
            return None

    
    def click_object(self, location, amount, interval, monitor):
        ctypes.windll.user32.SetCursorPos(int(location[0]) + ((monitor-1)*1920), int(location[1]))
        pyautogui.click(clicks=amount, interval=interval)
    
    def locate_cascade(self, cascade_path, screen):
        cascade_cookie = cv2.CascadeClassifier(cascade_path)
        loc = cascade_cookie.detectMultiScale(screen, minNeighbors=15)

        print(loc)
        return loc[0]
        
