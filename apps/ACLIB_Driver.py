from source.gui import ACApp, ACLabel, ACGrid
from source.aclib import ACLIB, formatTime, formatDistance
from source.gl import Texture, texture_rect


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

        self.next_time = ACLabel("", self, font_size=20, bold=1, text_h_alignment="center", text_v_alignment="middle")
        self.next_dist = ACLabel("", self, font_size=20, bold=1, text_h_alignment="center", text_v_alignment="middle")
        self.current = ACLabel("", self, font_size=20, bold=1, text_h_alignment="center", text_v_alignment="middle")
        self.diff = ACLabel("", self, font_size=20, bold=1, text_h_alignment="center", text_v_alignment="middle")
        self.prev_time = ACLabel("", self, font_size=20, bold=1, text_h_alignment="center", text_v_alignment="middle")
        self.prev_dist = ACLabel("", self, font_size=20, bold=1, text_h_alignment="center", text_v_alignment="middle")

        self.next_time.setBackgroundTexture(self.next1_tex)
        self.next_dist.setBackgroundTexture(self.next1_tex)
        self.current.setBackgroundTexture(self.middle_panel_tex)
        self.diff.setBackgroundTexture(self.middle_panel_tex)
        self.prev_time.setBackgroundTexture(self.prev1_tex)
        self.prev_dist.setBackgroundTexture(self.prev1_tex)

        self._grid.addWidget(self.prev_time, 0, 9, 6, 1)
        self._grid.addWidget(self.prev_dist, 1, 10, 5, 1)
        self._grid.addWidget(self.current, 6, 9, 6, 1)
        self._grid.addWidget(self.diff, 6, 10, 6, 1)
        self._grid.addWidget(self.next_time, 12, 9, 6, 1)
        self._grid.addWidget(self.next_dist, 12, 10, 5, 1)

        self.render_func = self.render

        self.setRenderCallback(self.render_func)

    def update(self, delta):
        super().update(delta)

        self.prev_time.setText("+" + formatTime(self.car.prev_time * 1000))
        self.prev_dist.setText("+" + formatDistance(self.car.prev_dist))
        self.current.setText(formatTime(self.car.lap_time))
        self.diff.setText(formatTime(self.car.lap_diff * 1000))
        self.next_time.setText("-" + formatTime(self.car.next_time * 1000))
        self.next_dist.setText("-" + formatDistance(self.car.next_dist))

    def render(self, delta):
        super().render(delta)
