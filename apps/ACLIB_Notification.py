from source.aclib import ACLIB, formatTimeCar
from source.animation import Animation
from source.color import Color
from source.event import LIB_EVENT
from source.gui import ACApp, ACGrid, ACLabel


class Notification(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Notification", 200, 200, 288, 64)

        self.hideDecoration().setBackgroundColor(Color(0, 0, 0, 0))

        self.car = ACLIB.CARS[0]
        self.grid = ACGrid(self, 5, 3)
        self.text = ACLabel("", self, font_size=20, bold=1, text_h_alignment="center", text_color=Color(1, 1, 1))
        self.timeout = 3
        self.timer = 0

        self.grid.addWidget(self.text, 0, 0, 5, 3)

        self.car.setEvent(LIB_EVENT.ON_FLAG_CHANGED, self.flagChange)
        self.car.setEvent(LIB_EVENT.ON_POSITION_LOST, self.posLost)
        self.car.setEvent(LIB_EVENT.ON_POSITION_GAINED, self.posGained)

    def update(self, delta):
        super().update(delta)

        self.timer += delta

        if self.timer > self.timeout:
            self.reset()

    def render(self, delta):
        super().render(delta)

    def reset(self):
        self.timer = 0
        self.animation = None
        self.setBackgroundColor(Color(0, 0, 0, 0))
        self.text.setTextColor(Color(1, 1, 1))
        self.text.setText("")

    def flagChange(self, car_index):
        self.reset()

        if self.car.flag == 1:
            self.text.setText("Faster car behind!")
            self.setBackgroundColor(Color(0, 0.5, 1, 0.5))
        elif self.car.flag == 2:
            start = Color(0, 0, 0, 0.5)
            step = Color(0.1, 0.1, 0, 0)
            stop = Color(1, 1, 0, 0.5)
            self.addAnimation(Animation(self, "background_color", start, step, stop, 0, "Alternate"))
            self.text.setText("Yellow Flag ahead!").setTextColor(Color(0, 0, 0))
        elif self.car.flag == 3 or self.car.flag == 6:
            self.setBackgroundColor(Color(1, 0.75, 0, 0.5))
            self.text.setText("Penalty: " + self.car.penalty_time + "s").setTextColor(Color(0, 0, 0))
        elif self.car.flag == 4:
            self.setBackgroundColor(Color(1, 1, 1, 1))
            self.text.setTextColor(Color(0, 0, 0))
        elif self.car.flag == 5:
            self.text.setText("Race over")
            self.setBackgroundColor(Color(0.5, 0.5, 0.5, 1))

    def posLost(self, car_index):
        self.reset()

        self.setBackgroundColor(Color(0.75, 0, 0, 0.5))
        next_car = formatTimeCar(self.car.prev_time, self.car.prev_dist, ACLIB.getTrackLength())

        if self.car.position == ACLIB.getCarsCount():
            self.text.setText("You lost a position!\nNo car is behind, you are last!")
        else:
            self.text.setText("You lost a position!\nNext car is " + next_car + " behind")

    def posGained(self, car_index):
        self.reset()

        self.setBackgroundColor(Color(0, 0.75, 0, 0.5))
        prev_car = formatTimeCar(self.car.next_time, self.car.next_dist, ACLIB.getTrackLength())

        if self.car.position == 1:
            self.text.setText("You gained a position!\nNo car ahead, you are first!")
        else:
            self.text.setText("You gained a position!\nNext car is " + prev_car + " ahead")
