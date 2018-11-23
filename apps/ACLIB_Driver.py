from time import strftime, localtime
from source.gui import ACApp, ACLabel, ACGrid, ACLabelPair
from source.widget import ACDeltaBarWidget, ACTyreWidget, ACTwinShiftLightWidget
from source.aclib import ACLIB, SESSION, s, formatTime, formatTimeCar, formatDistance, formatGear
from source.gl import Texture
from source.color import Color
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
        super().__init__("ACLIB_Driver", 200, 200, 576, 288)

        # try:
        #     db = DB("test.sql")
        # except:
        #     ACLIB.CONSOLE("test")

        self.hideDecoration().setBackgroundColor(Color(0.2, 0.2, 0.2, 0.75))

        self.car = ACLIB.CARS[ACLIB.getFocusedCar()]
        self._grid = ACGrid(self, 18, 11)

        self.next1_tex = Texture("apps/python/ACLIB/resources/next_1.png")
        self.next2_tex = Texture("apps/python/ACLIB/resources/next_2.png")
        self.m_panel_tex = Texture("apps/python/ACLIB/resources/info_panel_mid.png")
        self.prev1_tex = Texture("apps/python/ACLIB/resources/prev_1.png")
        self.prev2_tex = Texture("apps/python/ACLIB/resources/prev_2.png")
        self.status_tex = Texture("apps/python/ACLIB/resources/status.png")
        self.shift_tex = Texture("apps/python/ACLIB/resources/shift.png")

        self.lap = ACLabel("", self, font_size=20, italic=1, bold=1, background_color=DRIVER_BG_COLOR)
        self.pos = ACLabel("", self, font_size=20, italic=1, bold=1, background_color=DRIVER_BG_COLOR)
        self.last = ACLabel("", self, font_size=16, bold=1, background_color=DRIVER_BG_COLOR, text_h_alignment="center")
        self.best = ACLabel("", self, font_size=16, bold=1, background_color=DRIVER_BG_COLOR, text_h_alignment="center")

        self.rpm = ACLabel("", self, font_size=20, italic=1, background_color=DRIVER_BG_COLOR,
                           text_h_alignment="center")
        self.gear = ACLabel("", self, font_size=120, bold=1, background_color=DRIVER_BG_COLOR,
                            text_h_alignment="center")
        self.drs = ACLabel("", self, font_size=16, bold=1, background_color=DRIVER_BG_COLOR,
                           text_h_alignment="center")
        self.ers = ACLabel("", self, font_size=16, bold=1, background_color=DRIVER_BG_COLOR,
                           text_h_alignment="center")
        self.kers = ACLabel("", self, font_size=16, bold=1, background_color=DRIVER_BG_COLOR,
                            text_h_alignment="center")

        self.fuel = ACLabel("", self, font_size=14)
        self.fuel_lap_range = ACLabel("", self, font_size=14)
        self.fuel_lap_consumption = ACLabel("", self, font_size=14)
        self.local_time = ACLabel("", self, font_size=20, bold=1)

        self.next_time = ACLabel("", self, font_size=20, bold=1, background_color=DRIVER_BG_COLOR,
                                 text_h_alignment="left")
        self.next_dist = ACLabel("", self, font_size=20, bold=1, background_color=DRIVER_BG_COLOR,
                                 text_h_alignment="left")
        self.current = ACLabel("", self, font_size=20, bold=1, background_color=DRIVER_BG_COLOR,
                               text_h_alignment="center")
        self.s1 = ACLabel("", self, font_size=14, bold=1, background_color=DRIVER_BG_COLOR,
                          text_h_alignment="center")
        self.s2 = ACLabel("", self, font_size=14, bold=1, background_color=DRIVER_BG_COLOR,
                          text_h_alignment="center")
        self.s3 = ACLabel("", self, font_size=14, bold=1, background_color=DRIVER_BG_COLOR,
                          text_h_alignment="center")
        self.delta_widget = ACLabelPair(self, label_pos="top",
                                        label=ACLabel("", self, font_size=16, bold=1, text_h_alignment="center"),
                                        widget=ACDeltaBarWidget())
        self.shift_widget = ACTwinShiftLightWidget()
        self.tyre_widget = ACTyreWidget()
        self.status = ACLabel("", self, font_size=30, bold=1, background_color=DRIVER_BG_COLOR,
                              text_h_alignment="center")
        self.prev_time = ACLabel("", self, font_size=20, bold=1, background_color=DRIVER_BG_COLOR,
                                 text_h_alignment="right")
        self.prev_dist = ACLabel("", self, font_size=20, bold=1, background_color=DRIVER_BG_COLOR,
                                 text_h_alignment="right")

        # self.drs.setBackgroundTexture(self.status_tex)
        # self.ers.setBackgroundTexture(self.status_tex)
        # self.kers.setBackgroundTexture(self.status_tex)

        self.next_time.setBackgroundTexture(self.next1_tex)
        self.next_dist.setBackgroundTexture(self.next1_tex)
        self.current.setBackgroundTexture(self.m_panel_tex)
        self.delta_widget.setBackgroundTexture(self.m_panel_tex)
        self.status.setBackgroundTexture(self.m_panel_tex)
        self.prev_time.setBackgroundTexture(self.prev1_tex)
        self.prev_dist.setBackgroundTexture(self.prev1_tex)

        self._grid.addWidget(self.lap, 0, 1, 3, 1)
        self._grid.addWidget(self.pos, 0, 2, 3, 1)
        self._grid.addWidget(self.last, 0, 5, 6, 1)
        self._grid.addWidget(self.best, 0, 6, 6, 1)

        self._grid.addWidget(self.rpm, 8, 0, 2, 1)
        self._grid.addWidget(self.gear, 6, 1, 6, 6)

        self._grid.addWidget(self.fuel, 12, 1, 3, 1)
        self._grid.addWidget(self.fuel_lap_consumption, 12, 2, 3, 1)
        self._grid.addWidget(self.fuel_lap_range, 15, 2, 3, 1)
        self._grid.addWidget(self.local_time, 15, 3, 2, 1)
        self._grid.addWidget(self.tyre_widget, 12, 3, 5, 3)

        self._grid.addWidget(self.prev_time, 2, 7, 4, 1)
        self._grid.addWidget(self.prev_dist, 2, 8, 4, 1)
        self._grid.addWidget(self.current, 6, 7, 6, 1)
        self._grid.addWidget(self.s1, 6, 8, 2, 1)
        self._grid.addWidget(self.s2, 8, 8, 2, 1)
        self._grid.addWidget(self.s3, 10, 8, 2, 1)
        self._grid.addWidget(self.delta_widget, 6, 9, 6, 2)
        self._grid.addWidget(self.next_time, 12, 7, 4, 1)
        self._grid.addWidget(self.next_dist, 12, 8, 4, 1)

        self._grid.updateSize()

        self.readConfig("apps/python/ACLIB/config/ACLIB_Driver.ini")

    def init(self):
        if ACLIB.hasDRS(self.car.number):
            self._grid.addWidget(self.drs, 16, 1, 2, 1)
        if ACLIB.hasERS(self.car.number):
            self._grid.addWidget(self.ers, 16, 2, 2, 1)
        if ACLIB.hasKERS(self.car.number):
            self._grid.addWidget(self.kers, 16, 3, 2, 1)

    def update(self, delta):
        super().update(delta)

        self.tyre_widget\
            .setTemperature(self.car.tyre_temp)\
            .setPressure(self.car.tyre_pressure)\
            .setWear(self.car.tyre_wear)\
            .setDirt(self.car.tyre_dirt)

        if self.car.number != ACLIB.getFocusedCar():
            self.car = ACLIB.CARS[ACLIB.getFocusedCar()]

        if self.car.rpm / self.car.max_rpm >= DRIVER_BAD_SHIFT:
            self.rpm.setTextColor(DRIVER_BAD_COLOR)
            self.gear.setBackgroundColor(DRIVER_BAD_COLOR_05)
        elif self.car.rpm / self.car.max_rpm >= DRIVER_GOOD_SHIFT:
            self.rpm.setTextColor(DRIVER_OK_COLOR)
            self.gear.setBackgroundColor(DRIVER_OK_COLOR_05)
        else:
            self.rpm.setTextColor(Color(1, 1, 1, 1))
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

        self.delta_widget.pair_widget.setDelta(self.car.lap_diff)
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

        self.lap.setText("L: {:}/{:}".format(self.car.lap, ACLIB.getLaps()))
        self.pos.setText("P: {:}/{:}".format(self.car.position, ACLIB.getCarsCount()))
        self.last.setText("LST: " + formatTime(self.car.last_time))
        self.best.setText("BST: " + formatTime(self.car.best_time))

        self.gear.setText(formatGear(self.car.gear))
        self.rpm.setText("{:4.0f}".format(self.car.rpm))

        self.fuel.setText(str(round(self.car.fuel, 2)) + " l")
        self.fuel_lap_consumption.setText(str(round(self.car.lap_fuel, 2)) + " l/lap")
        self.fuel_lap_range.setText("(+" + s(round(self.car.lap_fuel_range, 2), " lap") + ")")
        self.local_time.setText(strftime("%H:%M:%S", localtime()))

        self.s1.setText(formatTime(self.car.sector_time[0], "{:d}:{:02d}.{:03d}"))
        self.s2.setText(formatTime(self.car.sector_time[1], "{:d}:{:02d}.{:03d}"))
        self.s3.setText(formatTime(self.car.sector_time[2], "{:d}:{:02d}.{:03d}"))

        self.prev_time.setText("-" + formatTimeCar(self.car.prev_time, self.car.prev_dist, ACLIB.getTrackLength()))
        self.prev_dist.setText("-" + formatDistance(self.car.prev_dist))
        self.current.setText(formatTime(self.car.lap_time))
        # self.status.setText(status)
        self.next_time.setText("+" + formatTimeCar(self.car.next_time, self.car.next_dist, ACLIB.getTrackLength()))
        self.next_dist.setText("+" + formatDistance(self.car.next_dist))

    def render(self, delta):
        super().render(delta)




# def optimalTemp(class_name):
#     temps = {
#         "90s touring": (75, 85),
#         "f138": ,
#         "f2004": ,
#         "fabarth": ,
#         "gt4": ,
#         "gte-gt3": ,
#         "hypercars r": ,
#         "lmp1": ,
#         "lmp3": ,
#         "porsche cup": ,
#         "proto c": ,
#         "rally": ,
#         "sf70h": ,
#         "sf15t": ,
#         "small sports": ,
#         "sportscars": ,
#         "supercars": ,
#         "suv": ,
#         "vintage touring": ,
#         "vintage gt": ,
#         "vintage supercars": ,
#     }
