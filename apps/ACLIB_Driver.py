from source.gui import ACApp, ACLabel, ACGrid
from source.aclib import ACLIB, formatTime, formatTimeCar, formatDistance, formatGear
from source.gl import Texture
from source.color import Color


class Driver(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Driver", 200, 200, 576, 320)

        self.hideDecoration().setBackgroundColor(Color(0, 0, 0, 0.5))

        self.car = ACLIB.CARS[0]
        self._grid = ACGrid(self, 18, 12)

        self.next1_tex = Texture("apps/python/ACLIB/resources/next_1.png")
        self.next2_tex = Texture("apps/python/ACLIB/resources/next_2.png")
        self.m_panel_tex = Texture("apps/python/ACLIB/resources/info_panel_mid.png")
        self.prev1_tex = Texture("apps/python/ACLIB/resources/prev_1.png")
        self.prev2_tex = Texture("apps/python/ACLIB/resources/prev_2.png")
        self.status_tex = Texture("apps/python/ACLIB/resources/status.png")

        self.rpm = ACLabel("", self, font_size=20, italic=1, background_color=Color(0.3, 0.3, 0.3, 0.75),
                           text_h_alignment="center")
        self.gear = ACLabel("", self, font_size=120, bold=1, background_color=Color(0.3, 0.3, 0.3, 0.75),
                            text_h_alignment="center")
        self.drs = ACLabel("", self, font_size=16, bold=1, background_color=Color(0.3, 0.3, 0.3, 0.75),
                           text_h_alignment="center")
        self.ers = ACLabel("", self, font_size=16, bold=1, background_color=Color(0.3, 0.3, 0.3, 0.75),
                           text_h_alignment="center")
        self.kers = ACLabel("", self, font_size=16, bold=1, background_color=Color(0.3, 0.3, 0.3, 0.75),
                            text_h_alignment="center")

        self.last = ACLabel("", self, font_size=16, background_color=Color(0.3, 0.3, 0.3, 0.75),
                            text_h_alignment="center")
        self.best = ACLabel("", self, font_size=16, background_color=Color(0.3, 0.3, 0.3, 0.75),
                            text_h_alignment="center")

        self.next_time = ACLabel("", self, font_size=20, bold=1, background_color=Color(0.3, 0.3, 0.3, 0.75),
                                 text_h_alignment="left")
        self.next_dist = ACLabel("", self, font_size=20, bold=1, background_color=Color(0.3, 0.3, 0.3, 0.75),
                                 text_h_alignment="left")
        self.current = ACLabel("", self, font_size=20, bold=1, background_color=Color(0.3, 0.3, 0.3, 0.75),
                               text_h_alignment="center")
        self.s1 = ACLabel("", self, font_size=14, background_color=Color(0.3, 0.3, 0.3, 0.75),
                          text_h_alignment="center")
        self.s2 = ACLabel("", self, font_size=14, background_color=Color(0.3, 0.3, 0.3, 0.75),
                          text_h_alignment="center")
        self.s3 = ACLabel("", self, font_size=14, background_color=Color(0.3, 0.3, 0.3, 0.75),
                          text_h_alignment="center")
        self.diff = ACLabel("", self, font_size=20, bold=1, background_color=Color(0.3, 0.3, 0.3, 0.75),
                            text_h_alignment="center")
        self.status = ACLabel("", self, font_size=30, bold=1, background_color=Color(0.3, 0.3, 0.3, 0.75),
                              text_h_alignment="center")
        self.prev_time = ACLabel("", self, font_size=20, bold=1, background_color=Color(0.3, 0.3, 0.3, 0.75),
                                 text_h_alignment="right")
        self.prev_dist = ACLabel("", self, font_size=20, bold=1, background_color=Color(0.3, 0.3, 0.3, 0.75),
                                 text_h_alignment="right")

        # self.drs.setBackgroundTexture(self.status_tex)
        # self.ers.setBackgroundTexture(self.status_tex)
        # self.kers.setBackgroundTexture(self.status_tex)

        self.next_time.setBackgroundTexture(self.next1_tex)
        self.next_dist.setBackgroundTexture(self.next1_tex)
        self.current.setBackgroundTexture(self.m_panel_tex)
        self.diff.setBackgroundTexture(self.m_panel_tex)
        self.status.setBackgroundTexture(self.m_panel_tex)
        self.prev_time.setBackgroundTexture(self.prev1_tex)
        self.prev_dist.setBackgroundTexture(self.prev1_tex)

        self._grid.addWidget(self.rpm, 7, 0, 4, 1)
        self._grid.addWidget(self.gear, 6, 1, 6, 6)

        if ACLIB.hasDRS(self.car.number):
            self._grid.addWidget(self.drs, 16, 1, 2, 1)
        if ACLIB.hasERS(self.car.number):
            self._grid.addWidget(self.ers, 16, 2, 2, 1)
        if ACLIB.hasKERS(self.car.number):
            self._grid.addWidget(self.kers, 16, 3, 2, 1)

        self._grid.addWidget(self.last, 0, 5, 6, 1)
        self._grid.addWidget(self.best, 0, 6, 6, 1)

        self._grid.addWidget(self.prev_time, 2, 7, 5, 1)
        self._grid.addWidget(self.prev_dist, 2, 8, 5, 1)
        self._grid.addWidget(self.current, 6, 7, 6, 1)
        self._grid.addWidget(self.s1, 6, 8, 2, 1)
        self._grid.addWidget(self.s2, 8, 8, 2, 1)
        self._grid.addWidget(self.s3, 10, 8, 2, 1)
        self._grid.addWidget(self.diff, 6, 9, 6, 1)
        self._grid.addWidget(self.status, 7, 9, 6, 2)
        self._grid.addWidget(self.next_time, 12, 7, 5, 1)
        self._grid.addWidget(self.next_dist, 12, 8, 5, 1)

        self._grid.updateSize()

        self.render_func = self.render

        self.setRenderCallback(self.render_func)

    def update(self, delta):
        super().update(delta)

        status = ""

        if self.car.penalty_time > 0:
            status = "Penalty: " + str(int(self.car.penalty_time)) + " s"
            self.status.setTextColor(Color(1, 0.75, 0, 1))
        else:
            self.status.setTextColor(Color(1, 1, 1, 1))
            status = ""

        if self.car.lap_diff < 0:
            self.diff.setTextColor(Color(0, 0.75, 0, 1))
            self.diff.setText("-" + formatTime(self.car.lap_diff * 1000))
        elif self.car.lap_diff > 0:
            self.diff.setTextColor(Color(0.75, 0, 0, 1))
            self.diff.setText("+" + formatTime(self.car.lap_diff * 1000))
        else:
            self.diff.setTextColor(Color(1, 1, 1, 1))

        self.gear.setText(formatGear(self.car.gear))
        self.rpm.setText(self.car.rpm)

        if ACLIB.hasDRS(self.car.number):
            self.drs.setText("DRS")
            if ACLIB.DRSAvailable(self.car.number):
                if ACLIB.DRSEnabled(self.car.number):
                    self.drs.setTextColor(Color(0, 1, 0, 1))
                else:
                    self.drs.setTextColor(Color(1, 1, 0, 1))
            else:
                self.drs.setTextColor(Color(1, 1, 1, 1))
        if ACLIB.hasERS(self.car.number):
            self.ers.setText("ERS")
        if ACLIB.hasKERS(self.car.number):
            self.kers.setText("KERS")

        self.s1.setText(formatTime(self.car.last_sector_time[0], "{:d}:{:02d}.{:03d}"))
        self.s2.setText(formatTime(self.car.last_sector_time[1], "{:d}:{:02d}.{:03d}"))
        self.s3.setText(formatTime(self.car.last_sector_time[2], "{:d}:{:02d}.{:03d}"))

        self.last.setText("LST: " + formatTime(self.car.last_time))
        self.best.setText("BST: " + formatTime(self.car.best_time))

        if self.car.last_sector_time[0] <= self.car.best_sector_time[0]:
            self.s1.setTextColor(Color(0, 0.75, 0, 1))
        elif self.car.last_sector_time[0] > self.car.best_sector_time[0]:
            self.s1.setTextColor(Color(0.85, 0.85, 0, 1))

        if self.car.last_sector_time[1] <= self.car.best_sector_time[1]:
            self.s2.setTextColor(Color(0, 0.75, 0, 1))
        elif self.car.last_sector_time[1] > self.car.best_sector_time[1]:
            self.s2.setTextColor(Color(0.85, 0.85, 0, 1))

        if self.car.last_sector_time[2] <= self.car.best_sector_time[2]:
            self.s3.setTextColor(Color(0, 0.75, 0, 1))
        elif self.car.last_sector_time[2] > self.car.best_sector_time[2]:
            self.s3.setTextColor(Color(0.85, 0.85, 0, 1))

        self.prev_time.setText("-" + formatTimeCar(self.car.prev_time, self.car.prev_dist, ACLIB.getTrackLength()))
        self.prev_dist.setText("-" + formatDistance(self.car.prev_dist))
        self.current.setText(formatTime(self.car.lap_time))
        self.status.setText(status)
        self.next_time.setText("+" + formatTimeCar(self.car.next_time, self.car.next_dist, ACLIB.getTrackLength()))
        self.next_dist.setText("+" + formatDistance(self.car.next_dist))

    def render(self, delta):
        super().render(delta)
