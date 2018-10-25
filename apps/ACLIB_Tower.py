from source.color import Color
from source.gui import ACApp, ACGrid, ACLabel
from source.aclib import ACLIB


#   +-----------+   +-----------+
#   |  |     |  |   |  |     |  |
#   +-----------+   +-----------+
#
#


class Tower(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Tower", 200, 200, 200, 200)

        self.max_rows = 10
        self.row_width = 256
        self.row_space = 64
        cols = ACLIB.getCarsCount() / self.max_rows

        self.grid = ACGrid(self, cols, self.max_rows)

        x = 0
        y = 0

        for _ in range(0, len(ACLIB.CARS)):
            car_grid = ACGrid(None, 7, 1)
            car_pos = ACLabel("", self)
            player_name = ACLabel("", self)
            player_penalty = ACLabel("", self)

            self.grid.addWidget(x, y, car_grid)

            car_grid.addWidget(car_pos, 0, 1, 1, 1)
            car_grid.addWidget(player_name, 1, 1, 5, 1)
            car_grid.addWidget(player_penalty, 6, 1, 5, 1)

            y += 1

            if y == self.max_rows:
                y = 0
                x += 1

                self.setSize((self._size[0], self._size[1] + self.row_space + self.row_width))
                
    def update(self):
        super().update()

        x = 0
        y = 0

        for car in ACLIB.CARS:

            car_grid = self.grid.getWidget(x, y)

            car_grid.getWidget(0, 0).setText(str(car.position)).drawBorder(False)
            car_grid.getWidget(1, 0).setText(str(car.player_nick)).drawBorder(False)

            penalty = car_grid.getWidget(6, 0)

            if car.penalty_time > 0:
                penalty.setText(str(car.penalty_time))
                penalty.setBackgroundColor(Color(0.7, 0, 0, 1))

            else:
                penalty.setBackgroundColor(Color(0, 0, 0, 0))

            y += 1

            if y == self.max_rows:
                y = 0
                x += 1
