from source.color import Color
from source.gui import ACApp, ACGrid, ACLabel
from source.aclib import ACLIB, formatTime
from source.gl import rect


class Tower(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Tower", 200, 200, 256, 256)

        self.hideDecoration()

        self.max_rows = 24
        self.row_width = 416
        self.row_height = 32
        self.col_width = 6
        self.cols = (int(ACLIB.getCarsCount() / self.max_rows) + 1)
        self.setSize((self.row_width * self.cols, self.max_rows * self.row_height))

        self._grid = ACGrid(self, self.cols * self.col_width, self.max_rows)

        x = 0
        y = 0
        c = 0.2

        for car in ACLIB.CARS:
            car_grid = TowerEntry(self._grid, self, car.number)
            self._grid.addWidget(car_grid, x, y, self.col_width - 1, 1)
            car_grid.updateSize().init()

            y += 1
            c = c * -1

            if y == self.max_rows:
                y = 0
                x += self.col_width

    def update(self, delta):
        super().update(delta)

        self._grid.update(delta)

    def render(self, delta):
        super().render(delta)

        self._grid.render(delta)


class TowerEntry(ACGrid):
    def __init__(self, parent, app, car_index):
        super().__init__(parent, 10, 1)

        self.car_index = car_index
        self.car = ACLIB.CARS[self.car_index]
        col_diff = 0.2 if car_index % 2 == 0 else -0.2
        self.position = ACLabel("", app, font_size=16, bold=1, text_h_alignment="center", text_v_alignment="middle",
                                background_color=Color(0.2 + col_diff, 0.2 + col_diff, 0.2 + col_diff, 0.75))
        self.name = ACLabel("", app, font_size=16, text_h_alignment="center", text_v_alignment="middle",
                            background_color=Color(0.5 + col_diff, 0.5 + col_diff, 0.5 + col_diff, 0.75))
        self.time = ACLabel("", app, font_size=16, bold=1, text_h_alignment="center", text_v_alignment="middle",
                            background_color=Color(0.1, 0.1, 0.1, 0.5))
        self.info = ACLabel("", app, font_size=16, bold=1, italic=1,
                            text_h_alignment="center", text_v_alignment="middle")

        if self.car.number == ACLIB.getFocusedCar():
            self.name.setBackgroundColor(Color(0, 0.75, 0, 0.75))

    def init(self):
        self.addWidget(self.position, 0, 0)
        self.addWidget(self.name, 1, 0, 5)
        self.addWidget(self.time, 6, 0, 3)
        self.addWidget(self.info, 9, 0, 1)

        return self

    def update(self, delta):
        super().render(delta)

        self.position.setText(str(self.car.position))
        self.name.setText(self.car.player_nick)

        if self.car.next_time > 0:
            self.time.setText("+" + formatTime(self.car.next_time * 1000))
        else:
            self.time.setText("")

        if self.car.in_pit:
            self.info.setText("PIT")
            self.info.setBackgroundColor(Color(1, 0.75, 0, 1))

        else:
            if self.car.penalty_time > 0:
                self.info.setText(str(round(self.car.penalty_time)) + "s")
                self.info.setBackgroundColor(Color(1, 0.25, 0, 1))

            else:
                if self.car.benefit > 0:
                    self.info.setText("+" + str(self.car.benefit))
                    self.info.setBackgroundColor(Color(0, 0.7, 0, 1))
                elif self.car.benefit < 0:
                    self.info.setText(str(self.car.benefit))
                    self.info.setBackgroundColor(Color(0.7, 0, 0, 1))
                else:
                    self.info.setText("")
                    self.info.setBackgroundColor(Color(0, 0, 0, 0))

        return self

    def render(self, delta):
        super().render(delta)

        pos = self.name.getPos()
        size = self.name.getSize()
        x = pos[0]
        for sector in range(0, self.car.sector_index + 1):
            color = Color(0.85, 0.85, 0)
            if self.car.sector_time[sector] < self.car.best_sector_time[sector]:
                color = Color(0, 0.75, 0)

            rect(x, pos[1] + 22, size[0] / 3, 6, color)
            x += size[0] / 3

        x = pos[0]
        for mini_sector in range(0, self.car.mini_sector_index + 1):
            color = Color(0.85, 0.85, 0)
            if self.car.sector_time[mini_sector] < self.car.best_sector_time[mini_sector]:
                color = Color(0, 0.75, 0)

            rect(x, pos[1] + 28, size[0] / 12, 5, color)
            x += size[0] / 12


