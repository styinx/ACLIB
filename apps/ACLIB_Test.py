from source.color import Color
from source.animation import Animation
from source.gui import ACApp, ACLabel
from source.aclib import ACLIB
from source.math import Rect
from source.gl import rect


class Test(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Test", 200, 200, 32, 32)

        self.hideDecoration()

        self.loops = 0

        self.my_widget = ACLabel("", self, self, text_color=Color(1, 0, 0, 1))

    def update(self, delta):
        super().update(delta)

        self.my_widget.setText("widget text: " + str(delta))

        # blue
        if ACLIB.CARS[0].flag == 1:
            start = Color(0, 0, 0, 1)
            step = Color(0, 0, 0.01, 0)
            stop = Color(0, 0, 1, 1)
            self.addAnimation(Animation(self, "background_color", start, step, stop, direction="Alternate"))

        if self.loops % 100 == 0:
            start = Color(0, 0, 0, 1)
            step = Color(0.05, 0.05, 0, 0)
            stop = Color(1, 1, 0, 1)
            self.addAnimation(Animation(self, "background_color", start, step, stop, 0, "Alternate"))
            self.setBackgroundColor(Color(1, 1, 0))

        if self.loops % 500 == 0:
            x, y = self.getPos()
            w, h = self.getSize()
            start = Rect().set(x, y, w, h)
            step = Rect().set(0, 0, 1, 1)
            stop = Rect().set(x, y, w + 25, h + 25)
            self.addAnimation(Animation(self, "geometry", start, step, stop, 0, "Alternate"))

        if self.loops == 1000:
            self.loops = 0

        self.loops += 1

    def render(self, delta):
        super().render(delta)

        r = self.geometry
        rect(r=Rect(x=0, y=r.h + 5, w=r.w, h=5))
        rect(r=Rect(x=0, y=r.h + 5, w=r.w, h=5), color=Color(1, 0, 0))
