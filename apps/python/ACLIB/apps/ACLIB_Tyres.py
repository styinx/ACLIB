import os

from settings import TEXTURE_DIR
from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.gl import Texture, texture_rect
from ui.gui.widget import ACApp, ACWidget
from ui.gui.layout import ACGrid
from ui.color import *


class Tyres(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Tyres', 200, 200, 98, 160)

        self.hide_decoration()
        self.background_color = TRANSPARENT
        self.background = False
        self.border = False

        self._grid = ACGrid(5, 5, self)

        self.fl = Tyre(self, Tyre.FL, data, meta)
        self.fr = Tyre(self, Tyre.FR, data, meta)
        self.rl = Tyre(self, Tyre.RL, data, meta)
        self.rr = Tyre(self, Tyre.RR, data, meta)

        self._grid.add(self.fl, 0, 0, 2, 2)
        self._grid.add(self.fr, 3, 0, 2, 2)
        self._grid.add(self.rl, 0, 3, 2, 2)
        self._grid.add(self.rr, 3, 3, 2, 2)

        self.fl.init()
        #self.fr.init()
        #self.rl.init()
        self.rr.init()

    def update(self, delta: int):
        self._grid.update(delta)

    def render(self, delta: int):
        self._grid.render(delta)


class Tyre(ACWidget):
    FL = 0
    FR = 1
    RL = 2
    RR = 3

    def __init__(self, parent: ACWidget, index: int, data: ACData, meta: ACMeta):
        super().__init__(parent)

        self._index = index

        self._left = TyreTile(self.app, TyreTile.LEFT, index, data, meta)
        self._right = TyreTile(self.app, TyreTile.RIGHT, index, data, meta)
        self._center_top = TyreTile(self.app, TyreTile.CENTER, index, data, meta)
        self._center_bot = TyreTile(self.app, TyreTile.CENTER, index, data, meta)
        self._core = TyreTile(self.app, TyreTile.CORE, index, data, meta)
        self._brake = TyreTile(self.app, TyreTile.BRAKE, index, data, meta)

        self._grid = None

    def init(self):

        self._grid = ACGrid(8, 10, self)

        self._grid.add(self._left, 0, 0, 2, 10)
        self._grid.add(self._center_top, 3, 0, 2, 3)
        self._grid.add(self._core, 3, 4, 2, 2)
        self._grid.add(self._center_bot, 3, 7, 2, 3)
        self._grid.add(self._right, 6, 0, 2, 10)

        if self._index % 2 == 0:
            self._grid.add(self._brake, 4, 2, 1, 6)
        else:
            self._grid.add(self._brake, 3, 2, 1, 6)

    def update(self, delta: int):
        if self._grid:
            self._grid.update(delta)

    def render(self, delta: int):
        if self._grid:
            self._grid.render(delta)


class TyreTile(ACWidget):
    TEXTURES = [
        os.path.join(TEXTURE_DIR, 'tyre_left.png'),
        os.path.join(TEXTURE_DIR, 'tyre_right.png'),
        os.path.join(TEXTURE_DIR, 'tyre_center.png'),
        os.path.join(TEXTURE_DIR, 'tyre_core.png'),
        os.path.join(TEXTURE_DIR, 'tyre_brake.png')
    ]
    COLORS = {}
    LEFT = 0
    RIGHT = 1
    CENTER = 2
    CORE = 3
    BRAKE = 4

    def __init__(self, parent: ACWidget, index: int, tyre: int, data: ACData, meta: ACMeta):
        super().__init__(parent)

        self._index = index
        self._tyre = tyre
        self._data = data
        self._meta = meta
        self._texture = Texture(TyreTile.TEXTURES[index])
        #self.background_texture = self._texture.path

        self._t_min, self._t_max = 80, 100
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

    def temp_color(self, val: int):
        val = round(val, 1)

        if val in TyreTile.COLORS:
            return TyreTile.COLORS[val]

        if val < self._t_min:
            color = BLUE
        elif val > self._t_max:
            color = RED
        else:
            color = GREEN

        TyreTile.COLORS[val] = color
        return val

    def init(self):
        front = self._tyre < 2
        self._t_min, self._t_max = self._meta.tyres.ideal_temperature(self._data.tyres.compound_name, front)

        TyreTile.COLORS = {}
