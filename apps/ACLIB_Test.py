from source.color import Color
from source.animation import Animation
from source.gui import ACApp
from source.gl import quad
from source.aclib import ACLIB


class Test(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Test", 200, 200, 32, 32)

        self.hideDecoration()

        self.loops = 0

    def update(self, delta):
        super().update(delta)

        # blue
        if ACLIB.CARS[0].flag == 1:
            start = Color(0, 0, 0, 1)
            step = Color(0, 0, 0.01, 0)
            stop = Color(0, 0, 1, 1)
            self.addAnimation(Animation(self, "_background_color", start, step, stop, direction="Alternate"))

        if self.loops % 100 == 0:
            start = Color(0, 0, 0, 1)
            step = Color(0.05, 0.05, 0, 0)
            stop = Color(1, 1, 0, 1)
            self.addAnimation(Animation(self, "_background_color", start, step, stop, 0, "Alternate"))

        if self.loops == 1000:
            self.loops = 0

        self.loops += 1

    def render(self, delta):
        super().render(delta)
