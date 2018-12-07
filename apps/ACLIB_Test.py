from source.aclib import ACLIB
from source.event import LIB_EVENT
from source.gui import ACApp, ACGrid, ACLabel, ACProgressBar, ACLineGraph
from source.widget import ACFuelWidget
import random


class Test(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Test", 200, 200, 512, 512)

        self.hideDecoration()

        self.car = ACLIB.CARS[0]

        self.grid = ACGrid(self, 5, 5)

        self.graph = ACLineGraph()

        self.grid.addWidget(self.graph, 0, 4, 5, 1)

        self.grid.updateSize()

        self.car.setEvent(LIB_EVENT.ON_LAP_CHANGED, self.reset)

    def reset(self, car_index):
        self.graph.points = {}

    def update(self, delta):
        super().update(delta)

        # self.graph[round(self.car.location * 100)] = round(self.car.speed)

    def render(self, delta):
        super().render(delta)
