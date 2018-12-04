from source.aclib import ACLIB
from source.color import Color
from source.event import LIB_EVENT
from source.gui import ACApp, ACGrid, ACLabel


class Notification(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Notification", 200, 200, 512, 96)

        self.hideDecoration().setBackgroundColor(Color(0, 0, 0, 0.5))

        self.car = ACLIB.CARS[0]
        self.grid = ACGrid(self, 5, 3)
        self.text = ACLabel("", self, font_size=20, bold=1, text_h_alignment="center", text_color=Color(1, 1, 1))
        self.timeout = 2
        self.timer = 0

        self.grid.addWidget(self.text, 0, 0, 5, 3)

        self.car.setEvent(LIB_EVENT.ON_FLAG_CHANGED, self.flagChange)
        self.car.setEvent(LIB_EVENT.ON_POSITION_CHANGED, self.posChange)

    def update(self, delta):
        super().update(delta)

        self.timer += delta

        if self.timer > self.timeout:
            self.timer = 0
            self.setBackgroundColor(Color(0, 0, 0, 0.5))
            self.text.setTextColor(Color(1, 1, 1))
            self.text.setText("")

    def render(self, delta):
        super().render(delta)

    def flagChange(self, car_index):
        if self.car.flag == 1:
            self.setBackgroundColor(Color(0, 0.5, 1, 0.5))
        elif self.car.flag == 2:
            self.setBackgroundColor(Color(1, 1, 0, 0.5))
        elif self.car.flag == 3:
            self.setBackgroundColor(Color(0, 0, 0, 1))
        elif self.car.flag == 4:
            self.setBackgroundColor(Color(1, 1, 1, 1))
            self.text.setTextColor(Color(0, 0, 0))
        elif self.car.flag == 5:
            self.setBackgroundColor(Color(0.5, 0.5, 0.5, 1))
        elif self.car.flag == 6:
            self.setBackgroundColor(Color(1, 0.5, 0, 1))
        else:
            self.setBackgroundColor(Color(0, 0, 0, 0.5))

    def posChange(self, car_index):
        if self.car.benefit > 0:
            self.setBackgroundColor(Color(0, 1, 0, 0.5))
        else:
            self.setBackgroundColor(Color(1, 0, 0, 0.5))

        self.text.setText(self.car.benefit)
