from source.aclib import ACLIB
from source.color import Color
from source.event import LIB_EVENT
from source.gui import ACApp, ACGrid, ACLineGraph


class Analytics(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Analytics", 200, 200, 400, 200)

        self.hideDecoration()

        self.car = ACLIB.CARS[0]
        self.granularity = 30

        self.grid = ACGrid(self, 8, 5)

        self.speed = ACLineGraph()
        self.delta = ACLineGraph()

        self.grid.addWidget(self.speed, 0, 0, 8, 2)
        self.grid.addWidget(self.delta, 0, 3, 8, 2)

        self.speed.setDrawColors([Color(0.9, 0.3, 0, 0.75), Color(1, 1, 0, 0.75), Color(0, 0.5, 0.5, 0.75)])
        self.speed.background_color = Color(0.2, 0.2, 0.2, 0.25)

        self.speed.setBackgroundColors([Color(0, 0.7, 0.7, 0.25), Color(0.9, 0.3, 0, 0.25), Color(1, 1, 0, 0.25)])
        self.delta.setBackgroundColors([Color(0.1, 0.1, 0.1, 0.4), Color(0.3, 0.3, 0.3, 0.4), Color(0.1, 0.1, 0.1, 0.4)])

        self.speed.x_max = self.granularity

        self.car.setEvent(LIB_EVENT.ON_LAP_CHANGED, self.reset)

    def reset(self, car_index):
        self.speed.reset()
        self.delta.reset()

        self.speed.x_max = self.granularity

    def update(self, delta):
        super().update(delta)

        self.speed[round(self.car.location * self.granularity)] = round(self.car.speed)
        self.delta[round(self.car.location * self.granularity)] = round(self.car.lap_diff) * - 1

    def render(self, delta):
        super().render(delta)
