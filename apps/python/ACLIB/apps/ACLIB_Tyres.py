from settings import TEXTURE_DIR, path
from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.gl import Texture, texture_rect, rect
from ui.gui.ac_widget import ACApp, ACLabel, ACWidget
from ui.gui.aclib_widget import ACLIBProgressBar
from ui.gui.layout import ACGrid
from ui.color import *
from util.log import console


class Tyres(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Tyres', 200, 200, 98, 160)

        self.hide_decoration()
        self.background_color = TRANSPARENT
        self.border_color = TRANSPARENT

        self._data = data
        self._meta = meta

        self._grid = ACGrid(5, 9, self)

        # For each tyre there is a separate class to avoid redundancy of index checking.
        self.fl = Tyre(Tyre.FL, self._grid, self._data, self._meta)
        self.fr = Tyre(Tyre.FR, self._grid, self._data, self._meta)
        self.rl = Tyre(Tyre.RL, self._grid, self._data, self._meta)
        self.rr = Tyre(Tyre.RR, self._grid, self._data, self._meta)

        self._grid.add(self.fl, 0, 0, 2, 4)
        self._grid.add(self.fr, 3, 0, 2, 4)
        self._grid.add(self.rl, 0, 5, 2, 4)
        self._grid.add(self.rr, 3, 5, 2, 4)


class Tyre(ACLabel):
    COLORS = {}
    FL = 0
    FR = 1
    RL = 2
    RR = 3

    def __init__(self, index: int, parent: ACWidget, data: ACData, meta: ACMeta):
        super().__init__(parent)

        self.background_color = TRANSPARENT

        self._data = data
        self._meta = meta

        self._index = index
        self._timer = 0
        self._wear_min, self._wear_max = 96, 100

        self._grid = ACGrid(9, 12, self)

        # Each tyre has inner, outer, center, core and brake temperature.
        # Each of these locations is rendered separately by a colored texture.
        self._left = TyreTile(TyreTile.LEFT, self._grid, self._index, self._data, self._meta)
        self._right = TyreTile(TyreTile.RIGHT, self._grid, self._index, self._data, self._meta)
        self._center_top = TyreTile(TyreTile.CENTER, self._grid, self._index, self._data, self._meta)
        self._center_bot = TyreTile(TyreTile.CENTER, self._grid, self._index, self._data, self._meta)
        self._core = TyreTile(TyreTile.CORE, self._grid, self._index, self._data, self._meta)
        self._brake = TyreTile(TyreTile.BRAKE, self._grid, self._index, self._data, self._meta)
        self._wear = ACLIBProgressBar(self._grid, self._wear_max, self._wear_min, self._wear_max)

        # Left tyre
        if self._index % 2 == 0:
            self._grid.add(self._left, 0, 0, 2, 10)
            self._grid.add(self._center_top, 3, 0, 2, 3)
            self._grid.add(self._core, 3, 4, 2, 2)
            self._grid.add(self._center_bot, 3, 7, 2, 3)
            self._grid.add(self._right, 6, 0, 2, 10)
            self._grid.add(self._brake, 8, 2, 1, 6)
        # Right tyre
        else:
            self._grid.add(self._left, 1, 0, 2, 10)
            self._grid.add(self._center_top, 4, 0, 2, 3)
            self._grid.add(self._core, 4, 4, 2, 2)
            self._grid.add(self._center_bot, 4, 7, 2, 3)
            self._grid.add(self._right, 7, 0, 2, 10)
            self._grid.add(self._brake, 0, 2, 1, 6)

        self._grid.add(self._wear, 0, 11, 9, 1)

    # Private
    def _wear_value(self):
        return self._data.tyres.wear[self._index]

    def _wear_color(self, val: float):
        val = round(val, 1)

        if val in Tyre.COLORS:
            return Tyre.COLORS[val]

        color = interpolate(val, self._wear_min, self._wear_max, RED, GREEN)

        Tyre.COLORS[val] = color
        return color

    # Public

    def update(self, delta: int):
        super().update(delta)

        self._timer += delta

        # Only update every second. Saves a bit computing power.
        if self._timer > 1:
            self._timer = 0
            self._wear.value = self._wear_value()
            self._wear.progress_color = self._wear_color(self._wear_value())


class TyreTile(ACLabel):
    TYRE_COLORS = {}
    BRAKE_COLORS = {}
    RIGHT = 0
    LEFT = 1
    CENTER = 2
    CORE = 3
    BRAKE = 4

    def __init__(self, index: int, parent: ACWidget, tyre: int, data: ACData, meta: ACMeta):
        super().__init__(parent)

        self._data = data
        self._meta = meta

        self._index = index
        self._tyre = tyre
        self._timer = 0

        # Default temperatures
        self._t_t_min, self._t_t_max = 80, 100
        self._t_t_low, self._t_t_high = 60, 120
        self._t_t_mid = 90
        self._t_t_range = 20
        self._b_t_min, self._b_t_max = 400, 500
        self._b_t_low, self._b_t_high = 300, 600
        self._b_t_mid = 450
        self._b_t_range = 100

        self._data.on(ACMeta.EVENT.READY, self._on_ready)

    # Private

    def _on_ready(self):
        self._init()
        self._data.on(ACData.EVENT.COMPOUND_CHANGED, self._init)

    def _init(self, *args):
        front = self._tyre < 2

        self._t_t_min, self._t_t_max = self._meta.tyres.ideal_temperature(self._data.tyres.compound_name, front)
        self._t_t_mid = self._t_t_min + (self._t_t_max - self._t_t_min) / 2
        self._t_t_range = self._t_t_max - self._t_t_min
        self._t_t_low = self._t_t_min - self._t_t_range * 1.5
        self._t_t_high = self._t_t_max + self._t_t_range * 1.5

        self._b_t_min, self._b_t_max = self._meta.tyres.ideal_brake_temperature(front)
        self._b_t_mid = self._b_t_min + (self._b_t_max - self._b_t_min) / 2
        self._b_t_range = self._b_t_max - self._b_t_min
        self._b_t_low = self._b_t_min - self._b_t_range * 2
        self._b_t_high = self._b_t_max + self._b_t_range * 2

        TyreTile.TYRE_COLORS = {}

    def _temp(self):
        if self._index == 0:
            return self._data.tyres.outer_temperature[self._tyre]
        elif self._index == 1:
            return self._data.tyres.center_temperature[self._tyre]
        elif self._index == 2:
            return self._data.tyres.core_temperature[self._tyre]
        elif self._index == 3:
            return self._data.tyres.inner_temperature[self._tyre]
        elif self._index == 4:
            return self._data.tyres.brake_temperature[self._tyre]

    def _temp_color(self, val: float):
        val = round(val, 1)

        # Tire
        if self._index < 4:
            if val in TyreTile.TYRE_COLORS:
                return TyreTile.TYRE_COLORS[val]

            if val < self._t_t_min:
                color = interpolate(val, self._t_t_low, self._t_t_min, BLUE, GREEN)
            elif val > self._t_t_max:
                color = interpolate(val, self._t_t_max, self._t_t_high, GREEN, RED)
            else:
                color = GREEN

            TyreTile.TYRE_COLORS[val] = color

        # Brake
        else:
            if val in TyreTile.BRAKE_COLORS:
                return TyreTile.BRAKE_COLORS[val]

            if val < self._b_t_min:
                color = interpolate(val, self._b_t_low, self._b_t_min, BLUE, GREEN)
            elif val > self._b_t_max:
                color = interpolate(val, self._b_t_max, self._b_t_high, GREEN, RED)
            else:
                color = GREEN

            TyreTile.BRAKE_COLORS[val] = color

        return color

    # Public

    def update(self, delta: int):
        super().update(delta)

        self._timer += delta

        # Use background color instead of texture and only update every 300ms. Saves a bit computing power.
        if self._timer > 0.3:
            self._timer = 0
            self.background_color = self._temp_color(self._temp())
