import os

from memory.ac_data import ACData
from settings import RESOURCE_DIR
from ui.gui.widget import Font, ACApp, ACLabel, ACIcon, ACWidget
from ui.gui.layout import ACGrid, ACHBox

from ui.color import Color, TRANSPARENT


class Comparator(ACApp):
    def __init__(self, data: ACData = None, meta = None):
        super().__init__('ACLIB_Comparator', 200, 200, 300, 300)

        self.hide_decoration()
        self.background_color = TRANSPARENT
        self.background = False
        self.border = False

        self._data = data

        self._grid = ACGrid(1, 4, self)

        self._header = ComparatorRow(self, data, -1)
        self._driver = ComparatorRow(self, data, 0)
        self._opponent1 = ComparatorRow(self, data, 1)
        self._opponent2 = ComparatorRow(self, data, 2)

        self._grid.add(self._header, 0, 0)
        self._grid.add(self._driver, 0, 1)
        self._grid.add(self._opponent1, 0, 2)
        self._grid.add(self._opponent2, 0 , 3)

    def update(self, delta: int):
        pass

    def render(self, delta: int):
        pass


class ComparatorRow(ACWidget):
    def __init__(self, parent: ACApp, data: ACData, driver: int):
        super().__init__(parent)
        self._header = driver == -1
        self._mode = ''

        self._header_font = Font("Roboto Mono")
        self._header_font.color = Color(0.9, 0.2, 0.2)
        self._header_font.size = 14

        self._grid = ACGrid(10, 3, parent)
        self._label = ACLabel('', self._header_font, parent=parent)

        self._top_box = ACHBox(parent)
        self._bottom_box = ACHBox(parent)
        self._left = ACIcon(os.path.join(RESOURCE_DIR, 'textures', 'cross.png'), parent)
        self._right = ACIcon(os.path.join(RESOURCE_DIR, 'textures', 'cross.png'), parent)
        self._top = []
        self._bottom = []

        self._grid.add(self._label, 1, 0, 8, 1)
        self._grid.add(self._left, 0, 1, 1, 2)
        self._grid.add(self._right, 9, 1, 1, 2)
        self._grid.add(self._top_box, 1, 1, 8, 1)
        self._grid.add(self._bottom_box, 1, 2, 8, 1)

        for i in range(0, 4):
            self._top.append(ACLabel('--:--', parent=parent))
            self._top_box.add(self._top[i])

            self._bottom.append(ACLabel('--:--', parent=parent))
            self._bottom_box.add(self._bottom[i])

        if not self._header:
            self._label.text = data.driver.firstname
        else:
            self._label.text = 'Sectors'


