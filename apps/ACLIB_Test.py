from source.aclib import ACLIB
from source.color import Color
from source.animation import Animation
from source.gui import ACApp


class Test(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Test", 200, 200, 256, 256)

        self.loops = 0

    def update(self, delta):
        super().update(delta)

        if self.loops == 50:
            self.addAnimation(
                Animation(self, "_background_color", Color(0, 0, 0, 1), Color(0.01, 0, 0, 0), Color(1, 0, 0, 1)))

        if self.loops == 250:
            self.addAnimation(
                Animation(self, "_background_color", Color(1, 0, 0, 1), Color(-0.01, 0, 0, 0), Color(0, 0, 0, 1)))

        if self.loops == 400:
            self.addAnimation(
                Animation(self, "_background_color", Color(0, 0, 0, 1), Color(0, 0.01, 0, 0),
                          Color(0, 1, 0, 1)).setDirection("Alternate"))
            self.loops = 0

        self.loops += 1

        ACLIB.CONSOLE(self.loops)
