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
                if variables['has_plastic_mouse'] == True:
                    mechanisms.take_screenshot(self.monitor, './tools/ss_cache/screen.png')
                    screen = cv2.imread('./tools/ss_cache/screen.png')

                    self.check_factory(screen)
                    self.check_store(screen, template='./resources/Mine.png', threshold=0.9)                
                    self.check_farm(screen)

                    grandma_loc = mechanisms.locate_object_template_match('./resources/grandma.png', threshold=0.93, screen=screen)
                    if grandma_loc !=None:
                        if len(grandma_loc) > 0:
                            mechanisms.click_object(amount=1, location=grandma_loc, interval=0, monitor=self.monitor)

                else:
                    if self.check_store(screen, template='./resources/plastic_mouse.png', threshold=0.98) == True:
                        mechanisms.take_screenshot(self.monitor, './tools/ss_cache/screen.png')
                        time.sleep(0.1)
                        icon_visible = mechanisms.locate_object_template_match('./resources/plastic_mouse.png', threshold=0.93, screen=screen)
                        if len(icon_visible) <= 0:
                            variables['has_plastic_mouse'] = True

                self.check_store(screen, template='./resources/reinforced_index_finger.png', threshold=1)
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
                mechanisms.click_object((cookie[0], cookie[1]), 400, 0.000001, self.monitor)

    def check_factory(self, screen):
        factory_loc = mechanisms.locate_object_template_match('./resources/Factory.png', 0.97, screen)
        if factory_loc != None:
            try:
                mechanisms.click_object(factory_loc, 1, 0, self.monitor)
                mouse.move(-10, 0)
            except:
                pass

    def check_farm(self, screen):
        farm_loc = mechanisms.locate_object_template_match('./resources/Farm.png', 0.96, screen)
        if farm_loc != None and self.farms <= 10:
            try:
                mechanisms.click_object(farm_loc, 1, 0, self.monitor)
                mouse.move(-10, 0)
            except:
                pass

    def check_store(self, screen, template, threshold):
        obj = mechanisms.locate_object_template_match(template, threshold, screen)
        if obj != None:
            try:
                mechanisms.click_object(obj, 1, 0, self.monitor)
                return True
            except:
                return False
        return False

