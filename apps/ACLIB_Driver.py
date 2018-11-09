from source.gui import ACApp, ACLabel, ACGrid
from source.aclib import ACLIB, formatTime, formatTimeCar, formatDistance, formatGear
from source.gl import Texture
from source.color import Color


class Driver(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Driver", 200, 200, 576, 320)

        self.hideDecoration()

        self.car = ACLIB.CARS[0]
        self._grid = ACGrid(self, 18, 12)

        self.next1_tex = Texture("apps/python/ACLIB/resources/next_1.png")
        self.next2_tex = Texture("apps/python/ACLIB/resources/next_2.png")
        self.middle_panel_tex = Texture("apps/python/ACLIB/resources/info_panel_mid.png")
        self.prev1_tex = Texture("apps/python/ACLIB/resources/prev_1.png")
        self.prev2_tex = Texture("apps/python/ACLIB/resources/prev_2.png")

        self.rpm = ACLabel("", self, font_size=20, italic=1, text_h_alignment="center", text_v_alignment="middle")
        self.gear = ACLabel("", self, font_size=150, bold=1, text_h_alignment="center", text_v_alignment="middle")

        self.s1 = ACLabel("", self, font_size=14)
        self.s2 = ACLabel("", self, font_size=14)
        self.s3 = ACLabel("", self, font_size=14)

        self.next_time = ACLabel("", self, font_size=20, bold=1, text_h_alignment="left", text_v_alignment="middle")
        self.next_dist = ACLabel("", self, font_size=20, bold=1, text_h_alignment="left", text_v_alignment="middle")
        self.current = ACLabel("", self, font_size=20, bold=1, text_h_alignment="center", text_v_alignment="middle")
        self.diff = ACLabel("", self, font_size=20, bold=1, text_h_alignment="center", text_v_alignment="middle")
        self.status = ACLabel("", self, font_size=30, bold=1, text_h_alignment="center", text_v_alignment="middle")
        self.prev_time = ACLabel("", self, font_size=20, bold=1, text_h_alignment="right", text_v_alignment="middle")
        self.prev_dist = ACLabel("", self, font_size=20, bold=1, text_h_alignment="right", text_v_alignment="middle")

        self.rpm.setBackgroundColor(Color(0.3, 0.3, 0.3, 0.75))
        self.gear.setBackgroundColor(Color(0.3, 0.3, 0.3, 0.75))
        self.s1.setBackgroundColor(Color(0.3, 0.3, 0.3, 0.75))
        self.s2.setBackgroundColor(Color(0.3, 0.3, 0.3, 0.75))
        self.s3.setBackgroundColor(Color(0.3, 0.3, 0.3, 0.75))

        self.next_time.setBackgroundTexture(self.next1_tex)
        self.next_dist.setBackgroundTexture(self.next1_tex)
        self.current.setBackgroundTexture(self.middle_panel_tex)
        self.diff.setBackgroundTexture(self.middle_panel_tex)
        self.status.setBackgroundTexture(self.middle_panel_tex)
        self.prev_time.setBackgroundTexture(self.prev1_tex)
        self.prev_dist.setBackgroundTexture(self.prev1_tex)

        self._grid.addWidget(self.rpm, 7, 0, 4, 1)
        self._grid.addWidget(self.gear, 6, 1, 6, 6)

        self._grid.addWidget(self.s1, 0, 2, 5, 1)
        self._grid.addWidget(self.s2, 0, 3, 5, 1)
        self._grid.addWidget(self.s3, 0, 4, 5, 1)

        self._grid.addWidget(self.prev_time, 0, 7, 6, 1)
        self._grid.addWidget(self.prev_dist, 1, 8, 5, 1)
        self._grid.addWidget(self.current, 6, 7, 6, 1)
        self._grid.addWidget(self.diff, 6, 8, 6, 1)
        self._grid.addWidget(self.status, 6, 9, 6, 2)
        self._grid.addWidget(self.next_time, 12, 7, 6, 1)
        self._grid.addWidget(self.next_dist, 12, 8, 5, 1)

        self.render_func = self.render

        self.setRenderCallback(self.render_func)

    def update(self, delta):
        super().update(delta)

        status = ""

        if self.car.penalty_time > 0:
            status = "Penalty: " + self.car.penalty_time + " s"
            self.status.setTextColor(Color(0.75, 0, 0, 1))
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

        self.s1.setText("Sector 1: " + formatTime(self.car.last_sector_time[0]))
        self.s2.setText("Sector 2: " + formatTime(self.car.last_sector_time[1]))
        self.s3.setText("Sector 3: " + formatTime(self.car.last_sector_time[2]))

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
