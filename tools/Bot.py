from cv2 import threshold
from numpy import var
from .Mechanisms import *
import traceback
import ctypes
from pynput import mouse, keyboard
from .parse_variables_json import read_json, write_json

variables_path = './tools/variables.json'
mechanisms = Mechanisms()

class Bot:
    def __init__(self, monitor):
        self.monitor = monitor
        self.is_active = True

    def bot_sequence(self):
        self.is_active = True
        while True:
            if self.is_active == False:
                break

            listener = keyboard.Listener(on_press=lambda key:self.on_press(key))
            listener.start()

            try:
                mechanisms.take_screenshot(self.monitor, './tools/ss_cache/screen.png')
                screen = cv2.imread('./tools/ss_cache/screen.png')

                achievements_ignore = mechanisms.locate_object_template_match('./resources/ignore_achievments.png', 0.97, screen)
                if achievements_ignore != None:
                    try:
                        mechanisms.click_object(achievements_ignore, 1, 0, self.monitor)
                    except:
                        pass
                variables = read_json(variables_path)

                self.check_store(screen, './resources/plastic_mouse.png', 0.99)
                if mechanisms.locate_object_template_match('./resources/Bank.png', threshold=0.999, screen=screen) != None:
                    self.check_store(screen, template='./resources/Bank.png', threshold=0.999)

                elif mechanisms.locate_object_template_match('./resources/Factory.png', threshold=0.999, screen=screen) != None:
                    self.check_factory(screen)
                    
                else:
                    self.check_store(screen, template='./resources/Mine.png', threshold=0.999)
                    self.check_farm(screen)

                self.click_cookie(screen)

                write_json('./tools/variables.json', variables)

            except Exception as e:
                print(traceback(e))
                print('unknown error!')
                break
    def on_press(self, key):
        self.is_active = False
    
    def click_cookie(self, screen):
        cookie = mechanisms.locate_object_template_match('./resources/cookie.png', 0.7, screen)
        if cookie != None:
            if len(cookie) > 0:
                mechanisms.click_object((cookie[0], cookie[1]), 800, 0.000001, self.monitor)

    def check_factory(self, screen):
        factory_loc = mechanisms.locate_object_template_match('./resources/Factory.png', 0.99999, screen)
        if factory_loc != None:
            try:
                mechanisms.click_object(factory_loc, 1, 0, self.monitor)
            except:
                pass

    def check_farm(self, screen):
        farm_loc = mechanisms.locate_object_template_match('./resources/Farm.png', 0.99999, screen)
        if farm_loc != None:
            try:
                mechanisms.click_object(farm_loc, 1, 0, self.monitor)
            except:
                pass

    def check_store(self, screen, template, threshold):
        obj = mechanisms.locate_object_template_match(template, threshold, screen)
        if obj != None:
            try:
                mechanisms.click_object(obj, 1, 0, self.monitor)
                pass
            except:
                pass
