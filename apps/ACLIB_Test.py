from source.aclib import ACLIB, formatTimeCar, SESSION
from source.gui import ACApp, ACGrid, ACLabel, ACProgressBar
from source.widget import ACFuelWidget
import random


class Test(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Test", 200, 200, 512, 96)

        self.hideDecoration()

        self.grid = ACGrid(self, 5, 5)

        self.s1 = ACFuelWidget(self)
        self.s2 = ACProgressBar(self, 0, 50)
        self.s3 = ACLabel("", self)
        self.s4 = ACLabel("", self)

        self.grid.addWidget(self.s1, 0, 0, 5, 1)
        self.grid.addWidget(self.s2, 0, 1, 5, 1)
        self.grid.addWidget(self.s3, 0, 2, 5, 1)
        self.grid.addWidget(self.s4, 0, 3, 5, 1)

        self.grid.updateSize()

    def update(self, delta):
        super().update(delta)

        car = ACLIB.CARS[0]
        self.s2.value = random.randint(0, 100)
        self.s4.setText(formatTimeCar(car.rel_next_time, car.rel_next_dist, ACLIB.getTrackLength()) + " " +
                        formatTimeCar(car.rel_prev_time, car.rel_prev_dist, ACLIB.getTrackLength()))

    def render(self, delta):
        super().render(delta)
