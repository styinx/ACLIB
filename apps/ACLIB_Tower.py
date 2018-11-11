from source.color import Color
from source.gui import ACApp, ACGrid, ACLabel
from source.aclib import ACLIB, formatTime
from source.gl import rect, Texture
from source.event import LIB_EVENT


class Tower(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Tower", 200, 200, 256, 256)

        self.hideDecoration()

        self.max_rows = 24
        self.row_width = 448
        self.row_height = 32
        self.col_width = 6
        self.cols = (int(ACLIB.getCarsCount() / self.max_rows) + 1)
        self.setSize((self.row_width * self.cols, self.max_rows * self.row_height))

        self._grid = ACGrid(self, self.cols * self.col_width, self.max_rows)

        for car in ACLIB.CARS:
            car_grid = TowerEntry(self._grid, self, car.number)

            if car.position - 1 < self.max_rows:
                self._grid.addWidget(car_grid, 0, car.position - 1, self.col_width - 1, 1)
            else:
                x = int(car.position - 1 / self.max_rows)
                y = car.position % self.max_rows
                self._grid.addWidget(car_grid, x, y, self.col_width - 1, 1)

            car_grid.updateSize().init()

            car.setEvent(LIB_EVENT.ON_POSITION_CHANGED, self.sort)

    def sort(self, car):
        # car = ACLIB.CARS[car]
        # x = int(car.position - 1 / self.max_rows)
        # y = car.position % self.max_rows
        # changed = self._grid.getWidget(x, y)
        # changed_car = changed.car
        # changed_x = int(changed_car.position - 1 / self.max_rows)
        # changed_y = changed_car.position % self.max_rows
        # new = self._grid.getWidget(changed_x, changed_y)
        #
        # self._grid.addWidget(changed, x, y)
        # self._grid.addWidget(new, changed_x, changed_y)
        pass

    def update(self, delta):
        super().update(delta)

        self._grid.update(delta)

    def render(self, delta):
        super().render(delta)

        self._grid.render(delta)

    @staticmethod
    def getClassColor(class_name):
        colors = {
            "90s touring":       Color(0.5, 0, 0, 1),
            "f138":              Color(1, 0, 0, 1),
            "f2004":             Color(1, 0, 0, 1),
            "fabarth":           Color(0, 0, 0, 1),
            "gt4":               Color(0.5, 0.75, 0.25, 1),
            "gte-gt3":           Color(0.25, 0.75, 0, 1),
            "hypercars r":       Color(0.5, 0, 0, 1),
            "lmp1":              Color(0, 0.5, 1, 1),
            "lmp3":              Color(0, 1, 1, 1),
            "porsche cup":       Color(1, 0.75, 0, 1),
            "proto c":           Color(0, 0, 0, 1),
            "rally":             Color(0, 0, 0, 1),
            "sf70h":             Color(1, 0, 0, 1),
            "sf15t":             Color(1, 0, 0, 1),
            "small sports":      Color(0, 0, 0, 1),
            "sportscars":        Color(1, 1, 0, 1),
            "supercars":         Color(0.5, 0.5, 1, 1),
            "suv":               Color(0, 0, 0, 1),
            "vintage touring":   Color(0, 0, 0, 1),
            "vintage gt":        Color(0, 0, 0, 1),
            "vintage supercars": Color(0, 0, 0, 1)
        }

        if class_name in colors.keys():
            return colors[class_name]
        else:
            return Color(1, 1, 1, 1)


class TowerEntry(ACGrid):
    def __init__(self, parent, app, car_index):
        super().__init__(parent, 12, 1)

        self.car_index = car_index
        self.car = ACLIB.CARS[self.car_index]
        self.position = ACLabel("", app, font_size=20, bold=1, text_h_alignment="center", text_v_alignment="middle",
                                text_color=Color(0, 0, 0, 1), background_color=Color(0, 0, 0, 0.75))
        self.car_class = ACLabel("", app, background_color=Color(0, 0, 0, 0.5))
        self.name = ACLabel("", app, font_size=16, bold=1, text_h_alignment="left", text_v_alignment="middle",
                            background_color=Color(0, 0, 0, 0.5))
        self.time = ACLabel("", app, font_size=16, bold=1, text_h_alignment="left", text_v_alignment="middle",
                            background_color=Color(0, 0, 0, 0.5))
        self.info = ACLabel("", app, font_size=16, bold=1, italic=1, text_h_alignment="center",
                            text_v_alignment="middle", background_color=Color(0, 0, 0, 0.5))

        self.position.setBackgroundTexture(Texture("apps/python/ACLIB/resources/tower_position_background.png"))
        self.position.setBackgroundColor(Tower.getClassColor(self.car.car_class))
        self.car_class.setBackgroundTexture(ACLIB.getCarBadge(self.car.number))

    def init(self):
        self.addWidget(self.position, 0, 0)
        self.addWidget(self.car_class, 1, 0, 1)
        self.addWidget(self.name, 2, 0, 6)
        self.addWidget(self.time, 8, 0, 3)
        self.addWidget(self.info, 11, 0, 1)

        return self

    def update(self, delta):
        super().render(delta)

        self.position.setText(str(self.car.position))
        self.name.setText(self.car.player_nick)

        if self.car.number == ACLIB.getFocusedCar():
            self.name.setBackgroundColor(Color(0, 0.75, 0, 0.75))

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
                    self.info.setText(str(self.car.benefit))
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

            rect(x, pos[1] + 22, int(size[0] / 3), 4, color)
            rect(x, pos[1] + 22, int(size[0] / 3), 4, Color(0, 0, 0, 1), False)
            x += int(size[0] / 3)

        x = pos[0]
        for mini_sector in range(0, self.car.mini_sector_index + 1):
            color = Color(0.85, 0.85, 0)
            if self.car.mini_sector_time[mini_sector] < self.car.best_mini_sector_time[mini_sector]:
                color = Color(0, 0.75, 0)

            rect(x, pos[1] + 28, int(size[0] / 12), 4, color)
            rect(x, pos[1] + 28, int(size[0] / 12), 4, Color(0, 0, 0, 1), False)
            x += int(size[0] / 12)
