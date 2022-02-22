from .Mechanisms import *
import traceback
import ctypes
from pynput import mouse, keyboard

# keyboard_obj = keyboard.Controller()
# mouse_obj = keyboard.Controller()


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

                self.check_factory(screen)
                self.check_farm(screen)

                self.click_cookie(mechanisms, screen)

            except Exception as e:
                print('unknown error!')
                break
    def on_press(self, key):
        self.is_active = False
    
    def click_cookie(self, mechanisms, screen):
        cookie = mechanisms.locate_object_template_match('./resources/cookie.png', 0.7, screen)
        if len(cookie) > 0:
            mechanisms.click_object((cookie[0], cookie[1]), 200, 0.000001, self.monitor)

    def check_factory(self, screen):
        factory_loc = mechanisms.locate_object_template_match('./resources/Factory.png', 0.95, screen)
        if factory_loc != None:
            try:
                mechanisms.click_object(factory_loc, 1, 0, self.monitor)
                mouse.move(-10, 0)
            except:
                pass

    def check_farm(self, screen):
        farm_loc = mechanisms.locate_object_template_match('./resources/Farm.png', 0.95, screen)
        if farm_loc != None:
            try:
                mechanisms.click_object(farm_loc, 1, 0, self.monitor)
                mouse.move(-10, 0)
            except:
                pass
