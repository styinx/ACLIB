from source.color import Color
from source.gui import ACApp, ACGrid, ACLabel, ACWidget
from source.aclib import ACLIB


class Tower(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Tower", 200, 200, 256, 256)

        self.hideDecoration().setBackgroundColor(Color(0, 0, 0, 0))

        self.max_rows = 22
        self.row_width = 288
        self.row_height = 32
        self.col_width = 6
        self.cols = (int(ACLIB.getCarsCount() / self.max_rows) + 1)
        self.setSize((self.row_width * self.cols, self.max_rows * self.row_height))

        self._grid = ACGrid(self, self.cols * self.col_width, self.max_rows)

        x = 0
        y = 0
        c = 0.2

        for car in ACLIB.CARS:
            # car_grid = ACGrid(None, 8, 1).setBackgroundColor(Color(1, 0.5, 0.5, 1))
            # car_pos = ACLabel("", self, font_size=16, bold=1, text_h_alignment="center", text_v_alignment="middle",
            #                   background_color=Color(0.2 + c, 0.2 + c, 0.2 + c, 0.75))
            # player_name = ACLabel("", self, font_size=16, text_h_alignment="center", text_v_alignment="middle",
            #                       background_color=Color(0.5 + c, 0.5 + c, 0.5 + c, 0.75))
            # player_penalty = ACLabel("", self, font_size=16, bold=1, italic=1,
            #                          text_h_alignment="center", text_v_alignment="middle")

            car_grid = TowerEntry(None, self, car.number)
            self._grid.addWidget(car_grid, x, y, self.col_width - 1, 1)
            car_grid.updateSize().init()
            #
            # car_grid.addWidget(car_pos, 0, 0, 1, 1)
            # car_grid.addWidget(player_name, 1, 0, 6, 1)
            # car_grid.addWidget(player_penalty, 7, 0, 1, 1)

            y += 1
            c = c * -1

            if y == self.max_rows:
                y = 0
                x += self.col_width

    def update(self, delta):

        x = 0
        y = 0

        # for car in ACLIB.CARS:
        #     car_grid = self._grid.getWidget(x, y)
        #
        #     car_grid.getWidget(0, 0).setText(str(car.position))
        #     car_grid.getWidget(1, 0).setText(str(car.player_nick))
        #
        #     penalty = car_grid.getWidget(7, 0)
        #
        #     if car.penalty_time > 0:
        #         penalty.setText(str(round(car.penalty_time)))
        #         penalty.setBackgroundColor(Color(0.7, 0, 0, 1))
        #
        #     else:
        #         if car.benefit > 0:
        #             penalty.setText("+" + str(car.benefit))
        #             penalty.setBackgroundColor(Color(0, 0.7, 0, 1))
        #         elif car.benefit < 0:
        #             penalty.setText(str(car.benefit))
        #             penalty.setBackgroundColor(Color(0.7, 0, 0, 1))
        #         else:
        #             penalty.setText("")
        #             penalty.setBackgroundColor(Color(0, 0, 0, 1))
        #
        #     car_grid.update(delta)
        #
        #     y += 1
        #
        #     if y == self.max_rows:
        #         y = 0
        #         x += self.col_width

        for _ in range(0, ACLIB.getCarsCount()):
            car_grid = self._grid.getWidget(x, y)
            ACLIB.CONSOLE(car_grid.car_index)
            car_grid.update(delta)

            y += 1

            if y == self.max_rows:
                y = 0
                x += self.col_width

        self._grid.update(delta)

    def render(self, delta):
        super().render(delta)


class TowerEntry(ACGrid):
    def __init__(self, parent, app, car_index):
        super().__init__(parent, 8, 1)

        self.car_index = car_index
        self.car = ACLIB.CARS[self.car_index]
        col_diff = 0.2 if car_index % 2 == 0 else -0.2
        self.position = ACLabel("", app, font_size=16, text_h_alignment="center", text_v_alignment="middle",
                                background_color=Color(0.2 + col_diff, 0.2 + col_diff, 0.2 + col_diff, 0.75))
        self.name = ACLabel("", app, font_size=16, text_h_alignment="center", text_v_alignment="middle",
                            background_color=Color(0.5 + col_diff, 0.5 + col_diff, 0.5 + col_diff, 0.75))
        self.info = ACLabel("", app, font_size=16, bold=1, italic=1,
                            text_h_alignment="center", text_v_alignment="middle")

    def init(self):
        self.addWidget(self.position, 0, 0)
        self.addWidget(self.name, 1, 0, 6)
        self.addWidget(self.info, 7, 0)

        return self

    def update(self, delta):

        self.position.setText(str(self.car.position))
        self.name.setText(self.car.player_name)

        if self.car.penalty_time > 0:
            self.info.setText(str(round(self.car.penalty_time)))
            self.info.setBackgroundColor(Color(0.7, 0, 0, 1))

        else:
            if self.car.benefit > 0:
                self.info.setText("+" + str(self.car.benefit))
                self.info.setBackgroundColor(Color(0, 0.7, 0, 1))
            elif self.car.benefit < 0:
                self.info.setText(str(self.car.benefit))
                self.info.setBackgroundColor(Color(0.7, 0, 0, 1))
            else:
                self.info.setText("")
                self.info.setBackgroundColor(Color(0, 0, 0, 1))

        return self
