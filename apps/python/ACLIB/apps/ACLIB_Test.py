from source.aclib import ACLIB
from source.color import Color
from source.gui import ACApp, ACAreaGraph, ACGrid, ACDragableWidget, ACLabel, ACDockingWidget


class Test(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Test", 200, 200, 200, 200)

        self.hideDecoration()
        self.car = ACLIB.CARS[0]
        # self.graph = ACAreaGraph(self)

        # self.grid = ACGrid(self, 2, 2)
        #
        # self.d1 = ACDockingWidget(None)
        # self.d1.setBackgroundColor(Color(1, 0, 0))
        # self.d2 = ACDragableWidget(None)
        # self.d2.setBackgroundColor(Color(0, 0, 1))
        #
        # self.grid.addWidget(self.d1, 0, 0, 1, 1)
        # self.grid.addWidget(self.d2, 1, 1, 1, 1)

        self.grid = ACGrid(self, 2, 2)

        self.d2 = ACDockingWidget(self, 5).setBackgroundColor(Color(1, 0, 0))
        self.grid.addWidget(self.d2, 0, 0, 1, 1)

    def update(self, delta):
        super().update(delta)

        # self.graph[round(self.car.location * 30)] = round(self.car.speed, 2)

    def render(self, delta):
        super().render(delta)
