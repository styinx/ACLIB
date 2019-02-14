from source.aclib import ACLIB
from source.animation import Animation
from source.color import Color
from source.gui import ACApp, ACGrid, ACLabel


class Test(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Test", 200, 200, 200, 200)

        self.hideDecoration()

        start = Color(1, 0, 0, 1)
        step = Color(0, 0.025, 0, 0)
        stop = Color(1, 1, 0, 1)
        self.anim1 = Animation(self, "background_color", start, step, stop, -1, "Alternate")

    def update(self, delta):
        super().update(delta)

        if ACLIB.CARS[0].speed > 10 and self.animation is None:
            self.addAnimation(self.anim1)

    def render(self, delta):
        super().render(delta)
