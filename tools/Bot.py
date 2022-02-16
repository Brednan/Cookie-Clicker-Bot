from Mechanisms import *
import traceback

mechanisms = Mechanisms()

class Bot:
    def bot_sequence(self):
        try:
            mechanisms.take_screenshot(1, './tools/ss_cache/screen.png')
            object = mechanisms.locate_object('./resources/cookie_image.PNG', 0.8)
            print(object)

        except IndexError:
            print('Monitor not found!')
        except Exception as e:
            print(traceback(e))
            print('unknown error capturing screen!')

bot = Bot()
bot.bot_sequence()
