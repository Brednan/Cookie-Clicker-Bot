import mss
from PIL import Image

class GetScreen():
    def take_screenshot(self, monitor:int, cache_path):
        with mss.mss() as mss_instance:
            selected_monitor = mss_instance.monitors[monitor]
            screenshot = mss_instance.grab(monitor=selected_monitor)
            # for m in mss_instance.monitors:
            #     print(m)

            img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
            img.save(fp=cache_path, format='PNG')