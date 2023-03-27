import time
import urllib.request
from tempfile import NamedTemporaryFile

from PIL import Image
from displayhatmini import DisplayHATMini

width = DisplayHATMini.WIDTH
height = DisplayHATMini.HEIGHT


class CatShuffle:
    def __init__(self):
        self.buffer = Image.new("RGB", (width, height))
        self.displayhatmini = DisplayHATMini(self.buffer, backlight_pwm=True)
        self.displayhatmini.on_button_pressed(self.button_callback)

    def button_callback(self, pin):
        if not self.displayhatmini.read_button(pin):
            return

        if pin == DisplayHATMini.BUTTON_A:
            self.newcat()

    def newcat(self):
        with NamedTemporaryFile(suffix=".jpg") as ntf:
            resp = urllib.request.urlopen("https://cataas.com/cat")
            ntf.write(resp.read())
            ntf.seek(0)
            im = Image.open(ntf.name)

        self.buffer.paste(
            im.resize((width, height)),
            (0, 0),
        )

        self.displayhatmini.display()


cs = CatShuffle()
while True:
    cs.newcat()
    time.sleep(30)
