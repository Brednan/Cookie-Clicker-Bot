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
        self.mines = 0
        self.farms = 0
        self.grandmas = 0
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

                self.check_store(screen, template='./resources/plastic_mouse.png', threshold=1)
                self.check_store(screen, template='./resources/reinforced_index_finger.png', threshold=1)

                mechanisms.take_screenshot(self.monitor, './tools/ss_cache/screen.png')
                screen = cv2.imread('./tools/ss_cache/screen.png')

                if self.mines <= 5:
                    mine_available = self.check_store(screen, './resources/Mine.png', 0.97)
                    if mine_available == True:
                        self.mines +=1
                        time.sleep(0.01)
                
                if self.grandmas <= 10:
                    grandma_loc = mechanisms.locate_object_template_match('./resources/grandma.png', threshold=1, screen=screen)
                    if grandma_loc != None:
                        if len(grandma_loc) > 0:
                            try:
                                mechanisms.click_object(amount=1, location=grandma_loc, interval=0, monitor=self.monitor)
                                self.grandmas += 1
                            except:
                                pass

                mechanisms.take_screenshot(self.monitor, './tools/ss_cache/screen.png')
                screen = cv2.imread('./tools/ss_cache/screen.png')

                self.check_factory(screen)
                self.check_farm(screen)

                self.click_cookie(mechanisms, screen)

            except Exception as e:
                print(traceback(e))
                print('unknown error!')
                break
    def on_press(self, key):
        self.is_active = False
    
    def click_cookie(self, mechanisms, screen):
        cookie = mechanisms.locate_object_template_match('./resources/cookie.png', 0.7, screen)
        if cookie != None:
            if len(cookie) > 0:
                mechanisms.click_object((cookie[0], cookie[1]), 200, 0.000001, self.monitor)

    def check_factory(self, screen):
        factory_loc = mechanisms.locate_object_template_match('./resources/Factory.png', 0.97, screen)
        if factory_loc != None:
            try:
                mechanisms.click_object(factory_loc, 1, 0, self.monitor)
                mouse.move(-10, 0)
            except:
                pass

    def check_farm(self, screen):
        plastic_mouse_available = mechanisms.locate_object_template_match('./resources/plastic_mouse.png', 0.95, screen)
        if plastic_mouse_available == None:
            farm_loc = mechanisms.locate_object_template_match('./resources/Farm.png', 0.96, screen)
            if farm_loc != None and self.farms <= 10:
                try:
                    mechanisms.click_object(farm_loc, 1, 0, self.monitor)
                    mouse.move(-10, 0)
                    self.farms += 1
                except:
                    pass
        else:
            pass

    def check_store(self, screen, template, threshold):
        obj = mechanisms.locate_object_template_match(template, threshold, screen)
        if obj != None:
            try:
                mechanisms.click_object(obj, 1, 0, self.monitor)
            except:
                pass

