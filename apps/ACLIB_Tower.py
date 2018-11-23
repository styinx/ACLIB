from source.animation import Animation
from source.color import Color
from source.math import Rect
from source.gui import ACApp, ACGrid, ACLabel
from source.aclib import ACLIB, SESSION, formatTime, pad
from source.gl import rect, quad, Texture
from source.event import LIB_EVENT

TOWER_BG_COLOR = Color(0.1, 0.1, 0.1, 0.75)
TOWER_BEST_COLOR = Color(0.7, 0.3, 1, 1)
TOWER_BEST_COLOR_05 = Color(0.7, 0.3, 1, 0.5)
TOWER_GOOD_COLOR = Color(0, 0.75, 0, 1)
TOWER_GOOD_COLOR_05 = Color(0, 0.75, 0, 0.5)
TOWER_OK_COLOR = Color(0.85, 0.85, 0, 1)
TOWER_OK_COLOR_05 = Color(0.85, 0.85, 0, 0.5)
TOWER_BAD_COLOR = Color(0.75, 0, 0, 1)
TOWER_BAD_COLOR_05 = Color(0.75, 0, 0, 0.5)

TOWER_BAD_SHIFT = 0.95
TOWER_GOOD_SHIFT = 0.90


class Tower(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Tower", 200, 200, 256, 256)

        self.hideDecoration()

        self.show_classes = False
        self.classes = ""
        self.entries = {}

        self.max_rows = 24
        self.row_width = 432
        self.row_height = 32
        self.col_width = 6
        self.cols = (int(ACLIB.getCarsCount() / self.max_rows) + 1)
        self.setSize((self.row_width * self.cols, self.max_rows * self.row_height))

        for car in ACLIB.CARS:
            if self.classes == "":
                self.classes = car.car_class
            elif self.classes != car.car_class:
                self.show_classes = True
                break

        for car in ACLIB.CARS:
            x = int((car.position - 1) / self.max_rows) * self.row_width
            y = (car.position - 1) % self.max_rows * self.row_height
            self.entries[car.number] = TowerEntry(x, y, self.row_width, self.row_height, self, car.number,
                                                  self.show_classes)
            self.entries[car.number].setPos(0, (car.position - 1) % self.max_rows * self.row_height)
            car.setEvent(LIB_EVENT.ON_POSITION_CHANGED, self.swap)

    def swap(self, car_index):
        car_entry = self.entries[car_index]
        car_entry.setPos(0, (ACLIB.CARS[car_index].position - 1) % self.max_rows * self.row_height)

    def update(self, delta):
        super().update(delta)

        for entry in self.entries:
            self.entries[entry].update(delta)

    def render(self, delta):
        super().render(delta)

        for entry in self.entries:
            self.entries[entry].render(delta)

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
            "porsche cup":       Color(0.1, 0.5, 0.1, 1),
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


class TowerEntry:
    def __init__(self, x, y, w, h, app, car_index, show_class=False):
        self.init = False
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.benefit_marker = True
        self.car_index = car_index
        self.car = ACLIB.CARS[self.car_index]

        self.position = ACLabel("", app, font_size=20, bold=1, text_h_alignment="center", text_v_alignment="middle",
                                text_color=Color(0, 0, 0), background_color=Color(0, 0, 0))
        self.car_class = ACLabel("", app, background_color=Color(0, 0, 0, 1))
        self.name = ACLabel("", app, font_size=16, bold=1, text_h_alignment="left", text_v_alignment="middle",
                            background_color=Color(0, 0, 0, 0.75))
        self.time = ACLabel("", app, font_size=16, bold=1, text_h_alignment="left", text_v_alignment="middle",
                            background_color=Color(0, 0, 0, 0.75))
        self.info = ACLabel("", app, font_size=16, bold=1, italic=1, text_h_alignment="center",
                            text_v_alignment="middle", background_color=Color(0, 0, 0, 0))

        self.name.setBackgroundColor(Color(0, 0, 0, 0.75))
        self.time.setBackgroundColor(Color(1, 1, 1, 0.75)).setTextColor(Color(0, 0, 0, 1))

        if show_class:
            self.position.setBackgroundColor(Tower.getClassColor(self.car.car_class))
        self.position.setBackgroundTexture(Texture("apps/python/ACLIB/resources/tower_position_background.png"))
        self.car_class.setBackgroundTexture(self.car.car_badge)

        self.car.setEvent(LIB_EVENT.ON_LAP_CHANGED, self.reset)

    def reset(self, car_index):
        self.benefit_marker = True

    def setPos(self, x, y):
        self.position.setGeometry(Rect(0, y, 32, 30))
        self.car_class.setGeometry(Rect(32, y, 32, 30))
        self.name.setGeometry(Rect(64, y, 240, 30))
        self.time.setGeometry(Rect(304, y, 96, 30))
        self.info.setGeometry(Rect(400, y, 32, 30))

    def update(self, delta):
        self.position.update(delta)
        self.name.update(delta)
        self.time.update(delta)
        self.info.update(delta)

        # if not self.init:
        #     self.init = True
        #
        #     start = self.name.getGeometry().set(w=0, h=0)
        #     step = Rect(0, 0, 240 / 1000, 30 / 1000)
        #     stop = self.name.getGeometry().set(w=240, h=30)
        #     self.name.addAnimation(Animation(self.name, "_geometry", start, step, stop))

        self.position.setText(str(self.car.position))
        self.name.setText(pad(self.car.number) + " | " + self.car.player_nick)

        if self.car.number == ACLIB.getFocusedCar():
            self.name.setBackgroundColor(Color(1, 0.5, 0, 0.75))
        else:
            self.name.setBackgroundColor(Color(0, 0, 0, 0.75))

        if self.car.next_time > 0:
            if ACLIB.getSessionTypeId() == 1:
                self.time.setText("+" + formatTime((ACLIB.CARS[self.car.next].best_time - self.car.best_time) * 1000))
            elif ACLIB.getSessionTypeId() == 2:
                self.time.setText("+" + formatTime(self.car.next_time * 1000))
        else:
            self.time.setText(" " + formatTime(self.car.lap_time))

        if self.car.in_pit:
            self.info.setText("PIT")
            self.info.setBackgroundColor(Color(1, 0.75, 0, 1))

        else:
            if self.car.penalty_time > 0:
                self.info.setText(str(int(self.car.penalty_time)) + "s")
                self.info.setBackgroundColor(Color(1, 0.25, 0, 1))

            else:
                if self.car.benefit > 0 and self.benefit_marker:
                    if not self.info.hasAnimation():
                        start = Color(0, 0, 0, 1)
                        step = Color(0, 0.01, 0, 0)
                        stop = Color(0, 1, 0, 1)
                        self.info.addAnimation(Animation(self.info, "_background_color", start, step, stop,
                                                         direction="Alternate"))
                        self.benefit_marker = False
                    self.info.setText("+" + str(self.car.benefit))

                elif self.car.benefit < 0 and self.benefit_marker:
                    if not self.info.hasAnimation():
                        start = Color(0, 0, 0, 1)
                        step = Color(0.01, 0, 0, 0)
                        stop = Color(1, 0, 0, 1)
                        self.info.addAnimation(Animation(self.info, "_background_color", start, step, stop,
                                                         direction="Alternate"))
                    self.benefit_marker = False
                    self.info.setText(str(self.car.benefit))

                else:
                    self.info.setText("")
                    self.info.setBackgroundColor(Color(0, 0, 0, 0))

        return self

    def render(self, delta):
        self.position.render(delta)
        self.name.render(delta)
        self.time.render(delta)
        self.info.render(delta)

        if self.car.lap > 1:

            x, y = self.name.getPos()
            w, h = self.name.getSize()

            w -= 2

            o = x + 1
            for sector in range(0, self.car.sector_index + 1):
                color = Color(0.85, 0.85, 0)
                if self.car.sector_time[sector] <= SESSION.best_sector_time[sector]:
                    color = Color(0.7, 0.3, 1)
                elif self.car.sector_time[sector] <= self.car.best_sector_time[sector]:
                    color = Color(0, 0.75, 0)

                rect(o, y + 22, w / 3, 4, color)
                rect(o, y + 22, w / 3, 4, Color(0, 0, 0, 1), False)
                o += w / 3

            o = x + 1
            for mini_sector in range(0, self.car.mini_sector_index + 1):
                color = Color(0.85, 0.85, 0)
                if self.car.mini_sector_time[mini_sector] <= SESSION.best_mini_sector_time[mini_sector]:
                    color = Color(0.7, 0.3, 1)
                elif self.car.mini_sector_time[mini_sector] <= self.car.best_mini_sector_time[mini_sector]:
                    color = Color(0, 0.75, 0)

                rect(o, y + 26, w / 12, 4, color)
                rect(o, y + 26, w / 12, 4, Color(0, 0, 0, 1), False)
                o += w / 12
