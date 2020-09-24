from memory.ac_data import ACData
from ui.gui.widget import ACApp, ACLabel
from ui.gui.Font import Font
from ui.gui.layout import ACGrid, ACVBox

from ui.color import *
from util.format import Format


class Driver(ACApp):
    def __init__(self, data: ACData = None, meta = None):
        super().__init__('ACLIB_Driver', 200, 200, 600, 200)

        self.hide_decoration()
        self.background_color = TRANSPARENT
        self.background = False
        self.border = False

        self._data = data
        self._medium_font = Font("Roboto Mono")
        self._medium_font.color = WHITE
        self._medium_font.size = 14

        self._big_font = Font("Roboto Mono")
        self._big_font.size = 64
        self._big_font.bold = True
        self._big_font.color = BLACK

        self._grid = ACGrid(6, 6, self)
        self._box = ACVBox(self)

        self._gear = ACLabel('', self._big_font, 'center', 'middle', self)
        self._rpm = ACLabel('', self._medium_font, 'right', 'top', self)
        self._drs = ACLabel('DRS', self._medium_font, 'center', 'middle', self)
        self._ers = ACLabel('ERS', self._medium_font, 'center', 'middle', self)
        self._kers = ACLabel('KERS', self._medium_font, 'center', 'bottom', self)

        self._box.background_texture = 'apps/python/ACLIB/resources/textures/car_hud_circle.png'

        self._grid.add(self._box, 0, 0, 2, 6)
        self._grid.add(self._rpm, 5, 1)
        self._grid.add(self._drs, 5, 2)
        self._grid.add(self._ers, 5, 3)
        self._grid.add(self._kers, 5, 4)

        self._box.add(self._gear)

        if self._data.car.has_drs: self._drs.text = 'DRS'
        if self._data.car.has_ers: self._ers.text = 'ERS'
        if self._data.car.has_kers: self._kers.text = 'KERS'

    def update(self, delta: int):
        super().update(delta)

        self._gear.text = Format.gear(self._data.car.gear)
        self._rpm.text = Format.rpm(self._data.car.rpm)

    def render(self, delta: int):
        super().render(delta)
