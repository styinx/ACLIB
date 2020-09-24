from settings import TEXTURE_DIR, path
from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.gl import Texture, texture_rect, rect
from ui.gui.widget import ACApp, ACWidget, ACIcon, ACLabel
from ui.gui.layout import ACGrid
from ui.color import *
from util.log import log


class Tyres(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Tyres', 200, 200, 98, 160)

        self.hide_decoration()
        self.background_color = TRANSPARENT
        self.background = False
        self.border = False

        self._grid = ACGrid(5, 5, self)

        self.fl = Tyre(Tyre.FL, data, meta)
        self.fr = Tyre(Tyre.FR, data, meta)
        self.rl = Tyre(Tyre.RL, data, meta)
        self.rr = Tyre(Tyre.RR, data, meta)

        self._grid.add(self.fl, 0, 0, 2, 2)
        self._grid.add(self.fr, 3, 0, 2, 2)
        self._grid.add(self.rl, 0, 3, 2, 2)
        self._grid.add(self.rr, 3, 3, 2, 2)

        self.fl.init()
        self.fr.init()
        self.rl.init()
        self.rr.init()

    def update(self, delta: int):
        super().update(delta)

        self._grid.update(delta)

    def render(self, delta: int):
        self._grid.render(delta)


class Tyre(ACWidget):
    COLORS = {}
    FL = 0
    FR = 1
    RL = 2
    RR = 3

    def __init__(self, index: int, data: ACData, meta: ACMeta):
        super().__init__('')

        self.background_color = Color(0, 0, 0, 0.25)
        self.background = True

        self._index = index
        self._data = data

        self._left = TyreTile(TyreTile.LEFT, index, data, meta)
        self._right = TyreTile(TyreTile.RIGHT, index, data, meta)
        self._center_top = TyreTile(TyreTile.CENTER, index, data, meta)
        self._center_bot = TyreTile(TyreTile.CENTER, index, data, meta)
        self._core = TyreTile(TyreTile.CORE, index, data, meta)
        self._brake = TyreTile(TyreTile.BRAKE, index, data, meta)

        self._grid = None

    def init(self):
        self._grid = ACGrid(9, 10, self)

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

    def update(self, delta: int):
        self._grid.update(delta)

    def render(self, delta: int):
        self._grid.render(delta)

        # x, y = self.position
        # w, h = self.size
        #
        # if self._index < 2:
        #     rect(x, y, w, 10, self.wear_color(self.wear()))
        #
        # else:
        #     rect(x, y + h - 10, w, 10, self.wear_color(self.wear()))


class TyreTile(ACWidget):
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

    def __init__(self, index: int, tyre: int, data: ACData, meta: ACMeta):
        super().__init__(None)

        self._index = index
        self._tyre = tyre
        self._data = data
        self._meta = meta
        self._texture = Texture(TyreTile.TEXTURES[index])
        # self.background_texture = self._texture.path

        self._t_t_min, self._t_t_max = 80, 100
        self._b_t_min, self._b_t_max = 400, 500
        self._compound_loaded = False

    def update(self, delta: int):
        if not self._compound_loaded and len(self._data.tyres.compound) > 5:
            self.init()
            self._compound_loaded = True

    def render(self, delta: int):
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
                color = BLUE
            elif val > self._t_t_max:
                color = RED
            else:
                color = GREEN

            TyreTile.TYRE_COLORS[val] = color

        else:
            if val in TyreTile.BRAKE_COLORS:
                return TyreTile.BRAKE_COLORS[val]

            if val < self._b_t_min:
                color = BLUE
            elif val > self._b_t_max:
                color = RED
            else:
                color = GREEN

            TyreTile.TYRE_COLORS[val] = color

        return color

    def init(self):
        front = self._tyre < 2
        self._t_t_min, self._t_t_max = self._meta.tyres.ideal_temperature(self._data.tyres.compound_name, front)

        TyreTile.TYRE_COLORS = {}
