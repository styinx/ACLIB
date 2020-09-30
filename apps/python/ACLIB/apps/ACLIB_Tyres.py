from settings import TEXTURE_DIR, path
from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.gl import Texture, texture_rect
from ui.gui.widget import ACApp, ACLabel, ACWidget
from ui.gui.layout import ACGrid
from ui.color import *


class Tyres(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Tyres', 200, 200, 98, 160)

        self.hide_decoration()
        self.background_color = TRANSPARENT
        self.border_color = TRANSPARENT

        data.on(ACData.EVENT.READY, self.init)
        data.on(ACData.EVENT.COMPOUND_CHANGED, self.reload)

        self._data = data
        self._meta = meta

        self._grid = ACGrid(5, 5, self)

        self.fl = None
        self.fr = None
        self.rl = None
        self.rr = None

    def init(self):
        self.fl = Tyre(Tyre.FL, self._grid, self._data, self._meta)
        self.fr = Tyre(Tyre.FR, self._grid, self._data, self._meta)
        self.rl = Tyre(Tyre.RL, self._grid, self._data, self._meta)
        self.rr = Tyre(Tyre.RR, self._grid, self._data, self._meta)

        self._grid.add(self.fl, 0, 0, 2, 2)
        self._grid.add(self.fr, 3, 0, 2, 2)
        self._grid.add(self.rl, 0, 3, 2, 2)
        self._grid.add(self.rr, 3, 3, 2, 2)

        self.fl.init()
        self.fr.init()
        self.rl.init()
        self.rr.init()

    def reload(self, *args):
        self.fl.reload()
        self.fr.reload()
        self.rl.reload()
        self.rr.reload()


class Tyre(ACLabel):
    COLORS = {}
    FL = 0
    FR = 1
    RL = 2
    RR = 3

    def __init__(self, index: int, parent: ACWidget, data: ACData, meta: ACMeta):
        super().__init__(parent=parent)

        self.background_color = TRANSPARENT

        self._index = index
        self._data = data
        self._meta = meta

        self._left = None
        self._right = None
        self._center_top = None
        self._center_bot = None
        self._core = None
        self._brake = None

        self._grid = None

    def init(self):
        self._grid = ACGrid(9, 10, self)

        self._left = TyreTile(TyreTile.LEFT, self._grid, self._index, self._data, self._meta)
        self._right = TyreTile(TyreTile.RIGHT, self._grid, self._index, self._data, self._meta)
        self._center_top = TyreTile(TyreTile.CENTER, self._grid, self._index, self._data, self._meta)
        self._center_bot = TyreTile(TyreTile.CENTER, self._grid, self._index, self._data, self._meta)
        self._core = TyreTile(TyreTile.CORE, self._grid, self._index, self._data, self._meta)
        self._brake = TyreTile(TyreTile.BRAKE, self._grid, self._index, self._data, self._meta)

        if self._index % 2 == 0:
            self._grid.add(self._left, 0, 0, 2, 10)
            self._grid.add(self._center_top, 3, 0, 2, 3)
            self._grid.add(self._core, 3, 4, 2, 2)
            self._grid.add(self._center_bot, 3, 7, 2, 3)
            self._grid.add(self._right, 6, 0, 2, 10)
            self._grid.add(self._brake, 8, 2, 1, 6)
        else:
            self._grid.add(self._left, 1, 0, 2, 10)
            self._grid.add(self._center_top, 4, 0, 2, 3)
            self._grid.add(self._core, 4, 4, 2, 2)
            self._grid.add(self._center_bot, 4, 7, 2, 3)
            self._grid.add(self._right, 7, 0, 2, 10)
            self._grid.add(self._brake, 0, 2, 1, 6)

    def reload(self):
        self._left.init()
        self._right.init()
        self._center_top.init()
        self._core.init()
        self._center_bot.init()
        self._right.init()
        self._brake.init()

    def wear(self):
        return self._data.tyres.wear[self._index]

    def wear_color(self, val: float):
        val = round(val, 1)

        if val in Tyre.COLORS:
            return Tyre.COLORS[val]

        if val > 98:
            color = GREEN
        elif val > 96:
            color = YELLOW
        else:
            color = RED

        Tyre.COLORS[val] = color
        return color


class TyreTile(ACLabel):
    TEXTURES = [
        path(TEXTURE_DIR, 'tyre_right.png'),
        path(TEXTURE_DIR, 'tyre_left.png'),
        path(TEXTURE_DIR, 'tyre_center.png'),
        path(TEXTURE_DIR, 'tyre_core.png'),
        path(TEXTURE_DIR, 'tyre_brake.png')
    ]
    TYRE_COLORS = {}
    BRAKE_COLORS = {}
    RIGHT = 0
    LEFT = 1
    CENTER = 2
    CORE = 3
    BRAKE = 4

    def __init__(self, index: int, parent: ACWidget, tyre: int, data: ACData, meta: ACMeta):
        super().__init__('', parent=parent)

        self._index = index
        self._tyre = tyre
        self._data = data
        self._meta = meta
        self._texture = Texture(TyreTile.TEXTURES[index])
        # self.background_texture = self._texture.path

        self._t_t_min, self._t_t_max = 80, 100
        self._t_t_low, self._t_t_high = 60, 120
        self._t_t_mid = 90
        self._t_t_range = 20
        self._b_t_min, self._b_t_max = 400, 500
        self._b_t_low, self._b_t_high = 300, 600
        self._b_t_mid = 450
        self._b_t_range = 100
        self._compound_loaded = False

    def init(self):
        front = self._tyre < 2

        self._t_t_min, self._t_t_max = self._meta.tyres.ideal_temperature(self._data.tyres.compound_name, front)
        self._t_t_mid = self._t_t_min + (self._t_t_max - self._t_t_min) / 2
        self._t_t_range = self._t_t_max - self._t_t_min
        self._t_t_low = self._t_t_min - self._t_t_range
        self._t_t_high = self._t_t_max + self._t_t_range

        self._b_t_min, self._b_t_max = self._meta.tyres.ideal_brake_temperature(front)
        self._b_t_mid = self._b_t_min + (self._b_t_max - self._b_t_min) / 2
        self._b_t_range = self._b_t_max - self._b_t_min
        self._b_t_low = self._b_t_min - self._b_t_range
        self._b_t_high = self._b_t_max + self._b_t_range

        TyreTile.TYRE_COLORS = {}

    def update(self, delta: int):
        if not self._compound_loaded and len(self._data.tyres.compound) > 5:
            self.init()
            self._compound_loaded = True

    def render(self, delta: int):
        super().render(delta)

        x, y = self.position
        w, h = self.size
        texture_rect(x, y, w, h, self._texture, self.temp_color(self.temp()))

    def temp(self):
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

    def temp_color(self, val: float):
        val = round(val, 1)

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
