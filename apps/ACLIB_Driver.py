from time import strftime, localtime
from source.gui import ACApp, ACLabel, ACGrid, ACLabelPair
from source.widget import ACDeltaBarWidget, ACTyreWidget, ACFuelWidget, ACShiftLightBarWidget
from source.aclib import ACLIB, SESSION, formatTime, formatTimeCar, formatGear
from source.gl import Texture
from source.color import Color, TRANSPARENT

# import sqlite3

DRIVER_BG_COLOR = Color(0.1, 0.1, 0.1, 0.75)
DRIVER_BEST_COLOR = Color(0.7, 0.3, 1, 1)
DRIVER_BEST_COLOR_05 = Color(0.7, 0.3, 1, 0.5)
DRIVER_GOOD_COLOR = Color(0, 0.75, 0, 1)
DRIVER_GOOD_COLOR_05 = Color(0, 0.75, 0, 0.5)
DRIVER_OK_COLOR = Color(0.85, 0.85, 0, 1)
DRIVER_OK_COLOR_05 = Color(0.85, 0.85, 0, 0.5)
DRIVER_BAD_COLOR = Color(0.75, 0, 0, 1)
DRIVER_BAD_COLOR_05 = Color(0.75, 0, 0, 0.5)

DRIVER_BAD_SHIFT = 0.95
DRIVER_GOOD_SHIFT = 0.90


class Driver(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Driver", 200, 200, 576, 224)

        self.hideDecoration().setBackgroundColor(Color(0, 0, 0, 0.25))

        self.car = ACLIB.CARS[ACLIB.getFocusedCar()]
        self.grid = ACGrid(self, 18, 8)

        self.next1_tex = Texture("apps/python/ACLIB/resources/next_1.png")
        self.next2_tex = Texture("apps/python/ACLIB/resources/next_2.png")
        self.m_panel_tex = Texture("apps/python/ACLIB/resources/info_panel_mid.png")
        self.prev1_tex = Texture("apps/python/ACLIB/resources/prev_1.png")
        self.prev2_tex = Texture("apps/python/ACLIB/resources/prev_2.png")
        self.status_tex = Texture("apps/python/ACLIB/resources/status.png")
        self.shift_tex = Texture("apps/python/ACLIB/resources/shift.png")

        self.lap = ACLabel("", self, font_size=20, italic=1, bold=1)
        self.pos = ACLabel("", self, font_size=20, italic=1, bold=1)
        self.last = ACLabel("", self, font_size=16, bold=1)
        self.best = ACLabel("", self, font_size=16, bold=1)

        self.gear = ACLabel("", self, font_size=100, bold=1)
        self.speed = ACLabel("", self, font_size=20, bold=1).setBackgroundColor(TRANSPARENT)
        self.drs = ACLabel("", self, font_size=16, bold=1)
        self.ers = ACLabel("", self, font_size=16, bold=1)
        self.kers = ACLabel("", self, font_size=16, bold=1)

        self.fuel_widget = ACFuelWidget(self)
        self.local_time = ACLabel("", self, font_size=20, bold=1)
        self.race_time = ACLabel("", self, font_size=20, bold=1)
        self.session_time = 0

        self.next_time = ACLabel("", self, font_size=20, bold=1)
        self.current = ACLabel("", self, font_size=20, bold=1)
        self.s1 = ACLabel("", self, font_size=14, bold=1)
        self.s2 = ACLabel("", self, font_size=14, bold=1)
        self.s3 = ACLabel("", self, font_size=14, bold=1)
        self.delta_widget = ACLabelPair(self, label_pos="top", widget=ACDeltaBarWidget(),
                                        label=ACLabel("", self, font_size=16, bold=1))
        self.shift_widget = ACShiftLightBarWidget()
        self.tyre_widget = ACTyreWidget()
        self.status = ACLabel("", self, font_size=30, bold=1)
        self.prev_time = ACLabel("", self, font_size=20, bold=1)

        self.next_time.setBackgroundTexture(self.next1_tex)
        self.current.setBackgroundTexture(self.m_panel_tex)
        self.delta_widget.setBackgroundTexture(self.m_panel_tex)
        self.status.setBackgroundTexture(self.m_panel_tex)
        self.prev_time.setBackgroundTexture(self.prev1_tex)

        self.grid.addWidget(self.lap, 0, 1, 3, 1)
        self.grid.addWidget(self.pos, 3, 1, 3, 1)
        self.grid.addWidget(self.last, 0, 2, 6, 1)
        self.grid.addWidget(self.best, 0, 3, 6, 1)
        self.grid.addWidget(self.current, 0, 4, 6, 1)
        self.grid.addWidget(self.s1, 0, 5, 2, 1)
        self.grid.addWidget(self.s2, 2, 5, 2, 1)
        self.grid.addWidget(self.s3, 4, 5, 2, 1)

        self.grid.addWidget(self.shift_widget, 0, 0, 18, 1)
        self.grid.addWidget(self.gear, 6, 1, 6, 5)
        self.grid.addWidget(self.speed, 6, 5, 6, 1)

        self.grid.addWidget(self.tyre_widget, 12, 1, 3, 3)
        self.grid.addWidget(self.local_time, 15, 1, 3, 1)
        self.grid.addWidget(self.race_time, 15, 2, 3, 1)
        self.grid.addWidget(self.fuel_widget, 15, 3, 3, 5)

        self.grid.addWidget(self.prev_time, 2, 6, 4, 1)
        self.grid.addWidget(self.delta_widget, 6, 6, 6, 2)
        self.grid.addWidget(self.next_time, 12, 6, 4, 1)

        self.fuel_widget.init()

        self.grid.updateSize()

    def init(self):
        if ACLIB.hasDRS(self.car.number):
            self.grid.addWidget(self.drs, 16, 1, 2, 1)
        if ACLIB.hasERS(self.car.number):
            self.grid.addWidget(self.ers, 16, 2, 2, 1)
        if ACLIB.hasKERS(self.car.number):
            self.grid.addWidget(self.kers, 16, 3, 2, 1)

    def update(self, delta):
        super().update(delta)

        if self.car.number != ACLIB.getFocusedCar():
            self.car = ACLIB.CARS[ACLIB.getFocusedCar()]
            self.car.init()

        if SESSION.time_left == 0:
            self.session_time += delta * 1000
        else:
            self.session_time = SESSION.time_left

        if self.car.rpm / self.car.max_rpm >= DRIVER_BAD_SHIFT:
            self.gear.setBackgroundColor(DRIVER_BAD_COLOR_05)
        elif self.car.rpm / self.car.max_rpm >= DRIVER_GOOD_SHIFT:
            self.gear.setBackgroundColor(DRIVER_OK_COLOR_05)
        else:
            self.gear.setBackgroundColor(DRIVER_BG_COLOR)

        if ACLIB.hasDRS(self.car.number):
            self.drs.setText("DRS")
            if ACLIB.DRSAvailable(self.car.number):
                if ACLIB.DRSEnabled(self.car.number):
                    self.drs.setTextColor(DRIVER_GOOD_COLOR)
                else:
                    self.drs.setTextColor(DRIVER_OK_COLOR)
            else:
                self.drs.setTextColor(Color(1, 1, 1, 1))
        if ACLIB.hasERS(self.car.number):
            self.ers.setText("ERS")
        if ACLIB.hasKERS(self.car.number):
            self.kers.setText("KERS")

        if self.car.lap_diff < 0:
            self.delta_widget.label_widget.setTextColor(DRIVER_GOOD_COLOR)
            self.delta_widget.label_widget.setText("-" + formatTime(self.car.lap_diff * 1000))
        elif self.car.lap_diff > 0:
            self.delta_widget.label_widget.setTextColor(DRIVER_BAD_COLOR)
            self.delta_widget.label_widget.setText("+" + formatTime(self.car.lap_diff * 1000))
        else:
            self.delta_widget.label_widget.setTextColor(Color(1, 1, 1, 1))
            self.delta_widget.label_widget.setText(" " + formatTime(0))

        status = ""
        if self.car.penalty_time > 0:
            status = "Penalty: " + str(int(self.car.penalty_time)) + " s"
            self.status.setTextColor(Color(1, 0.25, 0, 1))
        else:
            self.status.setTextColor(Color(1, 1, 1, 1))
            status = ""

        if self.car.lap > 1:
            if self.car.sector_time[0] == SESSION.best_sector_time[0]:
                self.s1.setTextColor(DRIVER_BEST_COLOR)
            else:
                if self.car.sector_time[0] == self.car.best_sector_time[0]:
                    self.s1.setTextColor(DRIVER_GOOD_COLOR)
                else:
                    self.s1.setTextColor(DRIVER_OK_COLOR)

            if self.car.sector_time[1] == SESSION.best_sector_time[1]:
                self.s2.setTextColor(DRIVER_BEST_COLOR)
            else:
                if self.car.sector_time[1] == self.car.best_sector_time[1]:
                    self.s2.setTextColor(DRIVER_GOOD_COLOR)
                else:
                    self.s2.setTextColor(DRIVER_OK_COLOR)

            if self.car.sector_time[2] < SESSION.best_sector_time[2]:
                self.s3.setTextColor(DRIVER_BEST_COLOR)
            else:
                if self.car.sector_time[2] == self.car.best_sector_time[2]:
                    self.s3.setTextColor(DRIVER_GOOD_COLOR)
                else:
                    self.s3.setTextColor(DRIVER_OK_COLOR)

            if not self.car.last_invalid:
                if self.car.last_time == SESSION.best_lap_time:
                    self.last.setTextColor(DRIVER_BEST_COLOR)
                else:
                    if self.car.last_time == self.car.best_time:
                        self.last.setTextColor(DRIVER_GOOD_COLOR)
                    else:
                        self.last.setTextColor(DRIVER_OK_COLOR)

                if self.car.best_time == SESSION.best_lap_time:
                    self.best.setTextColor(DRIVER_BEST_COLOR)
                else:
                    self.best.setTextColor(DRIVER_GOOD_COLOR)
            else:
                self.last.setTextColor(DRIVER_BAD_COLOR)

        self.lap.setText("L: {:}|{:}".format(self.car.lap, ACLIB.getLaps("-")))
        self.pos.setText("P: {:}|{:}".format(self.car.position, ACLIB.getCarsCount()))
        self.last.setText("LST: " + formatTime(self.car.last_time))
        self.best.setText("BST: " + formatTime(self.car.best_time))

        self.gear.setText(formatGear(self.car.gear))
        self.speed.setText("{:3.0f} km/h".format(self.car.speed))
        self.local_time.setText(strftime("%H:%M:%S", localtime()))
        self.race_time.setText(formatTime(self.session_time))

        self.s1.setText(formatTime(self.car.sector_time[0], "{:d}:{:02d}.{:03d}"))
        self.s2.setText(formatTime(self.car.sector_time[1], "{:d}:{:02d}.{:03d}"))
        self.s3.setText(formatTime(self.car.sector_time[2], "{:d}:{:02d}.{:03d}"))

        self.prev_time.setText("-" + formatTimeCar(self.car.prev_time, self.car.prev_dist, ACLIB.getTrackLength()))
        self.current.setText(formatTime(self.car.lap_time))
        self.next_time.setText("+" + formatTimeCar(self.car.next_time, self.car.next_dist, ACLIB.getTrackLength()))

    def render(self, delta):
        super().render(delta)
