from cv2 import threshold
from numpy import var
from .Mechanisms import *
import traceback
import ctypes
from pynput import mouse, keyboard
from .parse_variables_json import read_json, write_json
import os

variables_path = './tools/variables.json'
mechanisms = Mechanisms()

class Bot:
    def __init__(self, monitor, restart):
        self.monitor = monitor
        self.is_active = True
        self.variables = read_json('./tools/variables.json')

        if restart == 'y':
            self.variables['grandmas_amount'] = 0
            self.variables['Farm_amount'] = 0
            self.variables['Mine_amount'] = 0
            self.variables['Factory_amount'] = 0
            self.variables['Bank_amount'] = 0
            self.variables['Temple_amount'] = 0
            write_json('./tools/variables.json', self.variables)

    def bot_sequence(self):
        self.is_active = True
        while True:
            if self.is_active == False:
                break

            listener = keyboard.Listener(on_press=lambda key:self.on_press(key))
            listener.start()

            try:
                #Take and parse screenshot
                mechanisms.take_screenshot(self.monitor, './tools/ss_cache/screen.png')
                screen = cv2.imread('./tools/ss_cache/screen.png')

                achievements_ignore = mechanisms.locate_object_template_match('./resources/ignore_achievments.png', 0.97, screen)
                if achievements_ignore != None:
                    try:
                        mechanisms.click_object(achievements_ignore, 1, 0, self.monitor)
                    except:
                        pass
                self.variables = read_json(variables_path)


                # Check for enhancers
                self.check_enhancements(screen)

                #retake/parse screenshot
                time.sleep(0.5)
                mechanisms.take_screenshot(self.monitor, './tools/ss_cache/screen.png')
                screen = cv2.imread('./tools/ss_cache/screen.png')

                # Check for items
                self.check_items(screen)

                self.click_cookie(screen)

                write_json('./tools/variables.json', self.variables)

            except Exception as e:
                print(traceback(e))
                print('unknown error!')
                break
    def on_press(self, key):
        self.is_active = False
    
    def click_cookie(self, screen):
        cookie = mechanisms.locate_object_template_match('./resources/cookie.png', 0.95, screen)
        if cookie != None:
            if len(cookie) > 0:
                mechanisms.click_object((cookie[0], cookie[1]), 800, 0.000001, self.monitor)

    def check_factory(self, screen):
        factory_loc = mechanisms.locate_object_template_match('./resources/Factory.png', 0.99, screen)
        if factory_loc != None:
            try:
                mechanisms.click_object(factory_loc, 1, 0, self.monitor)
                self.variables['Factory_amount'] += 1
            except:
                pass

    def check_farm(self, screen):
        farm_loc = mechanisms.locate_object_template_match('./resources/Farm.png', 0.99, screen)
        if farm_loc != None:
            try:
                mechanisms.click_object(farm_loc, 1, 0, self.monitor)
                self.variables['Farm_amount'] += 1
            except:
                pass

    def check_enhancement(self, screen, template, threshold):
        obj = mechanisms.locate_object_template_match(template, threshold, screen)
        if obj != None:
            try:
                mechanisms.click_object(obj, 1, 0, self.monitor)
                pass
            except:
                pass
    
    def check_store(self, screen, template, threshold, variable:str):
        obj = mechanisms.locate_object_template_match(template, threshold, screen)
        if obj != None:
            try:
                mechanisms.click_object(obj, 1, 0, self.monitor)
                self.variables[variable] += 1
                pass
            except:
                pass
    
    def check_enhancements(self, screen):
        images = os.listdir('./resources/enhancements/')
        for i in images:
            self.check_enhancement(screen, f'./resources/enhancements/{i}', 0.99)

    def check_items(self, screen):
        if self.variables['Temple_amount'] < 10:
            self.check_store(screen, template='./resources/Temple.png', threshold=0.999, variable='Temple_amount')

        if self.variables['Bank_amount'] < 10:
            self.check_store(screen, template='./resources/Bank.png', threshold=0.9999, variable='Bank_amount')

        if self.variables['Factory_amount'] < 10:
            self.check_factory(screen)
            
        if self.variables['Mine_amount'] < 15:
            self.check_store(screen, template='./resources/Mine.png', threshold=0.99, variable='Mine_amount')
        
        if self.variables['Farm_amount'] < 15:
            self.check_farm(screen)
